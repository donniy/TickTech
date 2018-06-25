from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flaskr.models import user
from flaskr import Iresponse
from functools import wraps


def get_current_user():
    """
    Gets the current user from a jwt token.
    How the user is retrieved depends on the environment
    we are in.
    """
    curr_identity = get_jwt_identity()
    if curr_identity is None:
        return None
    if curr_identity['in_lti']:
        return user.User.query.get(curr_identity['lis_person_sourcedid'])
    return user.User.query.get(curr_identity['user_id'])


def lti_session_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        curr_identity = get_jwt_identity()
        if curr_identity is None:
            return Iresponse.create_response("", 404)

        if not curr_identity['in_lti']:
            return Iresponse.create_response("", 412)
        return func(*args, **kwargs)
    return wrapper
