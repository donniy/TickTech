from flask import jsonify


def create_response(body, status_code):
    """
    Function that creates an http response
    with the specfied status code and in the body
    of the request the given object in the body param.
    The body will be jsonified, so it should be an object
    that is serialized.
    """
    response = jsonify(json_data=body)
    response.status_code = status_code
    return response


def empty_json_request():
    """
    Helper for creating a response when a empty json
    was supplied in the request.
    """
    return create_response("", 400)


def internal_server_error():
    """
    Easy helper for when a server error happened.
    """
    return create_response("", 500)
