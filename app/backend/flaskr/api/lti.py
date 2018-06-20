from . import apiBluePrint
import oauth2
from flask import jsonify, request, escape


@apiBluePrint.route('lti/launch', methods=['POST'])
def launch_lti_session():
    params = {}
    # oauth2 cant have an immutable dict.
    is_valid_oauth(dict(request.headers), request.form.to_dict().copy(),
                   request.url, request.method)
    return "WORKED"



def is_valid_oauth(headers, body, url, method):
    oauth_server = oauth2.Server()
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    oauth_server.add_signature_method(signature_method)
    consumer = oauth2.Consumer('consumerKey', 'test')
    print(consumer)
    oauth_request = oauth2.Request.from_request(
                method, url, headers=headers, parameters=body
    )
    oauth_server.verify_request(oauth_request, consumer, {})
