# -*- coding: utf-8 -*-

"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a represantation either in English or Hebrew
of the Jewish calendrical date and times for a given location
"""
from __future__ import division

import datetime
import sys
from itertools import chain, product

from hdate import hdate_julian as hj
from hdate import htables
from hdate.common import set_date


class HDate(object):
    """
    Hebrew date class.

    Supports converting from Gregorian and Julian to Hebrew date.
    """

    def __init__(self, date=None, diaspora=False, hebrew=True):
        """Initialize the HDate object."""
        self.gdate = set_date(date)
        self._hebrew = hebrew
        self._diaspora = diaspora
        self.jdn = hj.gdate_to_jdn(self.gdate.day, self.gdate.month,
                                   self.gdate.year)
        (self.h_day, self.h_month, self.h_year) = hj.jdn_to_hdate(self.jdn)

    def __unicode__(self):
        """Return a Unicode representation of HDate."""
        return get_hebrew_date(self.h_day, self.h_month, self.h_year,
                               self.get_omer_day(), self.dow(),
                               self.get_holyday(), hebrew=self._hebrew,
                               short=False)

    def __str__(self):
        """Return a string representation of HDate."""
        if sys.version_info.major < 3:
            return unicode(self).encode('utf-8')

        return self.__unicode__()

    def hdate_set_hdate(self, day, month, year):
        """Set the dates of the HDate object based on a given Hebrew date."""
        # sanity check
        if not 0 < month < 15:
            raise ValueError('month ({}) legal values are 1-14'.format(month))
        if not 0 < day < 31:
            raise ValueError('day ({}) legal values are 1-31'.format(day))

        jdn = hj.hdate_to_jdn(day, month, year)
        self.hdate_set_jdn(jdn)

    def hdate_set_jdn(self, jdn):
        """Set the date of the HDate object based on Julian date."""
        gday, gmonth, gyear = hj.jdn_to_gdate(jdn)
        gdate = datetime.date(gyear, gmonth, gday)
        self.__init__(gdate, self._diaspora, self._hebrew)

    def get_hebrew_date(self):
        """Return the hebrew date in the form of day, month year."""
        return self.h_day, self.h_month, self.h_year

    def get_holyday(self):
        """Return the number of holyday."""
        # Get the possible list of holydays for this day
        holydays_list = [
            holyday for holyday in htables.HOLIDAYS if
            (self.h_day, self.h_month) in product(
                *([x] if isinstance(x, int) else x for x in holyday.date))]

        # Filter any non-related holydays depending on Israel/Diaspora only
        holydays_list = [
            holyday for holyday in holydays_list if
            (holyday.israel_diaspora == "") or
            (holyday.israel_diaspora == "ISRAEL" and not self._diaspora) or
            (holyday.israel_diaspora == "DIASPORA" and self._diaspora)]

        # Filter any special cases defined by True/False functions
        holydays_list = [
            holyday for holyday in holydays_list if
            all(func(self) for func in holyday.date_functions_list)]

        assert len(holydays_list) <= 1

        # If anything is left return it, otherwise return 0
        return holydays_list[0].index if holydays_list else 0

    def get_holyday_name(self):
        """Return descriptive name for the current holyday."""
        try:
            name = next(x.name for x in htables.HOLIDAYS
                        if x.index == self.get_holyday())
        except StopIteration:
            name = ""
        return name

    def short_kislev(self):
        """Return whether this year has a short Kislev or not."""
        return True if self.year_size() in [353, 383] else False

    def dow(self):
        """Return Hebrew day of week Sunday = 1, Saturday = 6."""
        return self.gdate.weekday() + 2 if self.gdate.weekday() != 6 else 1

    def year_size(self):
        """Return the size of the given Hebrew year."""
        return hj.get_size_of_hebrew_year(self.h_year)

    def rosh_hashana_dow(self):
        """Return the Hebrew day of week for Rosh Hashana."""
        jdn = hj.hdate_to_jdn(1, 1, self.h_year)
        return (jdn + 1) % 7 + 1

    def pesach_dow(self):
        """Return the first day of week for Pesach."""
        jdn = hj.hdate_to_jdn(15, 7, self.h_year)
        return (jdn + 1) % 7 + 1

    def get_omer_day(self):
        """Return the day of the Omer."""
        omer_day = self.jdn - hj.hdate_to_jdn(16, 7, self.h_year) + 1
        if not 0 < omer_day < 50:
            return 0
        return omer_day

    def get_reading(self, diaspora):
        """Return number of hebrew parasha."""
        _year_type = (self.year_size() % 10) - 3
        year_type = (
            diaspora * 1000 +
            self.rosh_hashana_dow() * 100 +
            _year_type * 10 +
            self.pesach_dow())

        days = self.jdn - hj.hdate_to_jdn(1, 1, self.h_year)
        weeks = (days + self.rosh_hashana_dow() - 1) // 7

        if self.dow() != 7:
            if days == 22 and diaspora or days == 21 and not diaspora:
                return 54
            return 0

        readings = list(
            chain(*([x] if isinstance(x, int) else x
                    for reading in htables.READINGS
                    for x in reading.readings
                    if year_type in reading.year_type)))

        return readings[weeks]


def get_holyday_type(holyday):
    """Return a number describing the type of the holy day."""
    try:
        holyday_type = next(x.type for x in htables.HOLIDAYS
                            if x.index == holyday)
    except StopIteration:
        holyday_type = 0
    return holyday_type


def hebrew_number(num, hebrew=True, short=False):
    """Return "Gimatria" number."""
    if not hebrew:
        return str(num)
    if not 0 <= num < 10000:
        raise ValueError('num must be between 0 to 9999, got:{}'.format(num))
    hstring = u""
    if num >= 1000:
        hstring += htables.DIGITS[0][num // 1000]
        hstring += u"' "
        num = num % 1000
    while num >= 400:
        hstring += htables.DIGITS[2][4]
        num = num - 400
    if num >= 100:
        hstring += htables.DIGITS[2][num // 100]
        num = num % 100
    if num >= 10:
        if num in [15, 16]:
            num = num - 9
        hstring += htables.DIGITS[1][num // 10]
        num = num % 10
    if num > 0:
        hstring += htables.DIGITS[0][num]
    # possibly add the ' and " to hebrew numbers
    if not short:
        if len(hstring) < 2:
            hstring += u"'"
        else:
            hstring = hstring[:-1] + u'"' + hstring[-1]
    return hstring


def get_omer_string(omer):
    """Return a string representing the count of the Omer."""
    tens = [u"", u"עשרה", u"עשרים", u"שלושים", u"ארבעים"]
    ones = [u"", u"אחד", u"שנים", u"שלושה", u"ארבעה", u"חמשה",
            u"ששה", u"שבעה", u"שמונה", u"תשעה"]
    if not 0 < omer < 50:
        raise ValueError('Invalid Omer day: {}'.format(omer))
    ten = omer // 10
    one = omer % 10
    omer_string = u'היום '
    if 10 < omer < 20:
        omer_string += ones[one] + u' עשר'
    elif omer > 9:
        omer_string += ones[one]
        if one:
            omer_string += u' ו'
    if omer > 2:
        if omer > 20 or omer in [10, 20]:
            omer_string += tens[ten]
        if omer < 11:
            omer_string += ones[one] + u' ימים '
        else:
            omer_string += u' יום '
    elif omer == 1:
        omer_string += u'יום אחד '
    else:  # omer == 2
        omer_string += u'שני ימים '
    if omer > 6:
        omer_string += u'שהם '
        weeks = omer // 7
        days = omer % 7
        if weeks > 2:
            omer_string += ones[weeks] + u' שבועות '
        elif weeks == 1:
            omer_string += u'שבוע אחד '
        else:  # weeks == 2
            omer_string += u'שני שבועות '
        if days:
            omer_string += u'ו'
            if days > 2:
                omer_string += ones[days] + u' ימים '
            elif days == 1:
                omer_string += u'יום אחד '
            else:  # days == 2
                omer_string += u'שני ימים '
    omer_string += u'לעומר'
    return omer_string


def get_parashe(parasha, short=False, hebrew=True):
    """Get the string representing the parasha."""
    res = htables.PARASHAOT[parasha][hebrew]
    if short:
        return res
    return u"{} {}".format(u"פרשת" if hebrew else u"Parashat", res)


def get_hebrew_date(day, month, year, omer=0, dow=0, holiday=0,
                    short=False, hebrew=True):
    """Return a string representing the given date."""
    # Day
    res = u"{} {}".format(hebrew_number(day, hebrew=hebrew, short=short),
                          u"ב" if hebrew else u"")
    # Month
    res += htables.MONTHS[month-1][hebrew]
    # Year
    res += u" " + hebrew_number(year, hebrew=hebrew, short=short)

    # Weekday
    if dow:
        dw_str = u"יום " if hebrew else u""
        dw_str += htables.DAYS[dow-1][hebrew][short]
        res = dw_str + u" " + res
    if short:
        return res

    # Omer
    if 0 < omer < 50:
        res += u" " + hebrew_number(omer, hebrew=hebrew, short=short)
        res += u" " + u"בעומר" if hebrew else u" in the Omer"

    # Holiday
    for _holiday in (x for x in htables.HOLIDAYS if x.index == holiday):
        desc = _holiday.description[hebrew]
        res += u" " + desc if not hebrew else desc[short]
    return res
