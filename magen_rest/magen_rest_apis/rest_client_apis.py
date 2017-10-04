"""Rest Client APIs"""
import json
from http import HTTPStatus

import requests
import requests.exceptions
import simplejson

from magen_test_utils_apis.test_magen_object_apis import TestMagenObjectApis

from .rest_exception_apis import handle_specific_exception
from .rest_exception_apis import RestReturn

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


def known_exceptions(func):
    """
    Known Exceptions decorator.
    wraps a given function into try-except statement

    :param func: function to decorate
    :type func: Callable

    :return: decorated
    :rtype: Callable
    """
    def helper(*args, **kwargs):
        """Actual Decorator for handling known exceptions"""
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.RequestException, json.JSONDecodeError, simplejson.scanner.JSONDecodeError) as err:
            return handle_specific_exception(err)
    return helper


class RestClientApis(object):
    """APIs for handling REST Requests"""
    put_json_headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    get_json_headers = {'Accept': 'application/json'}

    @staticmethod
    @known_exceptions
    def http_get_and_check_success(url, my_function=None, verify=True, stream=False):
        """
        This function will send a GET request and check if the response is OK.

        :param stream: Whether to keep connection open in order to stream large files
        :param verify: Verify certs
        :param url: HTTP URL
        :param my_function: An optional function that performs specific application level checks. The function
            needs to returns the tuple success(boolean), message(string), return_code(int).
            The signature should be my_function(json_received as dict)

        :return: Rest Respond Object
        """
        session = requests.Session()
        get_response = session.get(url, verify=verify, stream=stream, timeout=2.0)
        get_response.raise_for_status()
        if get_response.status_code != HTTPStatus.NO_CONTENT and get_response.text:
            get_resp_json = get_response.json()
        else:
            get_resp_json = None
        if my_function:
            success, message, return_code = my_function(get_response)
        else:
            success = True
            message = get_response.reason
            return_code = get_response.status_code

        rest_return_obj = RestReturn(success=success, message=message, http_status=return_code,
                                     json_body=get_resp_json,
                                     response_object=get_response)
        return rest_return_obj

    @staticmethod
    @known_exceptions
    def http_delete_and_check_success(url, my_function=None, verify=True):
        """
        This function performs a DELETE request

        :param my_function: An optional function that performs domain specific checks aginst the delete response if any.
            The function needs to returns the tuple success(boolean), message(string), HTTPStatus(int).
            The signature should be my_function(json_received as dict)

        :param url: URL used by the POST request
        :return: Rest Respond Object
        """
        session = requests.Session()
        delete_resp = session.delete(
            url,
            verify=verify,
            stream=False,
            timeout=2.0)
        delete_resp.raise_for_status()
        if delete_resp.status_code != HTTPStatus.NO_CONTENT and delete_resp.text:
            delete_resp_json = delete_resp.json()
        else:
            delete_resp_json = None
        if my_function:
            success, message, return_code = my_function(delete_resp)
        else:
            success = True
            message = delete_resp.reason
            return_code = delete_resp.status_code
        rest_return_obj = RestReturn(success=success, message=message, http_status=return_code,
                                     json_body=delete_resp_json,
                                     response_object=delete_resp)
        return rest_return_obj

    @staticmethod
    @known_exceptions
    def http_post_and_check_success(url, json_req, my_function=None, timeout=2.0, verify=True):
        """
        This function performs a POST request and returns the json body to the caller
        for any further processing or validation

        :param timeout: Request timeout
        :param json_req: JSON to send to server
        :param url: URL used by the POST request
        :param my_function: An optional function that performs specific application level checks.
            The function needs to returns the tuple success(boolean), message(string), HTTPStatus(int).
            The signature should be my_function(json_received as dict)

        :return: Rest Respond Object
        """
        session = requests.Session()
        post_resp = session.post(
            url,
            verify=verify,
            data=json_req,
            headers=RestClientApis.put_json_headers,
            stream=False,
            timeout=timeout)

        post_resp.raise_for_status()
        # When an resource is created we need the Location header properly returned
        if 'Location' in post_resp.headers:
            if post_resp.status_code != HTTPStatus.NO_CONTENT and post_resp.text:
                post_resp_json = post_resp.json()
            else:
                post_resp_json = None
            if my_function:
                success, message, return_code = my_function(post_resp)
            else:
                success = True
                message = post_resp.reason
                return_code = post_resp.status_code
        else:
            success = False
            post_resp_json = None
            message = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
            return_code = HTTPStatus.INTERNAL_SERVER_ERROR

        rest_return_obj = RestReturn(success=success, message=message, http_status=return_code,
                                     json_body=post_resp_json,
                                     response_object=post_resp)
        return rest_return_obj

    @staticmethod
    @known_exceptions
    def http_put_and_check_success(url, json_req, my_function=None, verify=True):
        """
        This function performs a PUT request and returns the json body to the caller
        for any further processing or validation

        :param json_req: JSON to send to server
        :param url: URL used by the POST request
        :param my_function: An optional function that performs specific application level checks. The function
            needs to returns the tuple success(boolean), message(string), return_code(int). Return code must be
            on of the REST Status codes

        :return: Rest Respond Object
        """
        session = requests.Session()
        put_resp = session.put(
            url,
            verify=verify,
            data=json_req,
            headers=RestClientApis.put_json_headers,
            stream=False,
            timeout=2.0)

        put_resp.raise_for_status()
        post_resp_json = put_resp.json() if put_resp.status_code != HTTPStatus.NO_CONTENT and put_resp.text \
            else None
        if my_function:
            success, message, return_code = my_function(put_resp)
        else:
            success = True
            message = put_resp.reason
            return_code = put_resp.status_code
        rest_return_obj = RestReturn(success=success,
                                     http_status=return_code,
                                     message=message, json_body=post_resp_json)
        return rest_return_obj

    # The remaining methods in this class are for testing purposes.
    @staticmethod
    def http_get_location_header(response_obj):
        """Get Location Header for a recource"""
        return response_obj.response_object.headers['Location']

    @staticmethod
    @known_exceptions
    def http_post_and_compare_get_resp(url, json_req, json_resp, my_function=TestMagenObjectApis.compare_json,
                                       timeout=2.0):
        """
        This function performs a POST requests, extract the Location of the created magen_resource
        from the response. Then it performs a subsequent GET to check if magen_resource was created
        and checks if the response matches the expected response.

        :param timeout: Request timeout
        :param my_function: A domain specific function that validates the json expected with
            the json received from the subsequent GET request.
            The function needs to returns the tuple success(boolean), message(string), HTTPStatus(int).
            The signature should be my_function(json_expected as dict, json_received as dict)
        :param url: URL used by the POST request
        :param json_req: The JSON used in the request
        :param json_resp: The expected JSON response of the subsequent GET request
        :return: Rest Respond Object
        """
        post_resp_obj = RestClientApis.http_post_and_check_success(url, json_req, timeout=timeout)
        if post_resp_obj.success:
            # We get the HTTP Location of the subsequent GET request
            location_header = RestClientApis.http_get_location_header(post_resp_obj)
            get_response_obj = RestClientApis.http_get_and_check_success(location_header)
            if get_response_obj.success:
                json_get_resp = get_response_obj.json_body
                if json_get_resp:
                    success, message, return_code = my_function(json.loads(json_resp), json_get_resp)
                    rest_return_obj = RestReturn(success=success, http_status=return_code, message=message,
                                                 response_object=get_response_obj.response_object)
                    return rest_return_obj

                # No JSON body in server response. From the API client perspective this is a 500.
                rest_return_obj = RestReturn(success=False,
                                             message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                                             response_object=get_response_obj.response_object)
                return rest_return_obj
            # Get failed
            return get_response_obj
        # POST failed
        return post_resp_obj

    @staticmethod
    @known_exceptions
    def http_post_and_compare_resp(url, json_req, expected_post_json_resp,
                                   my_function=TestMagenObjectApis.compare_json):
        """
        This function performs a POST requests and check if the response matches the expected response.

        :param my_function: A domain specific function that validates the json expected with
            the json received from the subsequent GET request.
            The function needs to returns the tuple success(boolean), message(string), HTTPStatus(int).
            The signature should be my_function(json_expected as dict, json_received as dict)

        :param url: URL used by the POST request
        :param json_req: The JSON used in the request
        :param expected_post_json_resp: The expected JSON response of the subsequent GET request
        :return: Rest Respond Object
        """
        post_resp_obj = RestClientApis.http_post_and_check_success(url, json_req)
        if post_resp_obj.success:
            success, message, return_code = my_function(
                json.loads(expected_post_json_resp),
                post_resp_obj.json_body
            )
            rest_return_obj = RestReturn(success=success,
                                         http_status=return_code,
                                         message=message,
                                         response_object=post_resp_obj.response_object)
            return rest_return_obj
        # Post failed
        return post_resp_obj

    @staticmethod
    @known_exceptions
    def http_get_and_compare_resp(url, expected_get_json_resp, my_function=TestMagenObjectApis.compare_json):
        """
        Given a URL it performs a GET and checks if response matches expected response

        :param my_function: A domain specific function that validates the json expected with
            the json received from GET request.
            The function needs to returns the tuple success(boolean), message(string), HTTPStatus(int).
            The signature should be my_function(json_expected as dict, json_received as dict)

        :param url: URL of GET request
        :param expected_get_json_resp: expected JSON response
        :return: Rest Respond Object
        """
        get_resp_obj = RestClientApis.http_get_and_check_success(url)
        if get_resp_obj.success:
            get_resp_json = get_resp_obj.json_body
            success, message, return_code = my_function(json.loads(expected_get_json_resp), get_resp_json)
        else:
            return get_resp_obj

        rest_return_obj = RestReturn(success=success, message=message, http_status=return_code,
                                     json_body=get_resp_json,
                                     response_object=get_resp_obj.response_object)
        return rest_return_obj


    @staticmethod
    @known_exceptions
    def http_delete_and_get_check(url):
        """
        This function will delete a magen_resource and send a GET request and check if magen_resource was actually
        deleted. This is more of a test function since if server said something was deleted, it should have,
        otherwise server isbuggy.

        :param url: HTTP URL
        :type url: str
        :return: Rest Respond Object
        """
        delete_resp_obj = RestClientApis.http_delete_and_check_success(url)
        json_body = delete_resp_obj.json_body
        response_object = delete_resp_obj.response_object
        if delete_resp_obj.success:
            # if delete was successful
            get_resp_obj = RestClientApis.http_get_and_check_success(url)
            response_object = get_resp_obj.response_object
            json_body = get_resp_obj.json_body
            if get_resp_obj.http_status == HTTPStatus.NOT_FOUND:
                # if resource was not found we are good
                success = True
                return_code = HTTPStatus.OK
                message = HTTPStatus.OK.phrase
            else:
                success = False
                return_code = HTTPStatus.INTERNAL_SERVER_ERROR
                message = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
        else:
            success = False
            return_code = delete_resp_obj.http_status
            message = delete_resp_obj.message
        rest_return_obj = RestReturn(success=success, message=message, http_status=return_code,
                                     json_body=json_body, response_object=response_object)
        return rest_return_obj

    @staticmethod
    @known_exceptions
    def http_put_and_compare_get_resp(url, json_req, json_resp, my_function=TestMagenObjectApis.compare_json):
        """
        This function performs a PUT requests, performs a subsequent GET to check if magen_resource was created/updated
        and checks if the response matches the expected response.

        :param my_function: A domain specific function that validates the json expected with
            the json received from the subsequent GET request.
            The function needs to returns the tuple success(boolean), message(string), HTTPStatus(int).
            The signature should be my_function(json_expected as dict, json_received as dict)

        :param url: URL used by the PUT request
        :param json_req: The JSON used in the request
        :param json_resp: The expected JSON response of the subsequent GET request
        :return: Rest Respond Object
        """
        put_resp_obj = RestClientApis.http_put_and_check_success(url, json_req)
        if put_resp_obj.success:
            get_response_obj = RestClientApis.http_get_and_check_success(url)
            if get_response_obj.success:
                json_get_resp = get_response_obj.json_body
                if json_get_resp:
                    success, message, return_code = my_function(json.loads(json_resp), json_get_resp)
                    rest_return_obj = RestReturn(success=success,
                                                 http_status=return_code,
                                                 message=message,
                                                 response_object=get_response_obj.response_object)
                    return rest_return_obj

                # No JSON body in server response. From the API client perspective this is a 500.
                rest_return_obj = RestReturn(success=False,
                                             message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                                             response_object=get_response_obj.response_object)
                return rest_return_obj
            # Get failed
            return get_response_obj
        # POST failed
        return put_resp_obj

    @staticmethod
    @known_exceptions
    def http_put_and_compare_resp(url, json_req, json_resp, my_function=TestMagenObjectApis.compare_json):
        """
        This function performs a PUT requests, checks if the response matches the expected response.

        :param my_function: A domain specific function that validates the json expected with
            the json received from the subsequent GET request.
            The function needs to returns the tuple success(boolean), message(string), HTTPStatus(int).
            The signature should be my_function(json_expected as dict, json_received as dict)

        :param url: URL used by the PUT request
        :param json_req: The JSON used in the request
        :param json_resp: The expected JSON response of the PUT request
        :return: Rest Respond Object
        """
        put_resp_obj = RestClientApis.http_put_and_check_success(url, json_req)
        if put_resp_obj.success:
            json_put_resp = put_resp_obj.json_body
            if json_put_resp:
                success, message, return_code = my_function(json.loads(json_resp), json_put_resp)
                rest_return_obj = RestReturn(success=success,
                                             http_status=return_code,
                                             message=message,
                                             response_object=put_resp_obj.response_object)
                return rest_return_obj

            # No JSON body in server response. From the API client perspective this is a 500.
            rest_return_obj = RestReturn(success=False,
                                         message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase)
            return rest_return_obj
        # PUT failed
        return put_resp_obj
