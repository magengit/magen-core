from datetime import tzinfo, timedelta

import aniso8601

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class SimpleUtc(tzinfo):

    def dst(self, dt):
        pass

    def tzname(self, **kwargs):
        return "UTC"

    def utcoffset(self, dt):
        return timedelta(0)


def datetime_utc_parse(str_timedate):
    if 'T' in str_timedate:
        timestamp = aniso8601.parse_datetime(str_timedate)
    elif ' ' in str_timedate:
        timestamp = aniso8601.parse_datetime(str_timedate, delimiter=" ")
    else:
        raise SyntaxError("Date format is not allowed")
    return timestamp


# FIXME: I think the function above should just be a parse wrapping function
# and this function should be called to convert a string to a UTC datetime object
def datetime_parse_iso8601_string_to_utc(str_timedate):
    parsedTime = datetime_utc_parse(str_timedate)
    # Check if string contains proper timezone
    if parsedTime.utcoffset() == None:
        raise SyntaxError("Date must have timezone to be converted")
    utcTimestamp = (parsedTime - parsedTime.utcoffset()).replace(tzinfo=SimpleUtc())
    return utcTimestamp
