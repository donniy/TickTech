from . import apiBluePrint
from flask import request
from flaskr.i_request import *
from flaskr import lti


@apiBluePrint.route('lti/launch', methods=['POST'])
def launch_lti_session():
    i_req = IrequestFlask()
    i_req.transform_request_to_internal_request(request)
    try:
        lti_instance = lti.LTI_instance(i_req)
    except lti.InvalidLTIRequest:
        return "Invalid LTI request, check your key and secret."
    return "LTI SUCCES"
