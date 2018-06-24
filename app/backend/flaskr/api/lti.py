from . import apiBluePrint
from flask import request, redirect, jsonify
from flaskr.i_request import *
from flaskr import lti, Iresponse
from flask_jwt import JWT
from flaskr.models import user
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from flaskr.jwt_wrapper import get_current_user, lti_session_required
from flask_jwt_extended.tokens import (
    encode_refresh_token, encode_access_token
)

@apiBluePrint.route('lti/launch', methods=['POST'])
def launch_lti_session():
    """
    Function that get called by canvas to launch an lti request.
    From here we create an access token that will be used.
    We encode the lti session inside the jwt and set
    that we are in an lti session.
    """
    i_req = IrequestFlask()
    i_req.transform_request_to_internal_request(request)
    try:
        lti_instance = lti.LTI_instance(i_req)
    except lti.InvalidLTIRequest:
        return "Invalid LTI request, check your key and secret."

    print(lti_instance.params)
    user_id = lti_instance.user_id
    curr_user = user.User.query.get(user_id)
    if curr_user is None:
        return Iresponse.create_repsonse("Invalid user", 403)

    lti_instance.params['in_lti'] = True
    access_token = create_access_token(identity=lti_instance.params)
    # Add base url instead of hardcoded.
    return redirect("http://localhost:5000/start_lti_instance/" + access_token, 302)


@apiBluePrint.route('lti/auth_session', methods=['POST'])
@jwt_required
def auth_lti_session():
    """
    Function to authenticate the lti session.
    So, this checks if a valid token was supplied, this
    is done by the jwt_required decorator.
    """
    return Iresponse.create_response("", 200)


@apiBluePrint.route('lti/get_lti_params', methods=['GET'])
@lti_session_required  # This also checks for a jwt token.
def get_lti_params():
    return Iresponse.create_response(get_jwt_identity(), 200)
