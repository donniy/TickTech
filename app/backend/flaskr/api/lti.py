from . import apiBluePrint
from flask import request, redirect, jsonify, current_app
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

    expires = datetime.timedelta(minutes=1)
    lti_instance.params['in_lti'] = True
    access_token = create_access_token(identity=lti_instance.params,
                                       expires_delta=expires)
    if lti_instance.params.get('new_tiktech_course'):
        redirect_uri = current_app.config['TIKTECH_BASE_URL']
        redirect_uri += '/start_lti_instance/' + access_token
        lti_url = lti.lti_base_route + '/login/oauth2/auth?'
        lti_url += 'client_id=10000000000036&'
        lti_url += 'response_type=code&'
        lti_url += 'redirect_uri=' + redirect_uri
        return redirect(lti_url, 302)

    redirect_url = current_app.config['TIKTECH_BASE_URL']
    redirect_url += '/start_lti_instance/' + access_token
    return redirect(redirect_url)


def get_all_users_of_canvas_course_via_api(code, token, course_id):
    """
    Function that connects to the api of canvas, acting as the user.
    We can then get all the users for a course in canvas.
    """
    url = lti.lti_base_route + '/login/oauth2/token'
    redirect_uri = current_app.config['TIKTECH_BASE_URL']
    redirect_uri += '/start_lti_instance/' + token
    resp = requests.post(url, data = {
        'grant_type': 'authorization_code',
        'client_id': 10000000000036,
        'client_secret': 'XcHBV43CIqs4SZlgvFU6a2STQrF4YHGnQ26aMQiIIdNX0oCMcx3Eqpbvdqdwtrks',
        'redirect_uri': redirect_uri,
        'code': code,
        'replace_tokens': 'True',
    })
    access_token = resp.json().get('access_token')
    headers = {'Authorization': 'Bearer ' + access_token}
    lti.fill_new_course_with_canvas_data(headers, course_id)
    request_url = lti.lti_base_route + '/login/oauth2/token'
    res = requests.delete(request_url, headers=headers)



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
    lti_data = get_jwt_identity()
    custom_canvas_course_id = lti_data['custom_canvas_course_id']
    if lti_api_code:
        get_all_users_of_canvas_course_via_api(lti_api_code, token,
                                               custom_canvas_course_id)
    access_token = create_access_token(identity=get_jwt_identity())
    return Iresponse.create_response({'access_token': access_token}, 200)


@apiBluePrint.route('lti/get_lti_params', methods=['GET'])
@lti_session_required  # This also checks for a jwt token.
def get_lti_params():
    return Iresponse.create_response(get_jwt_identity(), 200)
