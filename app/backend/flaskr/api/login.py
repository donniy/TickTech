from flask import request
from . import apiBluePrint
from flaskr.models import Course
from flaskr.models.user import User
from flask_jwt_extended import jwt_required, create_access_token
from flaskr.jwt_wrapper import get_current_user
from flaskr import Iresponse, database
from flaskr.utils import json_validation
import bcrypt


@apiBluePrint.route('/login', methods=['POST'])
def login():
    """
    Function that checks if a user has the right credentials.
    If the user has the right credentials, it will be given a
    JWT.
    """
    json_data = request.get_json()
    if not json_validation.validate_json(json_data, ['email', 'password']):
        return Iresponse.create_response("Bad request", 400)

    user_email = request.json.get('email')
    password = request.json.get('password')
    user_info = User.query.filter_by(email=user_email).first()
    if not user_info:
        return Iresponse.create_response('No user found by this email', 404)

    # Check password
    hashedpsw = user_info.password
    if hashedpsw == bcrypt.hashpw(password.encode('utf-8'), hashedpsw):
        identity_wrapped = {
            'user_id': user_info.id,
            'in_lti': False,
        }
        acces_token = create_access_token(identity=identity_wrapped)
        return Iresponse.create_response({'status': 'success',
                                          'user': user_info.serialize,
                                          'access_token': acces_token}, 200)
    else:
        return Iresponse.create_response('Wrong password', 403)


@apiBluePrint.route('/user/retrieve', methods=['GET'])
@jwt_required
def retrieve_user():
    """
    Returns the user model of the current user.
    """
    current_identity = get_current_user()
    if current_identity is None:
        return Iresponse.create_response("", 404)

    student, ta, supv, usr = {}, {}, {}, {}
    student = database.serialize_list(current_identity.student_courses)
    ta = database.serialize_list(current_identity.ta_courses)
    supv = database.serialize_list(current_identity.supervisor_courses)

    usr = current_identity.serialize
    usr['student'] = student
    usr['ta'] = ta
    usr['supervisor'] = supv
    usr['roles'] = []

    if len(usr['student']) >= 1:
        usr['roles'].append('student')
    if len(usr['ta']) >= 1:
        usr['roles'].append('ta')
    if len(usr['supervisor']) >= 1:
        usr['roles'].append('supervisor')

    return Iresponse.create_response({'user': usr}, 200)
