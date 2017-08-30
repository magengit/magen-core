import json
import logging
import sys
from functools import singledispatch
from http import HTTPStatus

import requests
import requests.exceptions

from magen_logger.logger_config import LogDefaults
from magen_utils_apis.singleton_meta import Singleton

from .rest_return_api import RestReturn


__author__ = "repennor@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

# logger_config_instance = LogDefaults.get_instance()
# logger = logging.getLogger(logger_config_instance.default_log_name)


class RestExceptionApis(metaclass=Singleton):

    logger = logging.getLogger(LogDefaults.default_log_name)

    @singledispatch
    def handle_specific_exception(e):
        """
        Handles exceptions for the REST APIs functions. This function is overloaded with specific functions
        for the most important types of exceptions

        :return: Rest return object
        """
        RestExceptionApis.logger.error('Unexpected Error. Error: %s', sys.exc_info()[0])
        success = False
        message = e.args[0]
        http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        rest_return_obj = RestReturn(success=success, message=message, http_status=http_status,
                                     json_body=None,
                                     response_object=None)
        return rest_return_obj

    @handle_specific_exception.register(requests.exceptions.HTTPError)
    def _(e):
        success = False
        http_status = e.response.status_code
        message = e.response.reason
        json_body = e.response.json()
        RestExceptionApis.logger.error(
            'HTTP Error. Error: %s', http_status)
        rest_return_obj = RestReturn(success=success, message=message,
                                     http_status=http_status, json_body=json_body,
                                     response_object=e.response)
        return rest_return_obj

    @handle_specific_exception.register(requests.exceptions.ReadTimeout)
    @handle_specific_exception.register(requests.exceptions.ConnectTimeout)
    def _(e):
        RestExceptionApis.logger.error(
            'Server too slow. Error: %s', e)
        success = False
        message = HTTPStatus.SERVICE_UNAVAILABLE.phrase
        http_status = HTTPStatus.SERVICE_UNAVAILABLE
        rest_return_obj = RestReturn(success=success, message=message,
                                     http_status=http_status, json_body=None, response_object=None)
        return rest_return_obj

    @handle_specific_exception.register(requests.exceptions.ConnectionError)
    def _(e):
        RestExceptionApis.logger.error('ConnectionError. Error: %s', e)
        success = False
        message = HTTPStatus.SERVICE_UNAVAILABLE.phrase
        http_status = HTTPStatus.SERVICE_UNAVAILABLE
        rest_return_obj = RestReturn(success=success, message=message,
                                     http_status=http_status, json_body=None, response_object=None)
        return rest_return_obj

    @handle_specific_exception.register(requests.exceptions.InvalidSchema)
    def _(e):
        RestExceptionApis.logger.error(
            'InvalidSchema. Error: %s', e)
        success = False
        message = HTTPStatus.BAD_REQUEST.phrase
        http_status = HTTPStatus.BAD_REQUEST
        rest_return_obj = RestReturn(success=success, message=message,
                                     http_status=http_status, json_body=None, response_object=None)
        return rest_return_obj

    @handle_specific_exception.register(json.JSONDecodeError)
    def _(e):
        RestExceptionApis.logger.error(
            'JSONDecodeError. Error: %s', e)
        success = False
        message = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
        http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        rest_return_obj = RestReturn(success=success, message=message,
                                     http_status=http_status, json_body=None, response_object=None)
        return rest_return_obj
