from . import apiBluePrint
from flask import request, redirect, jsonify
from flaskr.i_request import *
from flaskr import lti, Iresponse
from flask_jwt import JWT
from flaskr.models import user
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from flaskr.jwt_wrapper import get_current_user, lti_session_required
import datetime
from flask_jwt_extended.tokens import (
    encode_refresh_token, encode_access_token
)
import requests


@apiBluePrint.route('lti/launch', methods=['POST'])
def launch_lti_session():
    """
    Function that get called by canvas to launch an lti request.
    From here we create an access token that will be used.
    We encode the lti session inside the jwt and set
    that we are in an lti session. The token we give
    is only valid for one minute, this is because we
    supply it in the route of the redirect.
    """
    i_req = IrequestFlask()
    i_req.transform_request_to_internal_request(request)
    try:
        lti_instance = lti.LTI_instance(i_req)
    except lti.InvalidLTIRequest:
        return "Invalid LTI request, check your key and secret."

    user_id = lti_instance.user_id
    curr_user = user.User.query.get(user_id)
    if curr_user is None:
        return Iresponse.create_repsonse("Invalid user", 403)

    # One minutes should be secure and enough?.
    expires = datetime.timedelta(minutes=1)
    lti_instance.params['in_lti'] = True
    print(lti_instance.params)
    access_token = create_access_token(identity=lti_instance.params,
                                       expires_delta=expires)

    #if lti_instance.params.get('new_tiktech_course'):
    return redirect('http://localhost:3000/login/oauth2/auth?client_id=10000000000036&response_type=code&redirect_uri=http://localhost:5000/start_lti_instance/'
                    + access_token)

    return redirect('http://localhost:5000/start_lti_instance/' + access_token)


def get_all_users_of_canvas_course_via_api(code, token):
    url = 'http://localhost:3000/login/oauth2/token'
    resp = requests.post(url, data = {
        'grant_type': 'authorization_code',
        'client_id': 10000000000036,
        'client_secret': 'XcHBV43CIqs4SZlgvFU6a2STQrF4YHGnQ26aMQiIIdNX0oCMcx3Eqpbvdqdwtrks',
        'redirect_uri': 'http://localhost:5000/start_lti_instance/' + token,
        'code': code
    })
    access_token = resp.json().get('access_token')
    headers = {'Authorization': 'Bearer ' + access_token}
    lti.fill_new_course_with_canvas_data(headers)


@apiBluePrint.route('lti/auth_session', methods=['POST'])
@jwt_required
def auth_lti_session():
    """
    Function to authenticate the lti session.
    So, this checks if a valid token was supplied, this
    is done by the jwt_required decorator.
    If a valid jwt token is found, we create a new token.
    We do this because the supplied token is a token
    with a very short life span given by the
    above launch_lti_session function.
    """
    token = request.headers['Authorization'].split(' ')[1]
    lti_api_code = request.args.get('code')
    if lti_api_code:
        get_all_users_of_canvas_course_via_api(lti_api_code, token)
    access_token = create_access_token(identity=get_jwt_identity())
    return Iresponse.create_response({'access_token': access_token}, 200)


@apiBluePrint.route('lti/get_lti_params', methods=['GET'])
@lti_session_required  # This also checks for a jwt token.
def get_lti_params():
    return Iresponse.create_response(get_jwt_identity(), 200)
