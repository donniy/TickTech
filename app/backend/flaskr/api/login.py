from flask import jsonify, request
from . import apiBluePrint
from flask_login import login_user
from flaskr.models.User import *


@apiBluePrint.route('/login', methods=['GET'])
def login():
    """
    Kijk of de login gegevens in POST correct zijn/communiceer met Canvas.
    """
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    return jsonify({'status': "success", 'message': {'text': request.json.get("message"), 'user_id': 12345678, 'id': 5}})
