"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a representation either in English or Hebrew
of the Jewish calendrical date and times for a given location
"""

import datetime
import logging
from itertools import chain, product

from hdate import converters as conv
from hdate import htables
from hdate.hebrew_date import HebrewDate
from hdate.htables import HolidayTypes, Months

_LOGGER = logging.getLogger(__name__)
# pylint: disable=too-many-public-methods

class HDate:
    """
    Hebrew date class.

    Supports converting from Gregorian and Julian to Hebrew date.
    """

    # Prefixes and strings for different languages
    DAY_PREFIXES = {'hebrew': 'יום ', 'english': '', 'french': ''}
    IN_PREFIXES = {'hebrew': 'ב', 'english': 'of ', 'french': ''}
    OMER_STRINGS = {'hebrew': 'בעומר', 'english': 'in the Omer', 'french': 'jour du Omer'}

    def __init__(
        self, gdate=datetime.date.today(), diaspora=False, lang='hebrew', heb_date=None
    ):
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
        self.lang = lang
        self.diaspora = diaspora
    
    def get_holiday_name(self):
        """Retrieve the holiday name based on the current language."""
        entries = self._holiday_entries()
        names = []
        for entry in entries:
            if self.lang == 'hebrew':
                names.append(entry.lang.hebrew.long)
            else:
                names.append(getattr(entry.lang, self.lang))
        return ", ".join(names)
    
    def get_number_repr(self, number, short=False):
        """Get the number representation based on the current language."""
        return hebrew_number(number, lang=self.lang, short=short)

    def get_month_name(self):
        """Return the month name in the selected language, handling leap years."""
        month = self.hdate.month
        is_leap = self.is_leap_year
        month_value = month.value

        # Adjust the month index for non-leap years
        if not is_leap:
            if month == Months.ADAR_II:
                # In non-leap years, Adar II is actually Adar
                month_value = Months.ADAR.value
            elif month.value > Months.ADAR.value:
                # Months after Adar II need to be adjusted down by one
                month_value -= 1

        # Adjust index for 0-based MONTHS tuple
        month_index = month_value - 1

        # Get the month name in the selected language
        month_lang = getattr(htables.MONTHS[month_index], self.lang)
        return month_lang

    def __str__(self):
        """Return a full Unicode representation of HDate."""
        # Get prefixes and strings based on language
        day_prefix = self.DAY_PREFIXES.get(self.lang, '')
        in_prefix = self.IN_PREFIXES.get(self.lang, '')

        # Get day name
        day_index = self.dow - 1  # Assuming dow is 1-based (Sunday=1)
        day_lang = getattr(htables.DAYS[day_index], self.lang)
        day_name = day_lang.long  # Use 'long' or 'short' as needed

        # Get day number representation
        day_number = self.get_number_repr(self.hdate.day)

        # Get month name
        month_name = self.get_month_name()

        # Get year number representation
        year_number = self.get_number_repr(self.hdate.year)

        result = f"{day_prefix}{day_name} {day_number} {in_prefix}{month_name} {year_number}"

        # Handle Omer day
        if 0 < self.omer_day < 50:
            omer_day_number = self.get_number_repr(self.omer_day)
            omer_string = self.OMER_STRINGS.get(self.lang, 'in the Omer')
            result = f"{result} {omer_day_number} {omer_string}"

        # Append holiday description if any
        if self.holiday_description:
            result = f"{result} {self.holiday_description}"
        return result


    def __repr__(self):
        """Return a representation of HDate for programmatic use."""
        return (
            f"HDate(gdate={self.gdate!r}, diaspora={self.diaspora}, "
            f"lang={self.lang!r})"
        )

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
            raise TypeError(f"date: {date} is not of type HebrewDate")
        if not 0 < date.day < 31:
            raise ValueError(f"day ({date.day}) legal values are 1-31")

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
        """Return the Hebrew date string in the selected language."""
        day = self.get_number_repr(self.hdate.day)
        month = getattr(htables.MONTHS[self.hdate.month.value - 1], self.lang)
        year = self.get_number_repr(self.hdate.year)
        return f"{day} {month} {year}"
    @property
    def parasha(self):
        """Return the upcoming parasha in the selected language."""
        parasha_index = self.get_reading()
        parasha = getattr(htables.PARASHAOT[parasha_index], self.lang)
        return parasha

    @property
    def holiday_description(self) -> Optional[str]:
        """
        Return the holiday description in the selected language.

        If none exists, will return None.
        """
        entries = self._holiday_entries()
        descriptions = []
        for entry in entries:
            # Access the language-specific description
            description_lang = getattr(entry.description, self.lang, None)
            if description_lang:
                # Check if it's a DESC namedtuple with 'long' and 'short' attributes
                if isinstance(description_lang, DESC):
                    descriptions.append(description_lang.long)
                else:
                    descriptions.append(description_lang)
        if descriptions:
            return ", ".join(descriptions)
        else:
            return None

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
    def is_leap_year(self):
        """Return True if this date's year is a leap year."""
        return self.hdate.year % 19 in [0, 3, 6, 8, 11, 14, 17]

    @property
    def holiday_type(self) -> List[HolidayTypes]:
        """Return a list of holiday types if they exist."""
        entries = self._holiday_entries()
        return [entry.type for entry in entries]

    @property
    def holiday_name(self) -> List[str]:
        """Return a list of holiday names for programmatic use."""
        entries = self._holiday_entries()
        return [entry.name for entry in entries]

    def _holiday_entries(self) -> List[HOLIDAY]:
        """Return the abstract holiday information from the holidays table."""
        holidays_list = self.get_holidays_for_year()
        entries = [
            holiday
            for holiday, holiday_hdate in holidays_list
            if holiday_hdate.hdate == self.hdate
        ]
        return entries

    def short_kislev(self):
        """Return whether this year has a short Kislev or not."""
        return self.year_size() in [353, 383]

    def long_cheshvan(self):
        """Return whether this year has a long Cheshvan or not."""
        return self.year_size() in [355, 385]

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
        jdn = conv.hdate_to_jdn(HebrewDate(self.hdate.year, Months.TISHREI, 1))
        return (jdn + 1) % 7 + 1

    def pesach_dow(self):
        """Return the first day of week for Pesach."""
        jdn = conv.hdate_to_jdn(HebrewDate(self.hdate.year, Months.NISAN, 15))
        return (jdn + 1) % 7 + 1

    @property
    def omer_day(self):
        """Return the day of the Omer."""
        first_omer_day = HebrewDate(self.hdate.year, Months.NISAN, 16)
        omer_day = self._jdn - conv.hdate_to_jdn(first_omer_day) + 1
        if not 0 < omer_day < 50:
            return 0
        return omer_day

    @property
    def daf_yomi_repr(self):
        """Return a tuple of mesechta and daf."""
        days_since_start_cycle_11 = (self.gdate - htables.DAF_YOMI_CYCLE_11_START).days
        page_number = days_since_start_cycle_11 % (htables.DAF_YOMI_TOTAL_PAGES)
        for mesechta in htables.DAF_YOMI_MESECHTOS:
            if page_number >= mesechta.pages:
                page_number -= mesechta.pages
            else:
                break
        daf_number = page_number + 2
        return mesechta, daf_number

    @property
    def daf_yomi(self):
        """Return a string representation of the daf yomi in the selected language."""
        mesechta, daf_number = self.daf_yomi_repr
        mesechta_name = getattr(mesechta.name, self.lang)
        daf = self.get_number_repr(daf_number)
        return f"{mesechta_name} {daf}"

    @property
    def next_day(self):
        """Return the HDate for the next day."""
        return HDate(self.gdate + datetime.timedelta(1), self.diaspora, self.lang)


    @property
    def previous_day(self):
        """Return the HDate for the previous day."""
        return HDate(self.gdate + datetime.timedelta(-1), self.diaspora, self.lang)

    @property
    def upcoming_shabbat(self):
        """Return the HDate for either the upcoming or current Shabbat.

        If it is currently Shabbat, returns the HDate of the Saturday.
        """
        if self.is_shabbat:
            return self
        # If it's Sunday, fast forward to the next Shabbat.
        saturday = self.gdate + datetime.timedelta((12 - self.gdate.weekday()) % 7)
        return HDate(saturday, diaspora=self.diaspora, lang=self.lang)

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
        while day_iter.previous_day.is_yom_tov or day_iter.previous_day.is_shabbat:
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
        _LOGGER.debug("Looking up holidays of types %s", types)
        # Filter any non-related holidays depending on Israel/Diaspora only
        holidays_list = [
            holiday
            for holiday in htables.HOLIDAYS
            if (holiday.israel_diaspora == "")
            or (holiday.israel_diaspora == "ISRAEL" and not self.diaspora)
            or (holiday.israel_diaspora == "DIASPORA" and self.diaspora)
        ]

        if types:
            # Filter non-matching holiday types.
            holidays_list = [
                holiday for holiday in holidays_list if holiday.type in types
            ]

        _LOGGER.debug(
            "Holidays after filters have been applied: %s",
            [holiday.name for holiday in holidays_list],
        )

        def holiday_dates_cross_product(holiday):
            """Given a (days, months) pair, compute the cross product.

            If days and/or months are singletons, they are converted to a list.
            """
            return product(
                *([x] if isinstance(x, (int, Months)) else x for x in holiday.date)
            )

        # Compute out every actual Hebrew date on which a holiday falls for
        # this year by exploding out the possible days for each holiday.
        holidays_list = [
            (
                holiday,
                HDate(
                    heb_date=HebrewDate(
                        self.hdate.year, date_instance[1], date_instance[0]
                    ),
                    diaspora=self.diaspora,
                    lang=self.lang,
                ),
            )
            for holiday in holidays_list
            for date_instance in holiday_dates_cross_product(holiday)
            if len(holiday.date) >= 2
        ]
        # Filter any special cases defined by True/False functions
        holidays_list = [
            (holiday, date)
            for (holiday, date) in holidays_list
            if all(func(date) for func in holiday.date_functions_list)
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
            heb_date=HebrewDate(self.hdate.year + 1, Months.TISHREI, 1),
            diaspora=self.diaspora,
            lang=self.lang,
        )
        next_year = next_rosh_hashana.get_holidays_for_year([HolidayTypes.YOM_TOV])

        # Filter anything that's past.
        holidays_list = [
            holiday_hdate
            for _, holiday_hdate in chain(this_year, next_year)
            if holiday_hdate >= self
        ]

        holidays_list.sort(key=lambda h: h.gdate)

        return holidays_list[0]

    def get_reading(self):
        """Return number of hebrew parasha."""
        _year_type = (self.year_size() % 10) - 3
        year_type = (
            self.diaspora * 1000
            + self.rosh_hashana_dow() * 100
            + _year_type * 10
            + self.pesach_dow()
        )

        _LOGGER.debug("Year type: %d", year_type)

        # Number of days since rosh hashana
        rosh_hashana = HebrewDate(self.hdate.year, Months.TISHREI, 1)
        days = self._jdn - conv.hdate_to_jdn(rosh_hashana)
        # Number of weeks since rosh hashana
        weeks = (days + self.rosh_hashana_dow() - 1) // 7
        _LOGGER.debug("Since Rosh Hashana - Days: %d, Weeks %d", days, weeks)

        # If it's currently Simchat Torah, return VeZot Haberacha.
        if weeks == 3:
            if (
                days <= 22
                and self.diaspora
                and self.dow != 7
                or days <= 21
                and not self.diaspora
            ):
                return 54

        # Special case for Simchat Torah in diaspora.
        if weeks == 4 and days == 22 and self.diaspora:
            return 54

        # Return the indexes for the readings of the given year
        def unpack_readings(readings):
            return list(chain(*([x] if isinstance(x, int) else x for x in readings)))

        reading_for_year = htables.READINGS[year_type]
        readings = unpack_readings(reading_for_year)
        # Maybe recompute the year type based on the upcoming shabbat.
        # This avoids an edge case where today is before Rosh Hashana but
        # Shabbat is in a new year afterwards.
        if (
            weeks >= len(readings)
            and self.hdate.year < self.upcoming_shabbat.hdate.year
        ):
            return self.upcoming_shabbat.get_reading()
        return readings[weeks]


