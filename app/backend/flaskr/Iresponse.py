from flask import jsonify

def create_response(body, status_code):
    response = jsonify(body)
    response.status_code = status_code
    return response

def empty_json_request():
    return create_response("", 400)


def internal_server_error():
    return create_response("", 500)
