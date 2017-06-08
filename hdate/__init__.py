import hdate_julian as hj
from htables import holydays_table, join_flags
from hdate_string import get_hebrew_date, get_zmanim_string
import datetime
from dateutil import tz
import math


def M(h, p):
    return ((h * PARTS_IN_HOUR) + p)

PARTS_IN_HOUR = 1080
PARTS_IN_DAY = 24 * PARTS_IN_HOUR
PARTS_IN_WEEK = 7 * PARTS_IN_DAY
PARTS_IN_MONTH = PARTS_IN_DAY + M(12, 793)  # Tikun for regular month


def set_date(date):
    if date is None:
        date = datetime.date.today()
    elif not isinstance(date, datetime.date):
        raise TypeError
    return date


class Zmanim(object):
    """
    Return Jewish day times
    """
    def __init__(self, date=None, latitude=None, longitude=None, timezone='', hebrew=True):
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
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(self.timezone)
        utc = datetime.datetime(self.date.year, self.date.month, self.date.day) + datetime.timedelta(minutes=minutes_from_utc)
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        return local

    def get_zmanim(self):
        d = dict()
        zmanim_list = self.get_utc_sun_time_full()
        for z in zmanim_list:
            d[z] = self.utc_minute_timezone(zmanim_list[z])
        return d

    def __repr__(self):
        return get_zmanim_string(self.zmanim, hebrew=self._hebrew)

    def gday_of_year(self):
        return (self.date - datetime.date(self.date.year, 1, 1)).days

    def _get_utc_sun_time_deg(self, deg):
        """ Returns the sunset and sunrise times in minutes from 00:00 (utc time)
        if sun altitude in sunrise is deg degries.
        This function only works for altitudes sun realy is.
        If the sun never get to this altitude, the returned sunset and sunrise values
        will be negative. This can happen in low altitude when latitude is
        nearing the pols in winter times, the sun never goes very high in
        the sky there.
        """
        M_PI = math.pi
        gama = 0  # location of sun in yearly cycle in radians
        eqtime = 0  # diffference betwen sun noon and clock noon
        decl = 0  # sun declanation
        ha = 0  # solar hour engle
        sunrise_angle = M_PI * deg / 180.0  # sun angle at sunrise/set

        # get the day of year
        day_of_year = self.gday_of_year()

        # get radians of sun orbit around erth =)
        gama = 2.0 * M_PI * ((day_of_year - 1) / 365.0)

        # get the diff betwen suns clock and wall clock in minutes
        eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gama) -
                           0.032077 * math.sin(gama) - 0.014615 * math.cos(2.0 * gama) -
                           0.040849 * math.sin(2.0 * gama))

        # calculate suns declanation at the equater in radians
        decl = (0.006918 - 0.399912 * math.cos(gama) + 0.070257 * math.sin(gama) -
                0.006758 * math.cos(2.0 * gama) + 0.000907 * math.sin(2.0 * gama) -
                0.002697 * math.cos(3.0 * gama) + 0.00148 * math.sin(3.0 * gama))

        # we use radians, ratio is 2pi/360
        latitude = M_PI * self.latitude / 180.0

        # the sun real time diff from noon at sunset/rise in radians
        try:
            ha = math.acos(math.cos(sunrise_angle) / (math.cos(latitude) * math.cos(decl)) - math.tan(latitude) * math.tan(decl))
        # check for too high altitudes and return negative values
        except ValueError:
            return -720, -720

        # we use minutes, ratio is 1440min/2pi
        ha = 720.0 * ha / M_PI

        # get sunset/rise times in utc wall clock in minutes from 00:00 time
        # sunrise / sunset
        return int(720.0 - 4.0 * self.longitude - ha - eqtime), int(720.0 - 4.0 * self.longitude + ha - eqtime)

    def get_utc_sun_time(self):
        "utc sunrise/set time for a gregorian date"
        return self._get_utc_sun_time_deg(90.833)

    def get_utc_sun_time_full(self):
        """
        return list of jewish relevant time for location (and current HDate date)
        """
        # sunset and rise time
        sunrise, sunset = self.get_utc_sun_time()

        # shaa zmanit by gara, 1/12 of light time
        sun_hour = (sunset - sunrise) / 12
        midday = (sunset + sunrise) / 2

        # get times of the different sun angles
        first_light, _n = self._get_utc_sun_time_deg(106.1)
        talit, _n = self._get_utc_sun_time_deg(101.0)
        _n, first_stars = self._get_utc_sun_time_deg(96.0)
        _n, three_stars = self._get_utc_sun_time_deg(98.5)
        plag_mincha = sunset - 1.25 * sun_hour
        stars_out = sunset + 18. * sun_hour / 60.
        big_mincha = sunrise + 6.5 * sun_hour
        small_mincha = sunrise + 9.5 * sun_hour
        mga_sunhour = (midday - first_light) / 6.
        mga_end_shma = first_light + mga_sunhour * 3.
        gra_end_shma = sunrise + sun_hour * 3.
        mga_end_tfila = first_light + mga_sunhour * 4.
        gra_end_tfila = sunrise + sun_hour * 4.
        midnight = midday + 12 * 60.
        res = dict(sunrise=sunrise, sunset=sunset, sun_hour=sun_hour, midday=midday, first_light=first_light,
                   talit=talit, first_stars=first_stars, three_stars=three_stars, plag_mincha=plag_mincha,
                   stars_out=stars_out, small_mincha=small_mincha, big_mincha=big_mincha, mga_end_shma=mga_end_shma,
                   gra_end_shma=gra_end_shma, mga_end_tfila=mga_end_tfila, gra_end_tfila=gra_end_tfila, midnight=midnight)
        return res


