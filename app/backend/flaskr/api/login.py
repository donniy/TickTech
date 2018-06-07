from flask import jsonify, request
from . import apiBluePrint


@apiBluePrint.route('/login', methods=['GET'])
def login():
    """
    Kijk of de login gegevens in POST correct zijn/communiceer met Canvas.
    """
    # TODO: Implementeer communicatie met canvas.
    return jsonify({'status': "success", 'message': {'text': request.json.get("message"), 'user_id': 12345678, 'id': 5}})
