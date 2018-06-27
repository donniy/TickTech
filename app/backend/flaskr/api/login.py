from flask import request
from . import apiBluePrint
from flaskr.models import user, Course
from flask_jwt_extended import jwt_required, create_access_token
from flaskr.jwt_wrapper import get_current_user
from flaskr import Iresponse, database


@apiBluePrint.route('/login', methods=['POST'])
def login():
    """
    Function that checks if a user has the right credentials.
    If the user has the right credentials, it will be given a
    JWT.
    """
    user_id = request.json.get('username')
    if not user_id:
        return Iresponse.create_response('', 403)

    curr_user = user.User.query.get(user_id)

    if not curr_user:
        return Iresponse.create_response("Invalid user", 403)

    identity_wrapped = {
        'user_id': curr_user.id,
        'in_lti': False,
    }
    acces_token = create_access_token(identity=identity_wrapped)
    return Iresponse.create_response({'status': 'success',
                                      'user': curr_user.serialize,
                                      'access_token': acces_token}, 200)


@apiBluePrint.route('/user/retrieve', methods=['GET'])
@jwt_required
def retrieve_user():
    """
    Returns the user model of the current user.
    """
    current_identity = get_current_user()
    student, ta, supv, usr = {}, {}, {}, {}
    student = database.serialize_list(current_identity.student_courses)
    ta = database.serialize_list(current_identity.ta_courses)
    supv = database.serialize_list(current_identity.supervisors)

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
