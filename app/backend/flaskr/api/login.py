from flask import jsonify, request
from . import apiBluePrint
from flaskr.models import user


@apiBluePrint.route('/login', methods=['POST'])
def login():
    """
    Kijk of de login gegevens in POST correct zijn/communiceer met Canvas.
    """
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)

    return jsonify({'status': 'success', 'user': user.serialize})