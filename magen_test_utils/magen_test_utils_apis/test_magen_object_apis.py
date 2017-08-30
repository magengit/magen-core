import itertools
import re
from datetime import datetime
from http import HTTPStatus

import aniso8601

from magen_utils_apis.datetime_api import SimpleUtc

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class TestMagenObjectApis:
    """
    This class has APIs that normally should be used when creating unit tests
    """

    @staticmethod
    def magen_ordered(obj):
        """
        This function flattens a Magen Python object into a ordered list.

        :param obj: Python object such as a dict
        :return: A sorted Python list
        """
        if isinstance(obj, dict):
            tlist = []
            for k, v in obj.items():
                if k == "cookie" and isinstance(v, str) and len(v) > 0:
                    tlist.append((k, "valid cookie string len > 0"))
                elif k == "_id":
                    tlist.append((k, "OID"))
                elif k == "policy_sessions" and len(v) == 1:
                    tlist.append((k, "valid ps list len == 1"))
                # We should only abstract the PI list check if there are
                # actually references in the list. Otherwise we get a false
                # negative where one response might have PI_list = [] and another
                # PI_list = [<some uuids..>].
                elif (k == "PI_list" or k == "policy_instances") and len(v) > 0:
                    tlist.append((k, "valid PI list"))
                # elif k == "uuid" and expected_uuid:
                #     tlist.append((k, expected_uuid))
                # elif k == "uuid" and isinstance(v, str) and len(v) > 20:
                #     tlist.append((k, "UUID will match"))
                # elif k == "uuid" and isinstance(v, list):
                #     tlist.append((k, "UUID will match"))
                elif k == "uuid":
                    tlist.append((k, "UUID will match"))
                elif k == "resource_id" and isinstance(v, str):
                    tlist.append((k, "magen_resource UUID will match"))
                elif k == "policy_contract_uuid" and isinstance(v, str):
                    tlist.append((k, "contract UUID will match"))
                elif k == "policy_template_uuid" and isinstance(v, str):
                    tlist.append((k, "template UUID will match"))
                elif k == "pi_uuid":
                    tlist.append((k, "PI_UUID will match"))
                elif k == "iv" and isinstance(v, str) and len(v) > 0:
                    tlist.append((k, "dynamic iv"))
                elif k == "key" and isinstance(v, str):
                    tlist.append((k, "dynamic iv"))
                elif k == "key_id":
                    tlist.append((k, "dynamic key"))
                elif re.search("timestamp", k):
                    # checking that timestamps are < now
                    now = datetime.utcnow().replace(tzinfo=SimpleUtc())
                    if " " in v:
                        timestamp = aniso8601.parse_datetime(v, delimiter=" ")
                        timestamp = timestamp.replace(tzinfo=SimpleUtc())
                    elif "T" in v:
                        timestamp = aniso8601.parse_datetime(v)
                        timestamp = timestamp.replace(tzinfo=SimpleUtc())
                    else:
                        raise ValueError("Format of the Data is not acceptable")
                    # make sure event timestamps are just in the past
                    if timestamp < now:
                        tlist.append((k, "valid timestamp"))
                    else:
                        tlist.append((k, TestMagenObjectApis.magen_ordered(v)))
                else:
                    tlist.append((k, TestMagenObjectApis.magen_ordered(v)))
            return sorted(tlist)
        if isinstance(obj, list):
            return sorted(TestMagenObjectApis.magen_ordered(x) for x in obj)
        else:
            return obj

    @staticmethod
    def deep_check_ordered(expected, received):
        """
        This function compares two Python objects ordered by the magen_ordered function

        :param expected: Expected Magen Python Ordered obj
        :param received: Received Magen Python Ordered obj

        :rtype: boolean
        """
        if isinstance(expected, dict) and isinstance(received, dict):
            z = itertools.zip_longest(expected.items(), received.items())
            success = True
            for (kv1, kv2) in z:
                success = success and TestMagenObjectApis.deep_check_ordered(kv1, kv2)
            return success
        elif isinstance(expected, list) and isinstance(received, list):
            z = itertools.zip_longest(expected, received)
            success = True
            for (kv1, kv2) in z:
                success = success and TestMagenObjectApis.deep_check_ordered(kv1, kv2)
            return success
        elif isinstance(expected, tuple) and isinstance(received, tuple):
            # Note: if this is a useful function, we could pass in the tuple
            # comparison function as an argument
            if len(expected) == 2 and len(received) == 2:
                k1, v1 = expected
                k2, v2 = received
                if k1 != k2:
                    # print("k1 != k2", k1,k2)
                    return False
                else:
                    if k1 == "renewal" or k1 == "expiration":
                        now = datetime.utcnow().replace(tzinfo=SimpleUtc())
                        # normalize v2: expiration times can be either
                        # a) with 'T' or ' ', b) tzinfo (+00.00) or not.
                        # Note: should it be consistent?
                        received_time = aniso8601.parse_datetime(
                            v2.replace(' ', 'T')).replace(tzinfo=SimpleUtc())
                        # make sure renewal and expiration timestamps are at least
                        # a few seconds in the future
                        return received_time > now
                    elif k1 == "revalidation":
                        # make sure they are the same for now
                        return v1 == v2
                    else:
                        # make sure rest is equal using the same recursive check
                        return TestMagenObjectApis.deep_check_ordered(v1, v2)
            else:
                return False
        else:
            return expected == received

    @staticmethod
    def compare_json(json_expected, json_received):
        """
        This function takes two Python objects representing JSON objects, orders  and compares them.

        :param json_expected: A Python object representing the expected JSON object
        :param json_received: A Python object representing the received JSON object

        :rtype: boolean
        """
        json_expected_magen_ordered = TestMagenObjectApis.magen_ordered(json_expected)
        json_received_magen_ordered = TestMagenObjectApis.magen_ordered(json_received)
        if TestMagenObjectApis.deep_check_ordered(
                json_expected_magen_ordered,
                json_received_magen_ordered):
            return True, HTTPStatus.OK.phrase, HTTPStatus.OK
        else:
            print("\n =>Check not successful")
            print("\n Original: \n")
            print(json_expected_magen_ordered)
            print("\n Received \n")
            print(json_received_magen_ordered)
            return False, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR

