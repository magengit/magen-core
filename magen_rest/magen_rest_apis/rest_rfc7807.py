
__author__ = "repennor@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class RestRfc7807(object):
    """
    This class should be used to construct RFC7807 responses to be included
    in HTTP responses.

    o  "type" (string) - A URI reference [RFC3986] that identifies the
      problem type.  This specification encourages that, when
      dereferenced, it provide human-readable documentation for the
      problem type (e.g., using HTML [W3C.REC-html5-20141028]).  When
      this member is not present, its value is assumed to be
      "about:blank".

    o  "title" (string) - A short, human-readable summary of the problem
      type.  It SHOULD NOT change from occurrence to occurrence of the
      problem, except for purposes of localization (e.g., using
      proactive content negotiation; see [RFC7231], Section 3.4).

    o  "status" (number) - The HTTP status code ([RFC7231], Section 6)
      generated by the origin server for this occurrence of the problem.

    o  "detail" (string) - A human-readable explanation specific to this
      occurrence of the problem.

    o  "instance" (string) - A URI reference that identifies the specific
      occurrence of the problem.  It may or may not yield further
      information if dereferenced.
    """

    def to_dict(self):
        """
        This function serializes the object into a Python dict so it can be encoded to a JSON string. It should be
        used with the json.dumps() function as the option "default=RestRfc7807.to_dict". See tests for examples

        :param o: object to be serialized

        :return:a dict of the object's fields
        """
        return {"type_uri": self.type_uri, "title": self.title, "status": self.status, "detail": self.detail,
                "instance": self.instance}

    def __init__(self, type_uri=None, title=None, status=None, detail=None, instance=None):
        self.__type_uri = type_uri
        self.__title = title
        self.__status = status
        self.__detail = detail
        self.__instance = instance

    @property
    def type_uri(self):
        """URI Type"""
        return self.__type_uri

    @type_uri.setter
    def type_uri(self, value):
        self.__type_uri = value

    @property
    def title(self):
        """Title"""
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def status(self):
        """Status"""
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def detail(self):
        """Detail"""
        return self.__detail

    @detail.setter
    def detail(self, value):
        self.__detail = value

    @property
    def instance(self):
        """Singleton instance"""
        return self.__instance

    @instance.setter
    def instance(self, value):
        self.__instance = value
