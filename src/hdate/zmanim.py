# -*- coding: utf-8 -*-

"""
Jewish calendrical times for a given location.

HDate calculates and generates a represantation either in English or Hebrew
of the Jewish calendrical times for a given location
"""
from __future__ import division

import datetime
import math
import sys

from dateutil import tz

from hdate import htables
from hdate.common import set_date


class Zmanim(object):
    """Return Jewish day times."""

    def __init__(self, date=None, latitude=None, longitude=None,
                 timezone='', hebrew=True):
        """Initialize the Zmanim object."""
        if latitude is None or longitude is None:
            # Tel Aviv cordinates
            latitude = 32.08088
            longitude = 34.78057
        self.date = set_date(date)
        self.latitude = latitude
        self.longitude = longitude
        self._hebrew = hebrew
        if not timezone:
            timezone = 'UTC'
        self.timezone = timezone
        self.zmanim = self.get_zmanim()

    def utc_minute_timezone(self, minutes_from_utc):
        """Return the local time for a given time UTC."""
        from_zone = tz.gettz('UTC')
        to_zone = (self.timezone if isinstance(self.timezone, datetime.tzinfo)
                   else tz.gettz(self.timezone))
        utc = datetime.datetime(self.date.year, self.date.month,
                                self.date.day) + \
            datetime.timedelta(minutes=minutes_from_utc)
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        return local

    def get_zmanim(self):
        """Return a dictionary of the zmanim the object represents."""
        zmanim_dict = dict()
        zmanim_list = self.get_utc_sun_time_full()
        for zman in zmanim_list:
            zmanim_dict[zman] = self.utc_minute_timezone(zmanim_list[zman])
        return zmanim_dict

    def __unicode__(self):
        """Return a Unicode representation of Zmanim."""
        return get_zmanim_string(self.zmanim, hebrew=self._hebrew)

    def __str__(self):
        """Return a string representation of Zmanim."""
        if sys.version_info.major < 3:
            return unicode(self).encode('utf-8')

        return self.__unicode__()

    def gday_of_year(self):
        """Return the number of days since January 1 of the given year."""
        return (self.date - datetime.date(self.date.year, 1, 1)).days

    def _get_utc_sun_time_deg(self, deg):
        """
        Return the sunset and sunrise times in minutes from 00:00 (utc).

        This is done for a given sun altitude in sunrise `deg` degrees
        This function only works for altitudes sun really is.
        If the sun never gets to this altitude, the returned sunset and sunrise
        values will be negative. This can happen in low altitude when latitude
        is nearing the poles in winter times, the sun never goes very high in
        the sky there.
        """
        gama = 0        # location of sun in yearly cycle in radians
        eqtime = 0      # difference betwen sun noon and clock noon
        decl = 0        # sun declanation
        hour_angle = 0  # solar hour angle
        sunrise_angle = math.pi * deg / 180.0  # sun angle at sunrise/set

        # get the day of year
        day_of_year = self.gday_of_year()

        # get radians of sun orbit around earth =)
        gama = 2.0 * math.pi * ((day_of_year - 1) / 365.0)

        # get the diff betwen suns clock and wall clock in minutes
        eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gama) -
                           0.032077 * math.sin(gama) -
                           0.014615 * math.cos(2.0 * gama) -
                           0.040849 * math.sin(2.0 * gama))

        # calculate suns declanation at the equater in radians
        decl = (0.006918 - 0.399912 * math.cos(gama) +
                0.070257 * math.sin(gama) -
                0.006758 * math.cos(2.0 * gama) +
                0.000907 * math.sin(2.0 * gama) -
                0.002697 * math.cos(3.0 * gama) +
                0.00148 * math.sin(3.0 * gama))

        # we use radians, ratio is 2pi/360
        latitude = math.pi * self.latitude / 180.0

        # the sun real time diff from noon at sunset/rise in radians
        try:
            hour_angle = (math.acos(
                math.cos(sunrise_angle) /
                (math.cos(latitude) * math.cos(decl)) -
                math.tan(latitude) * math.tan(decl)))
        # check for too high altitudes and return negative values
        except ValueError:
            return -720, -720

        # we use minutes, ratio is 1440min/2pi
        hour_angle = 720.0 * hour_angle / math.pi

        # get sunset/rise times in utc wall clock in minutes from 00:00 time
        # sunrise / sunset
        return int(720.0 - 4.0 * self.longitude - hour_angle - eqtime), \
            int(720.0 - 4.0 * self.longitude + hour_angle - eqtime)

    def get_utc_sun_time_full(self):
        """Return a list of Jewish times for the given location."""
        # sunset and rise time
        sunrise, sunset = self._get_utc_sun_time_deg(90.833)

        # shaa zmanit by gara, 1/12 of light time
        sun_hour = (sunset - sunrise) // 12
        midday = (sunset + sunrise) // 2

        # get times of the different sun angles
        first_light, _n = self._get_utc_sun_time_deg(106.1)
        talit, _n = self._get_utc_sun_time_deg(101.0)
        _n, first_stars = self._get_utc_sun_time_deg(96.0)
        _n, three_stars = self._get_utc_sun_time_deg(98.5)
        mga_sunhour = (midday - first_light) / 6

        res = dict(sunrise=sunrise, sunset=sunset, sun_hour=sun_hour,
                   midday=midday, first_light=first_light, talit=talit,
                   first_stars=first_stars, three_stars=three_stars,
                   plag_mincha=sunset - 1.25 * sun_hour,
                   stars_out=sunset + 18. * sun_hour / 60.,
                   small_mincha=sunrise + 9.5 * sun_hour,
                   big_mincha=sunrise + 6.5 * sun_hour,
                   mga_end_shma=first_light + mga_sunhour * 3.,
                   gra_end_shma=sunrise + sun_hour * 3.,
                   mga_end_tfila=first_light + mga_sunhour * 4.,
                   gra_end_tfila=sunrise + sun_hour * 4.,
                   midnight=midday + 12 * 60.)
        return res


def get_zmanim_string(zmanim, hebrew=True):
    """Get the string representing the zmanim of the day."""
    res = u""
    for zman in htables.ZMANIM:
        if zman.zman in zmanim:
            time = zmanim[zman.zman]
            res += u"{} - {:02d}:{:02d}\n".format(
                zman.description[hebrew], time.hour, time.minute)
    return res
