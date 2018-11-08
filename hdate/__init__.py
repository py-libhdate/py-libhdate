"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a represantation either in English or Hebrew
of the Jewish calendrical date and times for a given location
"""
from collections import namedtuple
from dateutil import tz

from hdate.date import HDate
from hdate.zmanim import Zmanim

__all__ = ['HDate', 'Zmanim']

HebrewDate = namedtuple("HebrewDate", ["year", "month", "day"])
Location = namedtuple(
    "Location", ["latitude", "longitude", "timezone", "altitude"])

# Default location to Jerusalem values
Location.__new__.__defaults__ = (
    31.778, 35.235, tz.gettz("Asia/Jerusalem"), 754)
