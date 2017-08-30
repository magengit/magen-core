#! /usr/bin/python3

__author__ = "Alena Lifar"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__email__ = "alifar@cisco.com"
__date__ = "10/24/2016"

SINGLE_COUNTER_DATA = """{
    "counters": {
        "counter": [{
            "name": "asset_creation",
            "period": 60
        }
        ]
    }
}"""

SINGLE_COUNTER_GET_RESP = """{
  "response": {
    "counters": {
      "counter": [
        {
          "abs_value": 0,
          "name": "asset_creation",
          "uuid": "547534e1-e606-44bb-a15a-71e82a947dad"
        }
      ]
    }
  },
  "status": 200,
  "title": "Get Counters by Source"
}"""

SINGLE_OK_COUNTER_GET_RESP = """{
  "response": {
    "counters": {
      "counter": [
        {
          "abs_value": 0,
          "alerts": false,
          "flavor": "RestResponse",
          "flavor_opt": "OK",
          "name": "asset_creation",
          "namespace": "Metric.Counter",
          "period": 60,
          "source": "ingestion",
          "uuid": "895859fc-d26b-4215-88e0-e2805a6ef134"
        }
      ]
    }
  },
  "status": 200,
  "title": "Get Detailed Counter"
}"""

SINGLE_COUNTER_DATA_NOT_FOUND = """{
"counters": {
    "counter": [ {
    "name": "asset_access",
    "period": 60,
    "flavor": "RestResponse.NOT_FOUND"
    }]}
}"""

SINGLE_NOT_FOUND_COUNTER_GET_RESP = """{
  "response": {
    "counters": {
      "counter": [
        {
          "abs_value": 0,
          "flavor": "RestResponse",
          "flavor_opt": "Not Found",
          "name": "asset_access",
          "uuid": "14931f38-aa13-46bc-a962-d477b5a8c4fc"
        }
      ]
    }
  },
  "status": 200,
  "title": "Get Counters by Source"
}"""

MULTIPLE_COUNTERS_DATA = """{
"counters": {
    "counter": [ {
    "name": "asset_creation",
    "period": 60
    },{
    "name": "asset_deletion",
    "flavor": "RestRequest.Delete"
    }]}
}"""

MULTIPLE_COUNTERS_GET = """{
  "response": {
    "counters": {
      "counter": [
        {
          "abs_value": 0,
          "flavor": "RestRequest",
          "flavor_opt": "DELETE",
          "name": "asset_deletion",
          "uuid": "e959ae3b-d2be-40f5-99b6-2503745b419a"
        },
        {
          "abs_value": 0,
          "name": "asset_creation",
          "uuid": "d9056542-ea33-40c9-8028-5e7f6eba1ff2"
        }
      ]
    }
  },
  "status": 200,
  "title": "Get Counters by Source"
}"""

DETAILED_SINGLE_COUNTER_RESPONSE = """{
  "response": {
    "counters": {
      "counter": [
        {
          "abs_value": 0,
          "alerts": false,
          "flavor": "RestResponse",
          "flavor_opt": "OK",
          "name": "asset_creation",
          "namespace": "Metric.Counter",
          "period": 60,
          "source": "ingestion",
          "uuid": "412bd442-4e4a-49fa-b191-ef326cdfbdb7"
        }
      ]
    }
  },
  "status": 200,
  "title": "Get Detailed Counter"
}"""

REST_REQUEST_COUNTERS_RESPONSE = """{
  "response": {
    "counters": {
      "counter": [
        {
          "abs_value": 0,
          "flavor": "RestRequest",
          "flavor_opt": "DELETE",
          "name": "asset_deletion",
          "uuid": "a9c9d7d9-ea10-455a-bc6e-ba5ebf17d5d5"
        }
      ]
    }
  },
  "status": 200,
  "title": "Get Flavored Counters by Source"
}"""
