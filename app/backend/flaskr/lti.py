from . import i_request
import oauth2

"""
This file contains some of the code for lti from the following file:
https://github.com/CodeGra-de/CodeGra.de/blob/master/psef/auth.py

"""

class InvalidLTIRequest(Exception):
    pass


# TODO: add getting of secret key from consumerKey
def validate_lti_Irequest(i_req):
    """
    Function that validates a LTI request by
    recreating the signature and comparing
    this with the provided signature.
    For this we require that the LTI request
    is wrapped in a Irequest(Internal request)
    object.
    For this it uses the python3-oauth2 libary.
    source:
    https://github.com/i-kiwamu/python3-oauth2/blob/master/oauth2/__init__.py

    If the LTI request is invalid, we throw an
    InvalidLTIRequest exception and log the error.
    """
    oauth_server = oauth2.Server()
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    oauth_server.add_signature_method(signature_method)
    consumer = oauth2.Consumer('consumerKey', 'test')
    oauth_request = oauth2.Request.from_request(
        i_req.method, i_req.url, i_req.headers, i_req.body)

    try:
        oauth_server.verify_request(oauth_request, consumer, {})
    except Exception as e:
        print(e)  # debug
        raise InvalidLTIRequest


def sanitize_lti_Irequest(i_req):
    """
    Function that removes all the sensitive data
    from an LTI request.
    """
    print(i_req.body)
    for key in i_req.body.copy().keys():
        if key.startswith('oauth'):
            del i_req.body[key]


class LTI:
    def __init__(self, i_req):
        """
        Createn an LTI instance from an internal request.
        It removes all the sensitive data from the request
        and only keeps it body. However this can be adapted.
        """
        self.params = {}
        self._sanitize_lti_Irequest(i_req)

    def _sanitize_lti_Irequest(self, i_req):
        """
        Function that removes all the sensitive data
        from an LTI request.
        """
        for key in i_req.body.copy().keys():
            if key.startswith('oauth'):
                del i_req.body[key]
        self.params = i_req.body
