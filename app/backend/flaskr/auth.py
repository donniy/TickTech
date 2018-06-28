from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flaskr.jwt_wrapper import get_current_user
from flaskr import Iresponse
from flaskr.models import Course


def require_ta_rights_in_course(course_id):
    """
    Function that can be used as a decorator, to require
    that an api path can only be accessed if the user
    has ta rights in the specified course. This means the user
    is either TA or supervisor(teacher) in this course.
    The course_id of the course should be given to
    this decorator and a valid jwt should be present
    from which the user can be extracted.
    """

    def decorator(func):
        """
        This decorator is required, so we can give
        a param to the require_ta_in_course decorator.
        """

        @wraps(func)
        def verify_ta_rights_in_course(*args, **kwargs):
            """
            Function that verifies that an user has ta rights in the specified
            course. This function required that the course_id is specified
            in the decorator.

            Returns on failure:
            - Iresponse 400: if the user can not be extracted from the jwt.
            - Iresponse 404: if the course can not be found.
            - Iresponse 403: if the user is not a ta in the course.

            Returns on succes:
            - Calls the decorated function, with the following params:
            (course, user, *args, **kwargs).
            So the decorated function should always accept atleast two params,
            namely the course and user, in that order.
            Extra params, should come after the course and user.
            """
            verify_jwt_in_request()
            curr_user = get_current_user()
            course = Course.Course.query.get(course_id)
            if curr_user is None:
                return Iresponse.create_response("", 400)
            if course is None:
                return Iresponse.create_response("Course not found", 404)
            if curr_user not in course.ta_courses:
                if curr_user not in course.supervisors:
                    return Iresponse.create_response("", 403)
            return func(course, curr_user, *args, **kwargs)
        return verify_ta_rights_in_course
    return decorator


def require_role(roles):
    def wrapper(fn):
        """
        Function that can be used as a decorator, to require
        that an api path can only be accessed if the user
        is a ta in the specified course. The course_id of the
        course should be given to this decorator and a valid
        jwt should be present from which the user can be extracted.
        """
        @wraps(fn)
        def verify_roles(*args, **kwargs):
            """
            Function that verifies that an user is a ta in the specified
            course. This function required that the course_id is specified
            in the decorator.

            Returns on failure:
            - Iresponse 400: if the user can not be extracted from the jwt.
            - Iresponse 404: if the course can not be found.
            - Iresponse 403: if the user is not a ta in the course.

            Returns on succes:
            - Calls the decorated function, with the following params:
            (course, user, *args, **kwargs).
            So the decorated function should always accept atleast two params,
            namely the course and user, in that order.
            Extra params, should come after the course and user.
            """
            verify_jwt_in_request()
            curr_user = get_current_user()

            c_ta = 'ta' in roles
            c_ta &= len(curr_user.ta_courses) > 0
            c_stud = 'student' in roles
            c_stud &= len(curr_user.student_courses) > 0
            c_super = 'supervisor' in roles
            c_super &= len(curr_user.supervisor_courses) > 0

            if curr_user is None:
                return Iresponse.create_response("", 400)
            if type(roles) != list:
                return Iresponse.create_response("", 500)
            if not c_ta and not c_stud and not c_super:
                return Iresponse.create_response(
                    "User doesn\'t have a correct role.",
                    403
                )

            return fn(*args, **kwargs)
        return verify_roles
    return wrapper

