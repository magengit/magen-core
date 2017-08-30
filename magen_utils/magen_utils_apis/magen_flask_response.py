#! /usr/bin/python3

from flask import Response
from flask.json import jsonify

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/25/2016"


class JSONifiedResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSONifiedResponse, cls).force_type(rv, environ)
