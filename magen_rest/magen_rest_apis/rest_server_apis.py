"""API for REST Server"""

import sys
import logging
from http import HTTPStatus

from flask.json import jsonify

from magen_logger.logger_config import LogDefaults

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class RestServerApis(object):
    """Rest Server API for Respond and Logging"""
    @staticmethod
    def respond(http_status=HTTPStatus.OK, title="Title", response=None):
        """
        This function prepares a HTTP Response object to be sent back to the client.

        :param http_status: standard http status code (int, phrase)
        :param title: app-level title of response
        :param response: dict with additional application-specific info
            : fields: success, cause, <op-specific-key>

        :return: Flask HTTP Response object
        """
        try:
            assert isinstance(http_status, HTTPStatus)  # pass HTTPStatus, not int
            resp = jsonify({'status': http_status, "title": title, "response": response})
            resp.status_code = int(http_status)
            return resp
        except Exception as err:
            print("Unexpected error: {} \n Stack Trace: {}".format(err, sys.exc_info()[0]))
            raise err

    @staticmethod
    def rest_api_log_all(app, *, logger=None, log_level=logging.DEBUG):
        """
        Log the urls supported by the supplied flask context, generally
        all the urls supported by the server/process

        :param app: flask application for this process
        :param logger: optional overide to default logger
        :param log_level: optional overide to default logger level
        :type app: Flask
        :type logger: logger
        :type log_level: logging_level
        :rtype: void
        """
        if not logger:
            logger = logging.getLogger(LogDefaults.default_log_name)
        logger.log(log_level, "REGISTERED URLS FOR PROCESS %s", app.name)
        for rule in app.url_map.iter_rules():
            logger.log(log_level, "RULE: %s %s", rule.rule, rule.methods)