def hebrew_number(num, lang='hebrew', short=False):
    """Return the number representation in the specified language.

    For 'hebrew', return the Hebrew numeral representation.
    For other languages, return the number as a string.
    """
    if lang != 'hebrew':
        return str(num)
    if not 0 < num < 10000:
        raise ValueError(f"num must be between 1 to 9999, got: {num}")
    hstring = ""
    # Handle thousands
    if num >= 1000:
        thousands = num // 1000
        hstring += htables.DIGITS[0][thousands] + "'"
        num = num % 1000
    # Handle hundreds
    hundreds = [400, 300, 200, 100]
    for value in hundreds:
        while num >= value:
            hstring += htables.DIGITS[2][value]
            num -= value
    # Handle tens
    if num >= 10:
        # Special cases for 15 and 16 to avoid sacred names
        if num == 15:
            hstring += htables.DIGITS[0][9] + htables.DIGITS[0][6]  # ט"ו
            num = 0
        elif num == 16:
            hstring += htables.DIGITS[0][9] + htables.DIGITS[0][7]  # ט"ז
            num = 0
        else:
            tens_value = (num // 10) * 10
            hstring += htables.DIGITS[1][tens_value]
            num = num % 10
    # Handle ones
    if num > 0:
        hstring += htables.DIGITS[0][num]
    # Add geresh or gershayim
    if not short:
        if len(hstring) == 1:
            hstring += "'"
        elif len(hstring) > 1:
            hstring = hstring[:-1] + '"' + hstring[-1]
    return hstring



def get_omer_string(omer, lang='hebrew'):
    """Return a string representing the count of the Omer in the specified language."""
    if not 0 < omer < 50:
        raise ValueError(f"Invalid Omer day: {omer}")

    if lang == 'hebrew':
        tens = ["", "עשרה", "עשרים", "שלושים", "ארבעים"]
        ones = ["", "אחד", "שניים", "שלושה", "ארבעה", "חמישה", "שישה", "שבעה", "שמונה", "תשעה"]
        omer_string = "היום "
        ten = omer // 10
        one = omer % 10

        if 10 < omer < 20:
            omer_string += ones[one] + " עשר"
        elif omer >= 20:
            if one != 0:
                omer_string += ones[one] + " ו"
            omer_string += tens[ten]
        else:
            omer_string += ones[omer]

        omer_string += " יום"
        # Add weeks and days
        weeks = omer // 7
        days = omer % 7
        if weeks > 0:
            omer_string += f", שהם {hebrew_number(weeks)} שבוע"
            if weeks > 1:
                omer_string += "ות"
            if days > 0:
                omer_string += f" ו-{hebrew_number(days)} יום"
        omer_string += " לעומר"
    elif lang == 'english':
        ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                 "seventeen", "eighteen", "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty"]
        omer_string = "Today is "
        if omer < 10:
            omer_string += ones[omer]
        elif 10 <= omer < 20:
            omer_string += teens[omer - 10]
        else:
            ten = omer // 10
            one = omer % 10
            omer_string += tens[ten]
            if one != 0:
                omer_string += "-" + ones[one]
        omer_string += " day"
        if omer != 1:
            omer_string += "s"
        omer_string += " of the Omer"
        # Add weeks and days
        weeks = omer // 7
        days = omer % 7
        if weeks > 0:
            omer_string += f", which is {weeks} week"
            if weeks != 1:
                omer_string += "s"
            if days > 0:
                omer_string += f" and {days} day"
                if days != 1:
                    omer_string += "s"
        omer_string += "."
    elif lang == 'french':
        ones = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
        teens = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize",
                 "dix-sept", "dix-huit", "dix-neuf"]
        tens = ["", "", "vingt", "trente", "quarante"]
        omer_string = "Aujourd'hui c'est le "
        if one == 1 and ten > 1:
            omer_string += tens[ten] + " et un"
        else:
            omer_string += tens[ten]
            if one != 0:
                omer_string += "-" + ones[one]
        if omer < 10:
            omer_string += ones[omer]
        elif 10 <= omer < 20:
            omer_string += teens[omer - 10]
        else:
            ten = omer // 10
            one = omer % 10
            omer_string += tens[ten]
            if one != 0:
                omer_string += "-" + ones[one]
        omer_string += "ième jour de l'Omer"
        # Add weeks and days
        weeks = omer // 7
        days = omer % 7
        if weeks > 0:
            omer_string += f", ce qui fait {weeks} semaine"
            if weeks != 1:
                omer_string += "s"
            if days > 0:
                omer_string += f" et {days} jour"
                if days != 1:
                    omer_string += "s"
        omer_string += "."
    else:
        # Default to English if language is not recognized
        omer_string = f"Today is day {omer} of the Omer."
    return omer_string

