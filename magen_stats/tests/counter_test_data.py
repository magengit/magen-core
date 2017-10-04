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

SINGLE_COUNTER_POST_RESP = """{
    "response": {
        "metric_uuid": [
            "dd1908ed-378c-464c-8557-df331c06bf79"
        ]
    },
    "status": 201,
    "title": "Post Counters for Source"
}"""

SINGLE_COUNTER_RESTRESP_POST_RESP = """{
    "response": {
        "metric_uuid": [
            "19fb449a-a62f-40ea-82ea-cd984b02e929"
        ]
    },
    "status": 201,
    "title": "Post Flavored Counters for Source"
}"""

SINGLE_COUNTER_FLAVORED_POST_RESP = """{
    "response": {
    "metric_uuid": [
        "1e5ca0da-47d5-42bb-8cf6-2ece162edb79"
        ]
    },
    "status": 201,
    "title": "Post Counters for Source"
}"""

MULTIPLE_COUNTERS_POST_RESP = """{
    "response": {
    "metric_uuid": [
        "986fd851-8ef0-49b5-8466-4a585015dc9c",
        "2e808077-e3cf-4369-8cdf-11d1ecb2b108"
        ]
    },
    "status": 201,
    "title": "Post Counters for Source"
}"""

SINGLE_COUNTER_GET_RESP = """{
  "response": {
    "counters": {
      "counter": [
        {
          "abs_value": 0,
          "name": "asset_creation",
          "metric_uuid": "547534e1-e606-44bb-a15a-71e82a947dad"
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
          "metric_uuid": "895859fc-d26b-4215-88e0-e2805a6ef134"
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
          "metric_uuid": "14931f38-aa13-46bc-a962-d477b5a8c4fc"
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
          "name": "asset_creation",
          "metric_uuid": "d9056542-ea33-40c9-8028-5e7f6eba1ff2"
        },
        {
          "abs_value": 0,
          "flavor": "RestRequest",
          "flavor_opt": "DELETE",
          "name": "asset_deletion",
          "metric_uuid": "e959ae3b-d2be-40f5-99b6-2503745b419a"
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
          "metric_uuid": "412bd442-4e4a-49fa-b191-ef326cdfbdb7"
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
          "metric_uuid": "a9c9d7d9-ea10-455a-bc6e-ba5ebf17d5d5"
        }
      ]
    }
  },
  "status": 200,
  "title": "Get Flavored Counters by Source"
}"""
