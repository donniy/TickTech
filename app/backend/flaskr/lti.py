from . import i_request
from flaskr.models.Course import Course
from flaskr.models.user import User
from flaskr import database
from flask import redirect
import oauth2
import requests
import uuid
"""
This file contains some of the code for lti from the following file:
Mostly the signature validation.
https://github.com/CodeGra-de/CodeGra.de/blob/master/psef/auth.py


This module containts most of the logic for LTI.
Possible data given by the LTI launch request can be found here:
https://github.com/instructure/canvas-lms/blob/stable/lib%2Flti%2Fvariable_expander.rb#L83

The above source also shows custom variables that can be added to the xml.
So far we use on custom variable, check the xml.
"""

lti_base_route = 'http://localhost:3000'
lti_api_route = '/api/v1'

# ext_roles are roles a person has over all the courses.
ext_roles_lookup_table = {
    'urn:lti:role:ims/lis/Learner': 'student',
    'urn:lti:role:ims/lis/Instructor': 'teacher',
    'urn:lti:role:ims/lis/TeachingAssistant': 'teachingAssistant',
    'urn:lti:role:ims/lis/ContentDeveloper': 'designer',
    'urn:lti:role:ims/lis/Learner/NonCreditLearner': 'observer',
}

# Map for the roles a person has in a certain course.
course_roles_lookup_table = {
    'Learner': 'student',
    'Instructor': 'teacher',
    'urn:lti:role:ims/lis/TeachingAssistant': 'teachingAssistant',
}


class InvalidLTIRequest(Exception):
    pass


class LTI_instance_database_helper:
    """
    Class that ensures that for all the data
    in the lti instance exists in our database.
    """
    def __init__(self, lti_instance):
        # Cache for queried objects.
        self.cache = {}
        self.lti_instance = lti_instance
        self.ensure_course_exists()
        self.ensure_user_exists()
        self.ensure_user_coupled_to_course()
        # Clear the cache again.
        self.cache = {}

    def ensure_course_exists(self):
        """
        Function that ensures the course in the lti instance
        exists.
        """
        print(self.lti_instance.params)
        canvas_course_id = self.lti_instance.params['custom_canvas_course_id']
        course = Course.query.filter_by(canvas_unique_id=canvas_course_id).first()
        course_name = self.lti_instance.course_name
        if course is None:
            self.lti_instance.params['new_tiktech_course'] = True
            course = Course(id=uuid.uuid4(), title=course_name,
                            description=self.lti_instance.course_description,
                            canvas_unique_id = canvas_course_id)
            if not database.addItemSafelyToDB(course, self.ensure_course_exists):
                self.cache['course'] = None
                return
        self.lti_instance.params['tiktech_course_id'] = course.id
        self.cache['course'] = course

    def ensure_user_exists(self):
        """
        Function that ensures the user exists.
        """
        user_id = int(self.lti_instance.user_id)
        print(user_id)
        user = User.query.get(user_id)
        if user is None:
            user = User()
            user.create(id=user_id,
                        name=self.lti_instance.user_full_name,
                        email=self.lti_instance.user_primary_email,
                        password="1")
            if not database.addItemSafelyToDB(user):
                user = None
        self.cache['user'] = user

    def ensure_user_coupled_to_course(self):
        """
        Function that ensures a user is linked to the course with the
        right role.
        """
        course = self.cache['course']
        user = self.cache['user']
        if course is None or user is None:
            return
        if self.lti_instance.is_student_in_course():
            if user not in course.student_courses:
                course.student_courses.append(user)
        if self.lti_instance.is_teacher_in_course():
            if user not in course.supervisors:
                course.supervisors.append(user)
        if self.lti_instance.is_teaching_assistant_in_course():
            if user not in course.ta_courses:
                course.ta_courses.append(user)

        # Wrap this into a safe commit.
        database.get_db().session.commit()


