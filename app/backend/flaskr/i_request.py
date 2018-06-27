class Irequest:
    """
    Internal request class. This is a base class so we
    can transform a request into an internal representation.
    This way we can support multiple frameworks, by just
    creating a derived class for the framework and then using
    the internal request object in all the other functions.

    The way this class is build at the moment is for easy use
    In other functions and to extract enformation from the request
    easily. This is mostly done for LTI at the moment.
    """
    def __init__(self):
        """
        @params headers: the headers of the request in a python dict.
        @params body: the body of the request in a mutable python dict.
        @params method: is the method of the request.
        @params url: the url from where the request was made.
        Below the types are displayed for the params, this typing must
        be followed.
        """
        self.headers = None  # Type: dict[str, str]
        self.body = None  # Type: dict[str, str]
        self.method = None  # Type: str
        self.url = None  # Type: str

    # TODO: Maybe add an execption to this function.
    def transform_request_to_internal_request(self, framework_request_type):
        """
        This is the function that transforms a certrain framework request type
        into our internal request type. This is done by extracting the
        following data from the request,
        encoded in the following type added to self.
        self.headers: the headers of the request in a python dict.
        self.body: the body of the request in a mutable python dict.
        self.method: is the method of the request as a str.
        self.url: the url from where the request was made as a str.
        Check the __init__ function of this class.
        """
        raise NotImplementedError


class IrequestFlask(Irequest):
    def transform_request_to_internal_request(self, flask_request):
        """
        Check parent class.
        """
        self.headers = dict(flask_request.headers)
        self.body = self._extract_body_from_request(flask_request)
        self.method = flask_request.method
        self.url = flask_request.url

    # TODO: Add support for multiple request types.
    def _extract_body_from_request(self, flask_request):
        """
        Extract the data from the flask_request.
        The data is in different places, depending on the type
        of request. Most important is that everything needed
        in the body is return in a dictionary.
        """
        if flask_request.method == "POST":
            return flask_request.form.to_dict().copy()
