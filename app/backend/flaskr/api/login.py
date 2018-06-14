from flask import jsonify, request
from . import apiBluePrint
from flaskr.models import user
from flask_jwt import jwt_required, current_identity
from flaskr import Iresponse


@apiBluePrint.route('/login', methods=['POST'])
def login():
    """
    Kijk of de login gegevens in POST correct zijn/communiceer met Canvas.
    """
    user_id = request.json.get('user_id')
    if not user_id:
        return Iresponse.create_response('', 403)

    user = User.query.get(user_id)

    if not user:
        return Iresponse.create_response("Invalid user", 403)

    return Iresponse.create_response({'status': 'success', 'user':
                                      user.serialize}, 200)


@apiBluePrint.route('/user/retrieve', methods=['GET'])
@jwt_required()
def retrieve_user():
    """
    Returns the user model of the current user.
    """
    print("retrieving user: " + str(current_identity))
    student, ta, usr = {}, {}, {}
    for s in current_identity.student_courses:
        student = {**student, **(s.serialize)}
    for t in current_identity.ta_courses:
        ta = {**ta, **(t.serialize)}

    usr = current_identity.serialize
    usr['student'] = student
    usr['ta'] = ta
    return Iresponse.create_response({'user': usr}, 200)
