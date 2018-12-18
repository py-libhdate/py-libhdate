# -*- coding: utf-8 -*-

"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a represantation either in English or Hebrew
of the Jewish calendrical date and times for a given location
"""
from __future__ import division

import datetime
import logging
from itertools import chain, product

from hdate import converters as conv
from hdate import htables
from hdate.common import BaseClass, HebrewDate
from hdate.htables import HolidayTypes, Months

_LOGGER = logging.getLogger(__name__)
# pylint: disable=too-many-public-methods


class HDate(BaseClass):
    """
    Hebrew date class.

    Supports converting from Gregorian and Julian to Hebrew date.
    """

    def __init__(self, gdate=datetime.date.today(), diaspora=False,
                 hebrew=True, heb_date=None):
        """Initialize the HDate object."""
        # Create private variables
        self._hdate = None
        self._gdate = None
        self._last_updated = None

        # Assign values
        # Keep hdate after gdate assignment so as not to cause recursion error
        if heb_date is None:
            self.gdate = gdate
            self.hdate = None
        else:
            self.gdate = None
            self.hdate = heb_date
        self.hebrew = hebrew
        self.diaspora = diaspora

    def __unicode__(self):
        """Return a full Unicode representation of HDate."""
        result = u"{}{} {} {}{} {}".format(
            u"יום " if self.hebrew else u"",
            htables.DAYS[self.dow - 1][self.hebrew][0],
            hebrew_number(self.hdate.day, hebrew=self.hebrew),
            u"ב" if self.hebrew else u"",
            htables.MONTHS[self.hdate.month - 1][self.hebrew],
            hebrew_number(self.hdate.year, hebrew=self.hebrew))

        if 0 < self.omer_day < 50:
            result += u" " + hebrew_number(self.omer_day, hebrew=self.hebrew)
            result += u" " + u"בעומר" if self.hebrew else u" in the Omer"

        if self.holiday_description:
            result += u" " + self.holiday_description
        return result

    def __repr__(self):
        """Return a representation of HDate for programmatic use."""
        return ("HDate(gdate={}, diaspora={}, hebrew={})".format(
            repr(self.gdate), self.diaspora, self.hebrew))

    def __lt__(self, other):
        """Implement the less-than operator."""
        assert isinstance(other, HDate)
        return self.gdate < other.gdate

    def __le__(self, other):
        """Implement the less-than or equal operator."""
        return not other < self

    def __gt__(self, other):
        """Implement the greater-than operator."""
        return other < self

    def __ge__(self, other):
        """Implement the greater than or equal operator."""
        return not self < other

    @property
    def hdate(self):
        """Return the hebrew date."""
        if self._last_updated == "hdate":
            return self._hdate
        return conv.jdn_to_hdate(self._jdn)

    @hdate.setter
    def hdate(self, date):
        """Set the dates of the HDate object based on a given Hebrew date."""
        # Sanity checks
        if date is None and isinstance(self.gdate, datetime.date):
            # Calculate the value since gdate has been set
            date = self.hdate

        if not isinstance(date, HebrewDate):
            raise TypeError('date: {} is not of type HebrewDate'.format(date))
        if not 0 < date.month < 15:
            raise ValueError(
                'month ({}) legal values are 1-14'.format(date.month))
        if not 0 < date.day < 31:
            raise ValueError('day ({}) legal values are 1-31'.format(date.day))

        self._last_updated = "hdate"
        self._hdate = date

    @property
    def gdate(self):
        """Return the Gregorian date for the given Hebrew date object."""
        if self._last_updated == "gdate":
            return self._gdate
        return conv.jdn_to_gdate(self._jdn)

    @gdate.setter
    def gdate(self, date):
        """Set the Gregorian date for the given Hebrew date object."""
        self._last_updated = "gdate"
        self._gdate = date

    @property
    def _jdn(self):
        """Return the Julian date number for the given date."""
        if self._last_updated == "gdate":
            return conv.gdate_to_jdn(self.gdate)
        return conv.hdate_to_jdn(self.hdate)

    @property
    def hebrew_date(self):
        """Return the hebrew date string."""
        return u"{} {} {}".format(
            hebrew_number(self.hdate.day, hebrew=self.hebrew),   # Day
            htables.MONTHS[self.hdate.month - 1][self.hebrew],   # Month
            hebrew_number(self.hdate.year, hebrew=self.hebrew))  # Year

    @property
    def parasha(self):
        """Return the upcoming parasha."""
        return htables.PARASHAOT[self.get_reading()][self.hebrew]

    @property
    def holiday_description(self):
        """
        Return the holiday description.

        In case none exists will return None.
        """
        entry = self._holiday_entry()
        desc = entry.description
        return desc.hebrew.long if self.hebrew else desc.english

    @property
    def is_shabbat(self):
        """Return True if this date is Shabbat, specifically Saturday.

        Returns False on Friday because the HDate object has no notion of time.
        For more detailed nuance, use the Zmanim object.
        """
        return self.gdate.weekday() == 5

    @property
    def is_holiday(self):
        """Return True if this date is a holiday (any kind)."""
        return self.holiday_type != HolidayTypes.UNKNOWN

    @property
    def is_yom_tov(self):
        """Return True if this date is a Yom Tov."""
        return self.holiday_type == HolidayTypes.YOM_TOV

    @property
    def holiday_type(self):
        """Return the holiday type if exists."""
        entry = self._holiday_entry()
        return entry.type

    @property
    def holiday_name(self):
        """Return the holiday name which is good for programmatic use."""
        entry = self._holiday_entry()
        return entry.name

    def _holiday_entry(self):
        """Return the abstract holiday information from holidays table."""
        holidays_list = self.get_holidays_for_year()
        holidays_list = [
            holiday for holiday, holiday_hdate in holidays_list if
            holiday_hdate.hdate == self.hdate
        ]
        assert len(holidays_list) <= 1

        # If anything is left return it, otherwise return the "NULL" holiday
        return holidays_list[0] if holidays_list else htables.HOLIDAYS[0]

    def short_kislev(self):
        """Return whether this year has a short Kislev or not."""
        return self.year_size() in [353, 383]

    @property
    def dow(self):
        """Return Hebrew day of week Sunday = 1, Saturday = 7."""
        # datetime weekday maps Monday->0, Sunday->6; this remaps to Sunday->1.
        return self.gdate.weekday() + 2 if self.gdate.weekday() != 6 else 1

    def year_size(self):
        """Return the size of the given Hebrew year."""
        return conv.get_size_of_hebrew_year(self.hdate.year)

    def rosh_hashana_dow(self):
        """Return the Hebrew day of week for Rosh Hashana."""
        jdn = conv.hdate_to_jdn(HebrewDate(self.hdate.year, Months.Tishrei, 1))
        return (jdn + 1) % 7 + 1

    def pesach_dow(self):
        """Return the first day of week for Pesach."""
        jdn = conv.hdate_to_jdn(HebrewDate(self.hdate.year, Months.Nisan, 15))
        return (jdn + 1) % 7 + 1

    @property
    def omer_day(self):
        """Return the day of the Omer."""
        first_omer_day = HebrewDate(self.hdate.year, Months.Nisan, 16)
        omer_day = self._jdn - conv.hdate_to_jdn(first_omer_day) + 1
        if not 0 < omer_day < 50:
            return 0
        return omer_day

    @property
    def next_day(self):
        """Return the HDate for the next day."""
        return HDate(self.gdate + datetime.timedelta(1), self.diaspora,
                     self.hebrew)

    @property
    def previous_day(self):
        """Return the HDate for the previous day."""
        return HDate(self.gdate + datetime.timedelta(-1), self.diaspora,
                     self.hebrew)

    @property
    def upcoming_shabbat(self):
        """Return the HDate for either the upcoming or current Shabbat.

        If it is currently Shabbat, returns the HDate of the Saturday.
        """
        if self.is_shabbat:
            return self
        # If it's Sunday, fast forward to the next Shabbat.
        saturday = self.gdate + datetime.timedelta(
            (12 - self.gdate.weekday()) % 7)
        return HDate(saturday, diaspora=self.diaspora, hebrew=self.hebrew)

    @property
    def upcoming_shabbat_or_yom_tov(self):
        """Return the HDate for the upcoming or current Shabbat or Yom Tov.

        If it is currently Shabbat, returns the HDate of the Saturday.
        If it is currently Yom Tov, returns the HDate of the first day
        (rather than "leil" Yom Tov). To access Leil Yom Tov, use
        upcoming_shabbat_or_yom_tov.previous_day.
        """
        if self.is_shabbat or self.is_yom_tov:
            return self

        if self.upcoming_yom_tov < self.upcoming_shabbat:
            return self.upcoming_yom_tov
        return self.upcoming_shabbat

    @property
    def first_day(self):
        """Return the first day of Yom Tov or Shabbat.

        This is useful for three-day holidays, for example: it will return the
        first in a string of Yom Tov + Shabbat.
        If this HDate is Shabbat followed by no Yom Tov, returns the Saturday.
        If this HDate is neither Yom Tov, nor Shabbat, this just returns
        itself.
        """
        day_iter = self
        while (day_iter.previous_day.is_yom_tov or
               day_iter.previous_day.is_shabbat):
            day_iter = day_iter.previous_day
        return day_iter

    @property
    def last_day(self):
        """Return the last day of Yom Tov or Shabbat.

        This is useful for three-day holidays, for example: it will return the
        last in a string of Yom Tov + Shabbat.
        If this HDate is Shabbat followed by no Yom Tov, returns the Saturday.
        If this HDate is neither Yom Tov, nor Shabbat, this just returns
        itself.
        """
        day_iter = self
        while day_iter.next_day.is_yom_tov or day_iter.next_day.is_shabbat:
            day_iter = day_iter.next_day
        return day_iter

    def get_holidays_for_year(self, types=None):
        """Get all the actual holiday days for a given HDate's year.

        If specified, use the list of types to limit the holidays returned.
        """
        # Filter any non-related holidays depending on Israel/Diaspora only
        holidays_list = [
            holiday for holiday in htables.HOLIDAYS if
            (holiday.israel_diaspora == "") or
            (holiday.israel_diaspora == "ISRAEL" and not self.diaspora) or
            (holiday.israel_diaspora == "DIASPORA" and self.diaspora)]

        if types:
            # Filter non-matching holiday types.
            holidays_list = [
                holiday for holiday in holidays_list if
                holiday.type in types
            ]

        # Filter any special cases defined by True/False functions
        holidays_list = [
            holiday for holiday in holidays_list if
            all(func(self) for func in holiday.date_functions_list)]

        def holiday_dates_cross_product(holiday):
            """Given a (days, months) pair, compute the cross product.

            If days and/or months are singletons, they are converted to a list.
            """
            return product(*([x] if isinstance(x, int) else x
                             for x in holiday.date))

        # Compute out every actual Hebrew date on which a holiday falls for
        # this year by exploding out the possible days for each holiday.
        holidays_list = [
            (holiday, HDate(
                heb_date=HebrewDate(self.hdate.year, date_instance[1],
                                    date_instance[0]),
                diaspora=self.diaspora,
                hebrew=self.hebrew))
            for holiday in holidays_list
            for date_instance in holiday_dates_cross_product(holiday)
            if len(holiday.date) >= 2
        ]
        return holidays_list

    @property
    def upcoming_yom_tov(self):
        """Find the next upcoming yom tov (i.e. no-melacha holiday).

        If it is currently the day of yom tov (irrespective of zmanim), returns
        that yom tov.
        """
        if self.is_yom_tov:
            return self
        this_year = self.get_holidays_for_year([HolidayTypes.YOM_TOV])
        next_rosh_hashana = HDate(
            heb_date=HebrewDate(self.hdate.year + 1, Months.Tishrei, 1),
            diaspora=self.diaspora,
            hebrew=self.hebrew)
        next_year = next_rosh_hashana.get_holidays_for_year(
            [HolidayTypes.YOM_TOV])

        # Filter anything that's past.
        holidays_list = [
            holiday_hdate for _, holiday_hdate in chain(this_year, next_year)
            if holiday_hdate >= self
        ]

        holidays_list.sort(key=lambda h: h.gdate)

        return holidays_list[0]

    def get_reading(self):
        """Return number of hebrew parasha."""
        _year_type = (self.year_size() % 10) - 3
        year_type = (
            self.diaspora * 1000 +
            self.rosh_hashana_dow() * 100 +
            _year_type * 10 +
            self.pesach_dow())

        _LOGGER.debug("Year type: %d", year_type)

        # Number of days since rosh hashana
        rosh_hashana = HebrewDate(self.hdate.year, Months.Tishrei, 1)
        days = self._jdn - conv.hdate_to_jdn(rosh_hashana)
        # Number of weeks since rosh hashana
        weeks = (days + self.rosh_hashana_dow() - 1) // 7
        _LOGGER.debug("Days: %d, Weeks %d", days, weeks)

        # If it's currently Simchat Torah, return VeZot Haberacha.
        if weeks == 3:
            if (days <= 22 and self.diaspora and self.dow != 7 or
                    days <= 21 and not self.diaspora):
                return 54

        # Special case for Simchat Torah in diaspora.
        if weeks == 4 and days == 22 and self.diaspora:
            return 54

        # Return the indexes for the readings of the given year
        def unpack_readings(readings):
            return list(chain(
                *([x] if isinstance(x, int) else x for x in readings)))

        reading_for_year = htables.READINGS[year_type]
        readings = unpack_readings(reading_for_year)
        # Maybe recompute the year type based on the upcoming shabbat.
        # This avoids an edge case where today is before Rosh Hashana but
        # Shabbat is in a new year afterwards.
        if (weeks >= len(readings)
                and self.hdate.year < self.upcoming_shabbat.hdate.year):
            return self.upcoming_shabbat.get_reading()
        return readings[weeks]


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


def get_omer_string(omer):  # pylint: disable=too-many-branches
    """Return a string representing the count of the Omer."""
    # TODO: The following function should be simplified (see pylint)
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