class LTI_instance:
    """
    Class that is an lti_instance. It has all the required information
    from an lti request and exposes them as properties. This instance
    does not contain any oauth information.
    The instance class makes sure that all the data exists in the database
    or is created and inserted into the database.
    This class thus exposes all the information that is required.
    """
    def __init__(self, i_req):
        """
        Createn an LTI instance from an internal request.
        It removes all the sensitive data from the request
        and only keeps it body. However this can be adapted.
        It checks if the request from which we create the instance
        is valid. If the request is not valid we throw an
        InvalidLTIRequest.
        """
        self.params = {}
        self.database_helper = None
        try:  # Maybe wrap this into a helper class.
            self._validate_lti_Irequest_signature(i_req)
            self._sanitize_lti_Irequest(i_req)
            self._ensure_params_exists(self.params)
            self._map_course_roles_to_internal_roles()
        except InvalidLTIRequest:
            raise
        self.database_helper = LTI_instance_database_helper(self)

    def _ensure_params_exists(self, body):
        """
        Ensure the request has the required parameters given
        in its body.
        """
        required_keys = [
            'context_title',
            'context_label',
            'lis_person_name_full',
            'roles',
            'lis_person_contact_email_primary',
            'lis_person_sourcedid',
            'lis_person_contact_email_primary',
        ]
        for key in required_keys:
            if body.get(key) is None:
                print("Required key is missing: {}".format(key))
                raise InvalidLTIRequest

    # TODO: add getting of secret key from consumerKey
    def _validate_lti_Irequest_signature(self, i_req):
        """
        Function that validates an LTI request by
        recreating the signature and comparing
        this with the provided signature.
        For this we require that the LTI request
        is wrapped in a Irequest(Internal request)
        object.
        For this it uses the python3-oauth2 libary.
        source:
        https://github.com/i-kiwamu/python3-oauth2/blob/master/oauth2/__init__.py

        If the LTI request is invalid, we throw an
        InvalidLTIRequest exception and log the error.
        """
        oauth_server = oauth2.Server()
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        oauth_server.add_signature_method(signature_method)
        consumer = oauth2.Consumer('consumerKey', 'test')
        oauth_request = oauth2.Request.from_request(
            i_req.method, i_req.url, i_req.headers, i_req.body)

        try:
            oauth_server.verify_request(oauth_request, consumer, {})
        except Exception as e:
            print(e)  # debug
            raise InvalidLTIRequest

    def _sanitize_lti_Irequest(self, i_req):
        """
        Function that removes all the sensitive data
        from an LTI request. And adds the remaining
        data to the body of self.
        """
        for key in i_req.body.copy().keys():
            if key.startswith('oauth'):
                del i_req.body[key]
        self.params = i_req.body

    def _map_course_roles_to_internal_roles(self):
        for role in self.params['roles'].split(','):
            internal_role = course_roles_lookup_table.get(role)
            if internal_role is None:  # Some roles are not valuable for us.
                continue
            if course_roles_lookup_table[role] is 'student':
                self.params['tiktech_is_course_student'] = True
            elif course_roles_lookup_table[role] is 'teacher':
                self.params['tiktech_is_course_teacher'] = True
            elif course_roles_lookup_table[role] is 'teachingAssistant':
                self.params['tiktech_is_course_TA'] = True

    def is_student_in_course(self):
        is_student = self.params.get('tiktech_is_course_student')
        if is_student is None:
            return False
        return is_student is True

    def is_teaching_assistant_in_course(self):
        is_ta = self.params.get('tiktech_is_course_TA')
        if is_ta is None:
            return False
        return is_ta is True

    def is_teacher_in_course(self):
        is_teacher = self.params.get('tiktech_is_course_teacher')
        if is_teacher is None:
            return False
        return is_teacher is True

    @property
    def course_name(self):
        return self.params['context_title']

    @property
    def course_description(self):
        return self.params['context_label']

    @property
    def user_full_name(self):
        return self.params['lis_person_name_full']

    @property
    def user_id(self):
        return self.params['lis_person_sourcedid']

    @property
    def user_primary_email(self):
        return self.params['lis_person_contact_email_primary']


def ensure_user_couples_to_course(user, course, user_data):
    """
    Helper for the one time fill function for canvas courses.
    It ensures the user is couples rightly to the course.
    """
    for role in user_data.get('enrollments'):
        role_type = role.get('type')
        if role_type == "StudentEnrollment":
            course.student_courses.append(user)
            break
        elif role_type == "TaEnrollment":
            course.ta_courses.append(user)
            break
        elif role_type == "TeacherEnrollment":
            course.supervisors.append(user)
            break
    database.commitSafelyToDB(func=ensure_user_couples_to_course)


def fill_new_course_with_canvas_data(headers, course_id):
    """
    A function that fills a new course with data from canvas.
    This function is only called if a new course is created.
    It then fills the course with students, tas and teachers.
    """
    request_url = lti_base_route + lti_api_route
    request_url += '/courses/{}/users?'.format(course_id)
    request_url += 'include[]=enrollments&include[]=email'
    user_req = requests.get(request_url, headers=headers)

    users = user_req.json()
    if user_req.status_code != 200:
        return

    for user in users:
        user_id = user.get('sis_user_id')
        if user_id is None:
            return

        existing_user = User.query.get(user_id)
        if existing_user is None:
            name = user.get('name')
            email = user.get('email')
            existing_user = User()
            existing_user.create(id=user_id, name=name, email=email,
                                 password="1")
            if not database.addItemSafelyToDB(existing_user,
                                              fill_new_course_with_canvas_data):
                continue

        course = Course.query.filter_by(canvas_unique_id=course_id).first()
        if course is None:
            return
        ensure_user_couples_to_course(existing_user, course, user)
