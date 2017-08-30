#! /usr/bin/python3
from http import HTTPStatus

from flask import request, abort, Blueprint
from magen_rest_apis.rest_server_apis import RestServerApis

from magen_statistics_api.counter_metric_api import CounterAPI
from magen_statistics_server.metrics_app_rest_api import wrap_response

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__date__ = "10/24/2016"

# Source Statistics API

# Counters
#
# get /magen/{source}/v2/counters/ - Get all counters that belong to {source} !
#
# post /magen/{source}/v2/counters/ - Create counter(-s) for a {source} !
#
# delete /magen/{source}/v2/counters/ - Delete all counters that belong to {source} !
#
# get /magen/{source}/v2/counters/{flavor_type}/ - Get all counters belong to {source} of certain {flavor}
#
# delete /magen/{source}/v2/counters/{flavor_type}/ - Delete all counters of certain {flavor}
#
# post /magen/{source}/v2/counters/{flavor_type}/{flavor_opt}/ - Create counter of certain {flavor}

sourced_counters = Blueprint("sourced_counters", __name__)


@sourced_counters.route("/magen/<source>/v2/counters/", methods=["GET"])
def get_counters_by_source(source):
    """
    Get all counters that belong to {source}

    :param source: string with name of source that invoked counter creation
    :return: JSON with list of counters
    """
    counter_list = CounterAPI.get_counters_by_source(source)
    counters = wrap_response(counter_list)
    if not counters["counters"]["counter"]:
        return RestServerApis.respond(http_status=HTTPStatus.NOT_FOUND, title="Get Counters by Source", response=counters)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Get Counters by Source", response=counters)


@sourced_counters.route("/magen/<source>/v2/counters/", methods=["POST"])
def push_counters_for_source(source):
    """
    Create counter(-s) for a {source}. Creation always requires a source

    :param source: string with name of source that invoked counter creation
    :return: JSON with list of uuids
    """
    try:
        data = request.json["counters"]["counter"]
        uuid_list = list()
        for item in data:
            uuid_list.append(CounterAPI.create_counter(source, **item))
        http_response = RestServerApis.respond(
            http_status=HTTPStatus.CREATED,
            title="Post Counters for Source",
            response={"uuid": uuid_list}
        )
        http_response.headers["location"] = request.url
        return http_response
    except TypeError:
        abort(400)


@sourced_counters.route("/magen/<source>/v2/counters/", methods=["DELETE"])
def delete_counters_of_source(source):
    """
    Delete all counters that belong to {source}

    :param source: string with name of source that invoked counter creation
    :return: JSON response
    """
    CounterAPI.delete_counters(source)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Delete All Counters", response={"acknowledged": True})


@sourced_counters.route("/magen/<source>/v2/counters/<flavor>/", methods=["GET"])
def get_flavored_counters_by_source(source, flavor):
    """
    Get counters belong to {source} of certain {flavor}

    :param source: string with name of source that invoked counter creation
    :param flavor: name of flavor for a counter
    :return: JSON with list of counters
    """
    counters_list = CounterAPI.get_flavored_counters(flavor, source)
    counters = wrap_response(counters_list)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Get Flavored Counters by Source", response=counters)


@sourced_counters.route("/magen/<source>/v2/counters/<flavor>/", methods=["DELETE"])
def delete_flavored_counters(source, flavor):
    """
    Delete all counters that belong to {source} of certain {flavor}

    :param source: string with name of source that invoked counter creation
    :param flavor: name of flavor for a counter
    :return: JSON response
    """
    pass


@sourced_counters.route("/magen/<source>/v2/counters/<flavor_type>/<flavor_opt>/", methods=["POST"])
def create_flavored_counters(source, flavor_type, flavor_opt):
    """
    Create counter belong to {source} of certain {flavor}
    URI examples:
    /magen/ingestion/v2/counters/restresponse/200/
    /magen/ingestion/v2/counters/restresponse/100/
    /magen/ingestion/v2/counters/restresponse/404/ etc.

    /magen/ingestion/v2/counters/restrequest.get/
    /magen/ingestion/v2/counters/restrequest.post/ etc.

    Only one counter of certain flavor per Source!

    :param source: string with name of source that invoked counter creation
    :param flavor_type: type of flavor for a counter: restresponse or restrequest
    :param flavor_opt: opt of flavor instance: name of enum options for flavors
    :return: JSON with list of uuids
    """
    try:
        data = request.json["counters"]["counter"]
        # FIXME: Probably need to change a format of request_data
        assert len(data) == 1  # making sure that provided data contains only 1 counter_dict
        uuid_list = list()
        for item in data:
            success, c_uuid = CounterAPI.create_flavored_counter(flavor_type, source, flavor_opt, **item)
            uuid_list.append(c_uuid)
            if not success:
                http_response = RestServerApis.respond(
                    http_status=HTTPStatus.BAD_REQUEST,
                    title="Post Flavored Counters for Source",
                    response=uuid_list
                )
                http_response.headers["location"] = request.url
                return http_response
        http_response = RestServerApis.respond(
            http_status=HTTPStatus.CREATED,
            title="Post Flavored Counters for Source",
            response={"uuid": uuid_list}
        )
        http_response.headers["location"] = request.url
        return http_response
    except TypeError:
        abort(400)


@sourced_counters.route("/magen/<source>/v2/counters/<flavor_type>/<flavor_opt>/", methods=["GET"])
def get_flavored_counter_detailed(source, flavor_type, flavor_opt):
    counter = CounterAPI.get_flavored_counter_dict(flavor_type, flavor_opt)
    counter_response = wrap_response(counter)
    return RestServerApis.respond(http_status=HTTPStatus.OK, title="Get Detailed Counter", response=counter_response)
