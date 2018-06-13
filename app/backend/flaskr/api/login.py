from flask import jsonify, request
from . import apiBluePrint
from flaskr.models import user
from flask_jwt import jwt_required, current_identity
from flaskr import Iresponse
from flaskr.models.user import *


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

    return Iresponse.create_response({'status': 'success', 'user': user.serialize}, 200)

@apiBluePrint.route('/user/retrieve', methods=['GET'])
@jwt_required()
def retrieve_user():
    """
    Returns the user model of the current user.
    """
    print("retrieving user")
    return Iresponse.create_response({'user': current_identity.serialize}, 200)