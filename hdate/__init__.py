"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a represantation either in English or Hebrew
of the Jewish calendrical date and times for a given location.
"""
from datetime import timedelta
from hdate.common import HebrewDate, Location
from hdate.date import HDate
from hdate.htables import HolidayTypes
from hdate.zmanim import Zmanim

__all__ = ['HDate', 'Zmanim', 'HebrewDate', 'Location', 'HolidayTypes']

def get_hdate_for_datetime(now, diaspora, hebrew, location, 
                           candle_lighting_offset, havdalah_offset):
    """Gets the HDate for a given datetime; switches after tzeit."""
    today = now.date()
    date = HDate(today, diaspora=diaspora, hebrew=hebrew)

    times = Zmanim(
        date=now, location=location,
        candle_lighting_offset=candle_lighting_offset,
        havdalah_offset=havdalah_offset, hebrew=hebrew)

    tzeit = times.zmanim['three_stars']
    # In case the havdalah offset is later than the calculated three stars,
    # use the later time.
    if times.havdalah is not None:
      tzeit = max(tzeit, times.havdalah)
    if (now >= tzeit):
      today += timedelta(1)
      date = HDate(today, diaspora=diaspora, hebrew=hebrew)
    return date
