from .models import user
from flask_jwt_extended import JWTManager
from flaskr import Iresponse

jwt = None


def authenticate(username, password):
    """
    Check if the login credentials in post are
    in line with Canvas requirements
    """
    usr = user.User.query.filter_by(id=username).first()
    return usr


def identity(payload):
    usr = user.User.query.filter_by(id=payload['identity']).first()
    if not usr:
        return Iresponse.create_response("Invalid user", 403)
    return usr


def init_jwt(app=None):
    if not app:
        raise Exception('No app parameter')
    global jwt
    jwt = JWTManager(app)
