from . import i_request
from flaskr.models.Course import Course
from flaskr.models.user import User
from flaskr import database
import oauth2
import uuid
"""
This file contains some of the code for lti from the following file:
Mostly the signature validation.
https://github.com/CodeGra-de/CodeGra.de/blob/master/psef/auth.py

"""

class LTI_roles_mapper:
    def __init__(ext_roles):
        pass


# TODO: Add batch processing for the database.
class InvalidLTIRequest(Exception):
    pass


class LTI_instance_database_helper:
    """
    Class that ensures that for all the data
    in the lti instance exists in our database.
    """
    def __init__(self, lti_instance):
        self.lti_instance = lti_instance
        self.ensure_course_exists()
        self.ensure_user_exists()

    def ensure_course_exists(self):
        """
        Function that ensures the course in the lti instance
        exists.
        """
        course_name = self.lti_instance.course_name
        if Course.query.filter_by(title=course_name).first() is None:
            course = Course(id=uuid.uuid4(), title=course_name,
                            description=self.lti_instance.course_description)
            if not database.addItemSafelyToDB(course):
                pass

    def ensure_user_exists(self):
        """
        Function that ensures the user exists.
        """
        user_id = int(self.lti_instance.user_id)
        if User.query.get(user_id) is None:
            user = User(id=user_id,
                        name=self.lti_instance.user_full_name,
                        email=self.lti_instance.user_primary_email)
            if not database.addItemSafelyToDB(user):
                pass
        print(User.query.all())

    def ensure_user_coupled_to_course(self):


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
        try:
            self._validate_lti_Irequest_signature(i_req)
            self._sanitize_lti_Irequest(i_req)
            self._ensure_params_exists(self.params)
        except InvalidLTIRequest:
            raise
        print(self.params)
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
            'ext_roles',
            'lis_person_contact_email_primary',
        ]
        for key in required_keys:
            if body.get(key) is None:
                print(key)
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

    @property
    def get_mapped_roles(self):
        if self.params.get('mapped_roles') is None:
            self.map_ext_roles_to_roles()
        return self.params['mapped_roles']

    def _map_ext_roles_to_roles(self):
        self.params['mapped_roles'] = LTI_roles_mapper(self.params['ext_roles'])