class HDate(object):
    """
    Hebrew date class
    Support convert from Gregorian and Julian to Hebrew date
    """
    def __init__(self, date=None, diaspora=False, hebrew=True):
        self._gdate = set_date(date)
        self._hebrew = hebrew
        self._diaspora = diaspora
        self.hdate_set_gdate()

    def __repr__(self):
        return self.to_string(hebrew=self._hebrew).encode('utf-8')

    def _set_h_from_jd(self, jd_tishrey1, jd_tishrey1_next_year):
        self._weekday = (self._jd + 1) % 7 + 1
        self._h_size_of_year = jd_tishrey1_next_year - jd_tishrey1
        self._h_new_year_weekday = (jd_tishrey1 + 1) % 7 + 1
        self._h_year_type = hj._get_year_type(self._h_size_of_year, self._h_new_year_weekday)
        self._h_days = self._jd - jd_tishrey1 + 1
        self._h_weeks = ((self._h_days - 1) + (self._h_new_year_weekday - 1)) / 7 + 1

    def to_string(self, short=False, hebrew=True):
        return get_hebrew_date(self._h_day, self._h_month, self._h_year, self.get_omer_day(), self._weekday, self.get_holyday(), hebrew=hebrew, short=short)

    def hdate_set_gdate(self):
        self._jd = hj._gdate_to_jd(self._gdate.day, self._gdate.month, self._gdate.year)
        self._h_day, self._h_month, self._h_year, jd_tishrey1, jd_tishrey1_next_year = hj._jd_to_hdate(self._jd)
        self._set_h_from_jd(jd_tishrey1, jd_tishrey1_next_year)

    def hdate_set_hdate(self, d, m, y):
        self._jd, jd_tishrey1, jd_tishrey1_next_year = hj._hdate_to_jd(d, m, y)
        gd, gm, gy = hj._jd_to_gdate(self._jd)
        self._gdate = datetime.date(gy, gm, gd)
        self._set_h_from_jd(jd_tishrey1, jd_tishrey1_next_year)

    def hdate_set_jd(self, jd):
        gd, gm, gy = hj._jd_to_gdate(jd)
        self._gdate = datetime.date(gy, gm, gd)
        self.hdate_set_gdate()

    def get_hebrew_date(self):
        return self._h_day, self._h_month, self._h_year

    def get_holyday(self):
        """return the number of holyday"""
        diaspora=self._diaspora
        holyday = 0
        # sanity check
        if (self._h_month < 1 or self._h_month > 14 or self._h_day < 1 or self._h_day > 30):
            return 0

        holyday = holydays_table[self._h_month - 1][self._h_day - 1]

        # if tzom on sat delay one day
        # tzom gdalyaho on sat
        if ((holyday == 3) and (self._weekday == 7 or (self._h_day == 4 and self._weekday != 1))):
            holyday = 0
        # 17 of Tamuz on sat
        if ((holyday == 21) and ((self._weekday == 7) or (self._h_day == 18 and self._weekday != 1))):
            holyday = 0
        # 9 of Av on sat
        if ((holyday == 22) and ((self._weekday == 7) or (self._h_day == 10 and self._weekday != 1))):
            holyday = 0

        # Hanukah in a long year
        if ((holyday == 9) and (self._h_size_of_year % 10 != 3) and (self._h_day == 3)):
            holyday = 0

        # if tanit ester on sat mov to Thu
        if ((holyday == 12) and ((self._weekday == 7) or (self._h_day == 11 and self._weekday != 5))):
            holyday = 0

        # yom yerushalym after 68
        if (holyday == 26) and (self._gdate.year < 1968):
            holyday = 0

        # yom ha azmaot and yom ha zicaron
        if (holyday == 17):
            if (self._gdate.year < 1948):
                holyday = 0
            elif (self._gdate.year < 2004):
                if ((self._h_day == 3) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 4) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 5) and (self._weekday != 6 and self._weekday != 7)):
                    holyday = 17
                elif ((self._h_day == 2) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 3) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 4) and (self._weekday != 5 and self._weekday != 6)):
                    holyday = 25
                else:
                    holyday = 0
            else:
                if ((self._h_day == 3) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 4) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 6) and (self._weekday == 3)):
                    holyday = 17
                elif ((self._h_day == 5) and (self._weekday != 6 and self._weekday != 7 and self._weekday != 2)):
                    holyday = 17
                elif ((self._h_day == 2) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 3) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 5) and (self._weekday == 2)):
                    holyday = 25
                elif ((self._h_day == 4) and (self._weekday != 5 and self._weekday != 6 and self._weekday != 1)):
                    holyday = 25
                else:
                    holyday = 0

        # yom ha shoaa, on years after 1958
        if (holyday == 24):
            if (self._gdate.year < 1958):
                holyday = 0
            else:
                if ((self._h_day == 26) and (self._weekday != 5)):
                    holyday = 0
                if ((self._h_day == 28) and (self._weekday != 2)):
                    holyday = 0
                if ((self._h_day == 27) and (self._weekday == 6 or self._weekday == 1)):
                    holyday = 0

        # Rabin day, on years after 1997
        if (holyday == 35):
            if (self._gdate.year < 1997):
                holyday = 0
            else:
                if ((self._h_day == 10 or self._h_day == 11) and (self._weekday != 5)):
                    holyday = 0
                if ((self._h_day == 12) and (self._weekday == 6 or self._weekday == 7)):
                    holyday = 0

        # Zhabotinsky day, on years after 2005
        if (holyday == 36):
            if (self._gdate.year < 2005):
                holyday = 0
            else:
                if ((self._h_day == 30) and (self._weekday != 1)):
                    holyday = 0
                if ((self._h_day == 29) and (self._weekday == 7)):
                    holyday = 0

        # diaspora holidays

        # simchat tora only in diaspora in israel just one day shmini+simchat tora
        if (holyday == 8 and not diaspora):
            holyday = 0

        # sukkot II holiday only in diaspora
        if (holyday == 31 and not diaspora):
            holyday = 6

        # pesach II holiday only in diaspora
        if (holyday == 32 and not diaspora):
            holyday = 16

        # shavot II holiday only in diaspora
        if (holyday == 30 and not diaspora):
            holyday = 0

        # pesach VIII holiday only in diaspora
        if (holyday == 29 and not diaspora):
            holyday = 0

        return holyday

    def get_omer_day(self):
        """return the day of the omer"""
        sixteen_nissan = HDate()
        sixteen_nissan.hdate_set_hdate(16, 7, self._h_year)
        omer_day = self._jd - sixteen_nissan._jd + 1
        if ((omer_day > 49) or (omer_day < 0)):
            omer_day = 0
        return omer_day

    def get_holyday_type(self, holyday):
        # regular day
        if (holyday == 0):
            return 0
        # Yom tov, To find erev yom tov, check if tomorrow returns 1
        if (holyday in [1, 2, 4, 5, 8, 15, 20, 27, 28, 29, 30, 31, 32]):
            return 1
        # Erev yom kippur
        if (holyday == 37):
            return 2
        # Hol hamoed
        if (holyday in [6, 7, 16]):
            return 3
        # Hanuka and purim
        if (holyday in [9, 13, 14]):
            return 4
        # Tzom
        if (holyday in [3, 10, 12, 21, 22]):
            return 5
        # Independance day and Yom yerushalaim
        if (holyday in [17, 26]):
            return 6
        # Lag baomer ,Tu beav, Tu beshvat
        if (holyday in [18, 23, 11]):
            return 7
        # Tzahal and Holocaust memorial days
        if (holyday in [24, 25]):
            return 8
        return 9

    def get_reading(self, diaspora):
        """Return number of hebrew parasha
        55..61 are joined readings e.g. Vayakhel Pekudei"""
        # if simhat tora return vezot habracha
        if (self._h_month == 1):
            # simhat tora is a day after shmini atzeret outsite israel
            if (self._h_day == 22 and not diaspora):
                return 54
            if (self._h_day == 23 and diaspora):
                return 54

        # if not shabat return none
        if (self._h_weekday != 7):
            return 0

        if (self._h_weeks == 1):
            if (self._h_new_year_weekday == 7):
                # Rosh hashana
                return 0
            elif ((self._h_new_year_weekday == 2) or (self._h_new_year_weekday == 3)):
                return 52
            else:  # if (self._h_new_year_weekday == 5)
                return 53
        elif(self._h_weeks == 2):
            if (self._h_new_year_weekday == 5):
                # Yom kippur
                return 0
            else:
                return 53
        elif(self._h_weeks == 3):
            # Succot
            return 0
        elif(self._h_weeks == 4):
            if (self._h_new_year_weekday == 7):
                # Simhat tora in israel
                if (not diaspora):
                    return 54
                # Not simhat tora in diaspora
                else:
                    return 0
            else:
                return 1
        else:
            # simhat tora on week 4 bereshit too
            reading = self._h_weeks - 3

            # was simhat tora on shabat ?
            if (self._h_new_year_weekday == 7):
                reading = reading - 1

            # no joining
            if (reading < 22):
                return reading

            # pesach
            if ((self._h_month == 7) and (self._h_day > 14)):
                # Shmini of pesach in diaspora is on the 22 of the month*/
                if (diaspora and (self._h_day <= 22)):
                    return 0
                if (not diaspora and (self._h_day < 22)):
                    return 0

            # Pesach allways removes one
            if (((self._h_month == 7) and (self._h_day > 21)) or (self._h_month > 7 and self._h_month < 13)):
                reading -= 1

                # on diaspora, shmini of pesach may fall on shabat if next new year is on shabat
                if (diaspora and (((self._h_new_year_weekday + self._h_size_of_year) % 7) == 2)):
                    reading -= 1

            # on diaspora, shavot may fall on shabat if next new year is on shabat
            if (diaspora and
               (self._h_month < 13) and
               ((self._h_month > 9) or (self._h_month == 9 and self._h_day >= 7)) and
               ((self._h_new_year_weekday + self._h_size_of_year) % 7) == 0):
                if (self._h_month == 9 and self._h_day == 7):
                    return 0
                else:
                    reading -= 1

            # joining
            if (join_flags[diaspora][self._h_year_type - 1][0] and (reading >= 22)):
                if (reading == 22):
                    return 55
                else:
                    reading += 1
            if (join_flags[diaspora][self._h_year_type - 1][1] and (reading >= 27)):
                if (reading == 27):
                    return 56
                else:
                    reading += 1
            if (join_flags[diaspora][self._h_year_type - 1][2] and (reading >= 29)):
                if (reading == 29):
                    return 57
                else:
                    reading += 1
            if (join_flags[diaspora][self._h_year_type - 1][3] and (reading >= 32)):
                if (reading == 32):
                    return 58
                else:
                    reading += 1

            if (join_flags[diaspora][self._h_year_type - 1][4] and (reading >= 39)):
                if (reading == 39):
                    return 59
                else:
                    reading += 1
            if (join_flags[diaspora][self._h_year_type - 1][5] and (reading >= 42)):
                if (reading == 42):
                    return 60
                else:
                    reading += 1
            if (join_flags[diaspora][self._h_year_type - 1][6] and (reading >= 51)):
                if (reading == 51):
                    return 61
                else:
                    reading += 1
        return reading
