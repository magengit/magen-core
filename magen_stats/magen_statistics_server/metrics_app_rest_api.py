#! /usr/bin/python3
from http import HTTPStatus

from flask import Blueprint

from magen_rest_apis.rest_server_apis import RestServerApis
from magen_statistics_api.metric import MetricsCollections
from magen_statistics_api.counter_metric_api import CounterAPI

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"


metrics_collections = MetricsCollections()

metrics = Blueprint("metrics", __name__)

# General Statistics API

# Counters
#
# get /magen/v2/counters/ - Get all counters in the system !
#
# delete /magen/v2/counters/ - Delete all counters in the system !
#
# get /magen/v2/counters/{flavor}/ - Get all counters of certain flavor
#
# get /magen/v2/counters/{uuid}/ - Get a counter full info
#
# delete /magen/v2/counters/{uuid}/ - Delete one counter
#
# put /magen/v2/counters/{uuid}/ - Update one counter
#


def wrap_response(counters):
    """
    Wraps response with fields according to REST

    :param counters: dict or list of counters
    :rtype: dict of wrapped data
    """
    if isinstance(counters, dict):
        result_counters = [counters]
    elif isinstance(counters, list):
        result_counters = counters
    else:
        return False
    return {
        "counters": {
            "counter": result_counters
        }
    }


@metrics.route("/magen/v2/counters/", methods=["GET"])
def get_counters():
    """
    Get all counters in the system

    :return: JSON with list of counters
    :rtype: RestServerApis obj
    """
    counters_list = CounterAPI.get_all_counters()
    counters = wrap_response(counters_list)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Get All Counters", response=counters)


@metrics.route("/magen/v2/counters/", methods=["DELETE"])
def delete_counters():
    """
    Delete all counters in the system
    :return: JSON response
    """
    CounterAPI.delete_counters()
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Delete All Counters", response={"acknowledged": True})


@metrics.route("/magen/v2/counters/<flavor>/", methods=["GET"])
def get_counters_by_flavor(flavor):
    """
    Get all counters of certain flavor

    :param flavor: name of flavor for a counter
    :return: JSON with list of counters
    :rtype: RestServerApis obj
    """
    counters_list = CounterAPI.get_flavored_counters(flavor)
    counters = wrap_response(counters_list)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Get Flavored Counters", response=counters)


@metrics.route("/magen/v2/counters/<uuid>/", methods=["GET"])
def get_counter_detailed(uuid):
    """
    Get a counter full info

    :param uuid: string uuid of counter
    :return: JSON with counter dict
    :rtype: RestServerApis obj
    """
    counter = CounterAPI.get_counter(uuid)
    counter_response = wrap_response(counter)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Get Detailed Counter", response=counter_response)


@metrics.route("/magen/v2/counters/<uuid>/", methods=["DELETE"])
def delete_one_counter(uuid):
    """
    Delete one counter

    :param uuid: string uuid of counter
    :return: JSON response
    :rtype: RestServerApis obj
    """
    CounterAPI.delete_counter(uuid)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Delete One Counter", response={"acknowledged": True})


@metrics.route("/magen/v2/counters/<uuid>/", methods=["PUT"])
def update_one_counter(uuid):
    """
    Update one counter

    :param uuid: string uuid of counter
    :return: JSON response
    :rtype: RestServerApis obj
    """
    pass
