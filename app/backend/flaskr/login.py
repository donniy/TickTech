from .models import user
from flask_jwt_extended import JWTManager
from flaskr import Iresponse

jwt = None


def authenticate(username, password):
    """
    Kijk of de login gegevens in POST correct zijn/communiceer met Canvas.
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
