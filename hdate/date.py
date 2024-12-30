"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a representation either in English, French or Hebrew
of the Jewish calendrical date and times for a given location
"""

from __future__ import annotations

import datetime
import logging
from itertools import chain, product
from typing import Any, Optional, Union, cast

from hdate import htables
from hdate.gematria import hebrew_number
from hdate.hebrew_date import HebrewDate
from hdate.htables import Holiday, HolidayTypes, Masechta, Months
from hdate.translator import TranslatorMixin

_LOGGER = logging.getLogger(__name__)
# pylint: disable=too-many-public-methods


class HDate(TranslatorMixin):
    """
    Hebrew date class.

    Supports converting from Gregorian and Julian to Hebrew date.
    """

    # Prefixes and strings for different languages
    OMER_SUFFIX = {
        "hebrew": "בעומר",
        "english": "in the Omer",
        "french": "jour du Omer",
    }

    def __init__(
        self,
        gdate: datetime.date = datetime.date.today(),
        diaspora: bool = False,
        language: str = "hebrew",
        heb_date: Optional[HebrewDate] = None,
    ) -> None:
        """Initialize the HDate object."""
        super().__init__()
        # Initialize private variables
        self._last_updated = ""

        if heb_date is None:
            self.gdate = gdate
            self._hdate = HebrewDate.from_gdate(gdate)
        else:
            self.hdate = heb_date
            self._gdate = heb_date.to_gdate()

        self.diaspora = diaspora
        self.set_language(language)

    def __str__(self) -> str:
        """Return a full Unicode representation of HDate."""
        in_prefix = "ב" if self._language == "hebrew" else ""
        day_number = hebrew_number(self.hdate.day, language=self._language)
        year_number = hebrew_number(self.hdate.year, language=self._language)
        result = f"{self.dow} {day_number} {in_prefix}{self.hdate.month} {year_number}"

        # Handle Omer day
        if 0 < self.omer_day < 50:
            omer_day_number = hebrew_number(self.omer_day, language=self._language)
            omer_suffix = self.OMER_SUFFIX.get(self._language, "in the Omer")
            result = f"{result} {omer_day_number} {omer_suffix}"

        # Append holiday description if any
        if self.holiday_description:
            result = f"{result} {self.holiday_description}"
        return result

    def __repr__(self) -> str:
        """Return a representation of HDate for programmatic use."""
        return (
            f"HDate(gdate={self.gdate!r}, diaspora={self.diaspora}, "
            f"language={self._language!r})"
        )

    def __lt__(self, other: "HDate") -> bool:
        """Implement the less-than operator."""
        assert isinstance(other, HDate)
        return bool(self.gdate < other.gdate)

    def __le__(self, other: "HDate") -> bool:
        """Implement the less-than or equal operator."""
        return not other < self

    def __gt__(self, other: "HDate") -> bool:
        """Implement the greater-than operator."""
        return other < self

    def __ge__(self, other: "HDate") -> bool:
        """Implement the greater than or equal operator."""
        return not self < other

    @property
    def hdate(self) -> HebrewDate:
        """Return the hebrew date."""
        if self._last_updated == "hdate":
            return self._hdate
        return HebrewDate.from_gdate(self._gdate)

    @hdate.setter
    def hdate(self, date: HebrewDate) -> None:
        """Set the dates of the HDate object based on a given Hebrew date."""

        if not isinstance(date, HebrewDate):
            raise TypeError(f"date: {date} is not of type HebrewDate")

        self._last_updated = "hdate"
        self._hdate = date

    @property
    def gdate(self) -> datetime.date:
        """Return the Gregorian date for the given Hebrew date object."""
        if self._last_updated == "gdate":
            return self._gdate
        return self._hdate.to_gdate()

    @gdate.setter
    def gdate(self, date: datetime.date) -> None:
        """Set the Gregorian date for the given Hebrew date object."""
        self._last_updated = "gdate"
        self._gdate = date

    @property
    def hebrew_date(self) -> str:
        """Return the hebrew date string in the selected language."""
        day = hebrew_number(self.hdate.day, language=self._language)
        year = hebrew_number(self.hdate.year, language=self._language)
        return f"{day} {self.hdate.month} {year}"

    @property
    def parasha(self) -> str:
        """Return the upcoming parasha in the selected language."""
        parasha = self.get_reading()
        parasha.set_language(self._language)
        return str(parasha)

    @property
    def holiday_description(self) -> Optional[str]:
        """
        Return the holiday description in the selected language.
        If none exists, will return None.
        """
        entries = self._holiday_entries()
        for entry in entries:
            entry.set_language(self._language)
        return ", ".join(str(entry) for entry in entries) if entries else None

    @property
    def is_shabbat(self) -> bool:
        """Return True if this date is Shabbat, specifically Saturday.

        Returns False on Friday because the HDate object has no notion of time.
        For more detailed nuance, use the Zmanim object.
        """
        return self.gdate.weekday() == 5

    @property
    def is_holiday(self) -> bool:
        """Return True if this date is a holiday (any kind)."""
        return self.holiday_type != HolidayTypes.NONE

    @property
    def is_yom_tov(self) -> bool:
        """Return True if this date is a Yom Tov."""
        return self.holiday_type == HolidayTypes.YOM_TOV

    @property
    def is_leap_year(self) -> bool:
        """Return True if this date's year is a leap year."""
        return self.hdate.year % 19 in [0, 3, 6, 8, 11, 14, 17]

    @property
    def holiday_type(self) -> Union[HolidayTypes, list[HolidayTypes]]:
        """Return the holiday type if exists."""
        entries = self._holiday_entries()
        if len(entries) > 1:
            return [entry.type for entry in entries]
        if len(entries) == 1:
            return cast(HolidayTypes, entries[0].type)
        return HolidayTypes.NONE

    @property
    def holiday_name(self) -> Union[str, list[str]]:
        """Return the holiday name which is good for programmatic use."""
        entries = self._holiday_entries()
        if len(entries) > 1:
            return [entry.name for entry in entries]
        if len(entries) == 1:
            return cast(str, entries[0].name)
        return ""

    def _holiday_entries(self) -> list[Union[Holiday, Any]]:
        """Return the abstract holiday information from holidays table."""
        _holidays_list = self.get_holidays_for_year()
        holidays_list = [
            holiday
            for holiday, holiday_hdate in _holidays_list
            if holiday_hdate.hdate == self.hdate
        ]

        # If anything is left return it, otherwise return the "NULL" holiday
        return holidays_list

    def short_kislev(self) -> bool:
        """Return whether this year has a short Kislev or not."""
        return self.year_size() in [353, 383]

    def long_cheshvan(self) -> bool:
        """Return whether this year has a long Cheshvan or not."""
        return self.year_size() in [355, 385]

    @property
    def dow(self) -> htables.Days:
        """Return day of week enum."""
        # datetime weekday maps Monday->0, Sunday->6; this remaps to Sunday->1.
        _dow = self.gdate.weekday() + 2 if self.gdate.weekday() != 6 else 1
        dow = htables.Days(_dow)
        dow.set_language(self._language)
        return dow

    def year_size(self) -> int:
        """Return the size of the given Hebrew year."""
        return HebrewDate.year_size(self.hdate.year)

    def rosh_hashana_dow(self) -> int:
        """Return the Hebrew day of week for Rosh Hashana."""
        jdn = HebrewDate(self.hdate.year, Months.TISHREI, 1).to_jdn()
        return (jdn + 1) % 7 + 1

    def pesach_dow(self) -> int:
        """Return the first day of week for Pesach."""
        jdn = HebrewDate(self.hdate.year, Months.NISAN, 15).to_jdn()
        return (jdn + 1) % 7 + 1

    @property
    def omer_day(self) -> int:
        """Return the day of the Omer."""
        first_omer_day = HebrewDate(self.hdate.year, Months.NISAN, 16)
        omer_day = (self.hdate - first_omer_day).days + 1
        if not 0 < omer_day < 50:
            return 0
        return omer_day

    @property
    def daf_yomi_repr(self) -> tuple[Masechta, int]:
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
    def daf_yomi(self) -> str:
        """Return a string representation of the daf yomi."""
        mesechta, daf_number = self.daf_yomi_repr
        mesechta.set_language(self._language)
        daf = hebrew_number(daf_number, language=self._language, short=True)
        return f"{mesechta} {daf}"

    @property
    def next_day(self) -> "HDate":
        """Return the HDate for the next day."""
        return HDate(self.gdate + datetime.timedelta(1), self.diaspora, self._language)

    @property
    def previous_day(self) -> "HDate":
        """Return the HDate for the previous day."""
        return HDate(self.gdate + datetime.timedelta(-1), self.diaspora, self._language)

    @property
    def upcoming_shabbat(self) -> "HDate":
        """Return the HDate for either the upcoming or current Shabbat.

        If it is currently Shabbat, returns the HDate of the Saturday.
        """
        if self.is_shabbat:
            return self
        # If it's Sunday, fast forward to the next Shabbat.
        saturday = self.gdate + datetime.timedelta((12 - self.gdate.weekday()) % 7)
        return HDate(saturday, diaspora=self.diaspora, language=self._language)

    @property
    def upcoming_shabbat_or_yom_tov(self) -> "HDate":
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
    def first_day(self) -> "HDate":
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
    def last_day(self) -> "HDate":
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

    def get_holidays_for_year(
        self, types: Optional[list[HolidayTypes]] = None
    ) -> list[tuple[Holiday, HDate]]:
        """Get all the actual holiday days for a given HDate's year.

        If specified, use the list of types to limit the holidays returned.
        """
        _LOGGER.debug("Looking up holidays of types %s", types)
        # Filter any non-related holidays depending on Israel/Diaspora only
        _holidays_list = [
            holiday
            for holiday in htables.HOLIDAYS
            if (holiday.israel_diaspora == "")
            or (holiday.israel_diaspora == "ISRAEL" and not self.diaspora)
            or (holiday.israel_diaspora == "DIASPORA" and self.diaspora)
        ]

        if types:
            # Filter non-matching holiday types.
            _holidays_list = [
                holiday for holiday in _holidays_list if holiday.type in types
            ]

        _LOGGER.debug(
            "Holidays after filters have been applied: %s",
            [holiday.name for holiday in _holidays_list],
        )

        def holiday_dates_cross_product(
            holiday: Holiday,
        ) -> product[tuple[int, ...]]:
            """Given a (days, months) pair, compute the cross product.

            If days and/or months are singletons, they are converted to a list.
            """
            return product(
                *([x] if isinstance(x, (int, Months)) else x for x in holiday.date)
            )

        # Compute out every actual Hebrew date on which a holiday falls for
        # this year by exploding out the possible days for each holiday.
        _holidays_list_1 = [
            (
                holiday,
                HDate(
                    heb_date=HebrewDate(
                        self.hdate.year, date_instance[1], date_instance[0]
                    ),
                    diaspora=self.diaspora,
                    language=self._language,
                ),
            )
            for holiday in _holidays_list
            for date_instance in holiday_dates_cross_product(holiday)
            if len(holiday.date) >= 2
        ]
        # Filter any special cases defined by True/False functions
        holidays_list = [
            (holiday, date)
            for (holiday, date) in _holidays_list_1
            if all(func(date) for func in holiday.date_functions_list)
        ]
        return holidays_list

    @property
    def upcoming_yom_tov(self) -> "HDate":
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
            language=self._language,
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

    def get_reading(self) -> htables.Parasha:
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
        days = (self.hdate - rosh_hashana).days
        # Number of weeks since rosh hashana
        weeks = (days + self.rosh_hashana_dow() - 1) // 7
        _LOGGER.debug("Since Rosh Hashana - Days: %d, Weeks %d", days, weeks)

        # If it's currently Simchat Torah, return VeZot Haberacha.
        if weeks == 3:
            if (
                days <= 22
                and self.diaspora
                and self.dow != htables.Days.SATURDAY
                or days <= 21
                and not self.diaspora
            ):
                return htables.Parasha.VEZOT_HABRACHA

        # Special case for Simchat Torah in diaspora.
        if weeks == 4 and days == 22 and self.diaspora:
            return htables.Parasha.VEZOT_HABRACHA

        readings = next(
            seq
            for types, seq in htables.PARASHA_SEQUENCES.items()
            if year_type in types
        )
        # Maybe recompute the year type based on the upcoming shabbat.
        # This avoids an edge case where today is before Rosh Hashana but
        # Shabbat is in a new year afterwards.
        if (
            weeks >= len(readings)
            and self.hdate.year < self.upcoming_shabbat.hdate.year
        ):
            return self.upcoming_shabbat.get_reading()
        return cast(htables.Parasha, readings[weeks])


