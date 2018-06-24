from flask import jsonify, request
from . import apiBluePrint
from flaskr.models import user, Course
from flask_jwt_extended import jwt_required, create_access_token,
from flaskr.jwt_wrapper import get_current_user
from flaskr import Iresponse


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

    acces_token = create_access_token(identity=curr_user.id)
    return Iresponse.create_response({'status': 'success',
                                      'user': curr_user.serialize,
                                      'access_token': acces_token}, 200)


@apiBluePrint.route('/user/retrieve', methods=['GET'])
@jwt_required
def retrieve_user():
    """
    Returns the user model of the current user.
    """
    # print("retrieving user: " + str(current_identity))
    curr_user = get_current_user()
    print(curr_user.courses_user_is_ta_in)
    return Iresponse.create_response({'user': curr_user.serialize}, 200)

    student, ta, usr = {}, {}, {}
    for s in current_identity.student_courses:
        student = {**student, **(s.serialize)}
    for t in current_identity.ta_courses:
        ta = {**ta, **(t.serialize)}

    usr = current_identity.serialize
    usr['student'] = student
    usr['ta'] = ta
    return Iresponse.create_response({'user': usr}, 200)
