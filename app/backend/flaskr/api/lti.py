from . import apiBluePrint
from flask import request
from flaskr.i_request import *
from flaskr import lti


@apiBluePrint.route('lti/launch', methods=['POST'])
def launch_lti_session():
    i_req = IrequestFlask()
    i_req.transform_request_to_internal_request(request)
    try:
        lti.validate_lti_Irequest(i_req)
    except lti.InvalidLTIRequest:
        return "Invalid LTI request, check your key and secret."

    lti_instance = lti.LTI(i_req)
    print(lti_instance.params)
    return "LTI SUCCES"
