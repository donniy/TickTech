from flask import request
from . import apiBluePrint
from flaskr.models import user, Course
from flask_jwt_extended import jwt_required, create_access_token
from flaskr.jwt_wrapper import get_current_user
from flaskr import Iresponse, database


@apiBluePrint.route('/login', methods=['POST'])
def login():
    """
    Kijk of de login gegevens in POST correct zijn/communiceer met Canvas.
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
    student, ta, usr = {}, {}, {}
    student = database.serialize_list(current_identity.student_courses)
    ta = database.serialize_list(current_identity.ta_courses)
    supervisor = database.serialize_list(current_identity.supervisor_courses)
    print(supervisor)
    usr = current_identity.serialize
    usr['student'] = student
    usr['ta'] = ta
    usr['supervisor'] = supervisor
    return Iresponse.create_response({'user': usr}, 200)
