from collections import namedtuple

from dateutil import tz

HebrewDate = namedtuple("HebrewDate", ["year", "month", "day"])
Location = namedtuple(
    "Location", ["latitude", "longitude", "timezone", "altitude"])

# Default location to Jerusalem values
Location.__new__.__defaults__ = (
    31.778, 35.235, tz.gettz("Asia/Jerusalem"), 754)
