"""Mongo Return Class for structural Response"""
__author__ = "repennor@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MongoReturn(object):
    """
    This class encapsulates API return to clients.
    """

    def __init__(self, success=False, message=None, code=0, count=0, matched_count=0, documents=None,
                 response_object=None, db_exception=None):
        super().__init__()
        self.__success = success
        self.__message = message
        self.__code = code
        self.__count = count
        self.__matched_count = matched_count
        self.__documents = documents or list()
        self.__response_object = response_object
        self.__db_exception = db_exception

    @property
    def code(self):
        """
        Returns the Mongo status Code

        :rtype: boolean
        """
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = value

    @property
    def success(self):
        """
        Returns whether the Mongo API or successful

        :rtype: boolean
        """
        return self.__success

    @success.setter
    def success(self, value):
        self.__success = value

    @property
    def message(self):
        """
        Returns a descriptive message back to the API client

        :rtype: string
        """
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

    @property
    def matched_count(self):
        """
        Returns Number of documents matched back to client

        :rtype: int
        """
        return self.__matched_count

    @matched_count.setter
    def matched_count(self, value):
        self.__matched_count = value

    @property
    def count(self):
        """
        Returns Number of documents back to client

        :rtype: int
        """
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value

    @property
    def documents(self):
        """
        Returns the JSON body of the response from the server to the client

        :return: JSON object
        :rtype: dict
        """
        return self.__documents

    @documents.setter
    def documents(self, value):
        self.__documents = value

    @property
    def response_object(self):
        """
        Returns a Response object (see requests Python package) to the client

        :rtype: void
        """
        return self.__response_object

    @response_object.setter
    def response_object(self, value):
        self.__response_object = value

    @property
    def db_exception(self):
        """
        If an exception occurred and we caught it we return it here.

        :rtype: void
        """
        return self.__db_exception

    @db_exception.setter
    def db_exception(self, value):
        self.__db_exception = value

    def to_dict(self):
        """Cast Object to Dictionary"""
        return {"success": self.success, "message": self.message, "code": self.code, "count": self.count,
                "matched_count": self.matched_count, "json": self.documents, "response": self.response_object}
