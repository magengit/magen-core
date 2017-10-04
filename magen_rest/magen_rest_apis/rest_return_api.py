"""Rest Return Class"""
from http import HTTPStatus

__author__ = "repennor@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class RestReturn(object):
    """
    This class encapsulates API return to clients.
    """

    def __init__(self, success=False, message=None,
                 http_status=HTTPStatus.INTERNAL_SERVER_ERROR, json_body=None,
                 response_object=None):
        super().__init__()
        self.__success = success
        self.__message = message
        self.__http_status = http_status
        self.__json_body = json_body
        self.__response_object = response_object

    @property
    def success(self):
        """
        Returns whether the REST API or successful

        :return: boolean
        """
        return self.__success

    @success.setter
    def success(self, value):
        self.__success = value

    @property
    def message(self):
        """
        Returns a descriptive message back to the API client

        :return: string
        """
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

    @property
    def http_status(self):
        """
        Returns HTTPStatus back to client

        :return: HTTPStatus
        """
        return self.__http_status

    @http_status.setter
    def http_status(self, value):
        self.__http_status = value

    @property
    def json_body(self):
        """
        Returns the JSON body of the response from the server to the client

        :return: JSON object, a.k.a, dict
        """
        return self.__json_body

    @json_body.setter
    def json_body(self, value):
        self.__json_body = value

    @property
    def response_object(self):
        """
        Returns a Response object (see requests Python package) to the client

        :rtype: RestReturn object
        """
        return self.__response_object

    @response_object.setter
    def response_object(self, value):
        self.__response_object = value

    def to_dict(self):
        """Cast Object to Dictionary"""
        return {"success": self.success, "message": self.message, "http_status": self.http_status,
                "json": self.json_body, "response": self.response_object}
