#! /usr/bin/python3

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"

SINGLE_COUNTER_DICT = {
    "name": "asset_creation",
    "period": 60
}

SINGLE_COUNTER_CREATED_DETAILED_DICT = {
    'source': 'magen_stats_test',
    'period': 60,
    'flavor': None,
    'abs_value': 0,
    'name': 'asset_creation',
    'namespace': 'Metric.Counter',
    'alerts': False
    # 'uuid': '18e5a30e-ea4f-48af-ac66-d38810f3e69c' uuid is not included
}

SINGLE_FLAVORED_COUNTER_UNNAMED_DICT = {
    "period": 60,
    "alerts": True,
    "flavor": "RestResponse.Continue"
}

SINGLE_FLAVORED_COUNTER_UNNAMED_CREATED_DICT = {
    'flavor_opt': 'Continue',
    'abs_value': 0,
    'flavor': 'RestResponse',
    # 'uuid': 'c7db57c9-ce50-4836-a46f-8ee015b721f2', uuid is not included
    'name': 'magen_stats_test.RestResponse.Continue'
}

SINGLE_FLAVORED_COUNTER_UNNAMED_CREATED_DETAILED_DICT = {
    'flavor_opt': 'Continue',
    'flavor': 'RestResponse',
    'period': 60,
    # 'uuid': '755952c0-e83d-49dd-8587-a54bde96bf56', uuid is not included
    'namespace': 'Metric.Counter',
    'alerts': True, 'abs_value': 0,
    'source': 'magen_stats_test',
    'name': 'magen_stats_test.RestResponse.Continue'
}

FLAVOR_REST_RESPONSE_TYPE = "RestResponse"
FLAVOR_REST_RESPONSE_OPT = "NOT_FOUND"

SINGLE_REST_RESPONSE_COUNTER_DICT = {
    "period": 60,
    "alerts": True,
    "flavor": FLAVOR_REST_RESPONSE_TYPE + "." + FLAVOR_REST_RESPONSE_OPT,
    "name": "asset_access"
}

SINGLE_REST_RESPONSE_COUNTER_CREATED_DETAILED_DICT = {
    'source': 'magen_stats_test',
    'abs_value': 0,
    'namespace': 'Metric.Counter',
    'flavor_opt': 'Not Found',
    # 'uuid': '61f5249c-fae7-49a7-9506-b0cf81a96faf',
    'alerts': True,
    'name': 'asset_access',
    'flavor': 'RestResponse',
    'period': 60
}

FLAVOR_REST_REQUEST_TYPE = "RestRequest"
FLAVOR_REST_REQUEST_OPT = "GET"

SINGLE_REST_REQUEST_COUNTER_DICT = {
    "period": 60,
    "alerts": True,
    "flavor": FLAVOR_REST_REQUEST_TYPE + "." + FLAVOR_REST_REQUEST_OPT,
    "name": "asset_get"
}

SINGLE_REST_REQUEST_COUNTER_CREATED_DICT = {
    'flavor': 'RestRequest',
    # 'uuid': 'e5006be1-7fae-4686-98b0-2ec3d7ad6789',
    'name': 'asset_get',
    'flavor_opt': 'GET',
    'abs_value': 0
}

SINGLE_REST_REQUEST_COUNTER_CREATED_DETAILED_DICT = {
    # 'uuid': '7669c7a5-5a33-4180-a2bf-3618d0452b30',
    'alerts': True,
    'source': 'magen_stats_test',
    'name': 'asset_get',
    'flavor': 'RestRequest',
    'namespace': 'Metric.Counter',
    'abs_value': 0,
    'flavor_opt': 'GET',
    'period': 60
}

MULTIPLE_COUNTERS_CREATED_LIST = [{
    'abs_value': 0,
    'name': 'asset_creation'
    # 'uuid': 'ad5db976-b0c4-4255-9243-d950b07c947a'
}, {
    'abs_value': 0,
    'flavor_opt': 'GET',
    'name': 'asset_get',
    'flavor': 'RestRequest'
    # 'uuid': 'ce32f40b-128b-4a69-a5ae-36dd3a5d61a2'
}, {
    'abs_value': 0,
    'flavor_opt': 'Not Found',
    'name': 'asset_access',
    'flavor': 'RestResponse'
    # 'uuid': '41d01740-a110-4ebe-a9d0-231a0192c49f'
}]
