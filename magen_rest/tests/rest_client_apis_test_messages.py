MAGEN_SINGLE_ASSET_FINANCE_POST = """
{
  "asset": [
    {
      "name": "finance docs",
      "resource_group": "roadmap",
      "resource_id": 3,
      "client_uuid": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
      "host": "sjc-repenno-nitro10.cisco.com"
    }
  ]
}"""

MAGEN_SINGLE_ASSET_FINANCE_POST_RESP = """
{
  "response": {
    "asset": {
      "client_uuid": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
      "creation_timestamp": "2016-09-01 21:22:13.053688+00:00",
      "host": "sjc-repenno-nitro10.cisco.com",
      "name": "finance docs",
      "resource_group": "roadmap",
      "resource_id": 3,
      "uuid": "74c1c6ff-c266-43a6-9d14-82dca05cb6df",
      "version": 1
    },
    "cause": null,
    "success": true
  },
  "status": "201",
  "title": "Asset Creation"
}"""

MAGEN_SINGLE_ASSET_FINANCE_PUT = """
{
  "asset": [
    {
      "client_uuid": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
      "creation_timestamp": "2016-09-01 21:22:13.053688+00:00",
      "host": "sjc-repenno-nitro10.cisco.com",
      "name": "finance docs",
      "resource_group": "earnings",
      "resource_id": 2,
      "uuid": "74c1c6ff-c266-43a6-9d14-82dca05cb6df",
      "version": 1
    }
  ]
}"""

MAGEN_SINGLE_ASSET_FINANCE_GET_RESP = """
{
  "response": {
    "asset": [
      {
        "client_uuid": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
        "creation_timestamp": "2016-09-01T21:22:13.053000+00:00",
        "host": "sjc-repenno-nitro10.cisco.com",
        "name": "finance docs",
        "resource_group": "earnings",
        "resource_id": 2,
        "uuid": "1c43ae97-ce17-43cc-a90e-8733928ebb69",
        "version": 1
      }
    ],
    "cause": null,
    "success": true
  },
  "status": "200",
  "title": "Get Asset"
}"""

MAGEN_SINGLE_ASSET_GET_RESP_404 = """
{
  "response": {
    "asset": [],
    "cause": "Asset not found",
    "success": false
  },
  "title": "Get Asset"
}"""

MAGEN_SINGLE_ASSET_FINANCE_DELETE_RESPONSE = """
{
  "response": {
    "asset": "3bed9635-6d05-4d45-85c0-b7e0d51e1958",
    "cause": "Document deleted",
    "success": true
  },
  "title": "Delete Asset"
}"""