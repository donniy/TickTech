from flask import jsonify, request
from . import apiBluePrint
from flaskr.models import user
from flask_jwt import jwt_required, current_identity


@apiBluePrint.route('/login', methods=['POST'])
def login():
    """
    Kijk of de login gegevens in POST correct zijn/communiceer met Canvas.
    """
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)

    return jsonify({'status': 'success', 'user': user.serialize})

@apiBluePrint.route('/user/retrieve', methods=['GET'])
@jwt_required()
def get_user():
    """
    Returns the user model of the current user.
    """
    print("retrieving user")
    return jsonify({'user': current_identity.serialize})