def get_omer_string(omer: int, language: str = "hebrew") -> str:
    """Return a string representing the count of the Omer."""

    if not 0 < omer < 50:
        raise ValueError(f"Invalid Omer day: {omer}")

    if language == "hebrew":
        return _get_omer_string_hebrew(omer)
    if language == "english":
        return _get_omer_string_english(omer)
    if language == "french":
        return _get_omer_string_french(omer)

    return f"Today is day {omer} of the Omer."


def _get_omer_string_hebrew(omer: int) -> str:
    """Return a string representing the count of the Omer in hebrew."""
    tens = ["", "עשרה", "עשרים", "שלושים", "ארבעים"]
    ones = [
        "",
        "אחד",
        "שנים",
        "שלושה",
        "ארבעה",
        "חמשה",
        "ששה",
        "שבעה",
        "שמונה",
        "תשעה",
    ]

    omer_string = "היום "

    if 10 < omer < 20:
        omer_string += f"{ones[omer % 10]} עשר"
    elif omer >= 10:
        unit_part = ones[omer % 10]
        if omer % 10:
            unit_part += " ו"
        omer_string += unit_part + tens[omer // 10]
    else:

        if omer > 2:
            omer_string += ones[omer]

    if omer > 2:
        if omer < 11:
            omer_string += " ימים "
        else:
            omer_string += " יום "
    elif omer == 1:
        omer_string += "יום אחד "
    else:  # omer == 2
        omer_string += "שני ימים "

    if omer > 6:
        omer_string += "שהם "
        weeks, days = divmod(omer, 7)

        week_mapping = {1: "שבוע אחד ", 2: "שני שבועות "}
        omer_string += week_mapping.get(weeks, f"{ones[weeks]} שבועות ")

        if days:
            day_mapping = {1: "יום אחד ", 2: "שני ימים "}
            omer_string += "ו" + day_mapping.get(days, f"{ones[days]} ימים ")

    omer_string += "לעומר"
    return omer_string


def _get_omer_string_english(omer: int) -> str:
    """Return a string representing the count of the Omer in english."""
    ones = [
        "",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    teens = [
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]
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
    return omer_string


def _get_omer_string_french(omer: int) -> str:
    """Return a string representing the count of the Omer in french."""
    ones = [
        "",
        "un",
        "deux",
        "trois",
        "quatre",
        "cinq",
        "six",
        "sept",
        "huit",
        "neuf",
    ]
    teens = [
        "dix",
        "onze",
        "douze",
        "treize",
        "quatorze",
        "quinze",
        "seize",
        "dix-sept",
        "dix-huit",
        "dix-neuf",
    ]
    tens = ["", "", "vingt", "trente", "quarante"]

    irregular_ordinals = {
        1: "premier",
        2: "deuxième",
        3: "troisième",
        4: "quatrième",
        5: "cinquième",
        6: "sixième",
        7: "septième",
        8: "huitième",
        9: "neuvième",
        10: "dixième",
        11: "onzième",
        12: "douzième",
        13: "treizième",
        14: "quatorzième",
        15: "quinzième",
        16: "seizième",
        20: "vingtième",
        30: "trentième",
        40: "quarantième",
    }

    # Init
    omer_string = "Aujourd'hui c'est le "

    ten = omer // 10
    one = omer % 10

    # Construction
    if omer in irregular_ordinals:
        ordinal = irregular_ordinals[omer]
    else:
        if omer < 10:
            number_word = ones[omer]
        elif 10 < omer < 20:
            number_word = teens[omer - 10]
        else:
            if one == 1 and ten > 1:
                number_word = tens[ten] + " et un"
            else:
                number_word = tens[ten]
                if one != 0:
                    number_word += "-" + ones[one]

        ordinal = number_word + "ième"

    omer_string += ordinal + " jour de l'Omer"
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
    return omer_string
