"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a representation either in English, French or Hebrew
of the Jewish calendrical date and times for a given location
"""

from __future__ import annotations

import datetime as dt
import logging
from itertools import chain, product
from typing import Generator, Optional, Union, cast

from hdate import htables
from hdate.gematria import hebrew_number
from hdate.hebrew_date import HebrewDate, Months, Weekday
from hdate.htables import Holiday, HolidayTypes, Parasha
from hdate.omer import Omer
from hdate.translator import TranslatorMixin

_LOGGER = logging.getLogger(__name__)


class HDate(TranslatorMixin):  # pylint: disable=too-many-instance-attributes
    """
    Hebrew date class.

    Supports converting from Gregorian and Julian to Hebrew date.
    """

    def __init__(
        self,
        date: Union[dt.date, HebrewDate] = dt.date.today(),
        diaspora: bool = False,
        language: str = "hebrew",
    ) -> None:
        """Initialize the HDate object."""
        self.language = language
        super().__init__()
        # Initialize private variables
        self._last_updated = ""

        if isinstance(date, dt.date):
            self.gdate = date
            self._hdate = HebrewDate.from_gdate(date)
        else:
            self.hdate = date
            self._gdate = date.to_gdate()

        self.diaspora = diaspora
        self.omer = Omer(date=self.hdate, language=language)

    def __str__(self) -> str:
        """Return a full Unicode representation of HDate."""
        in_prefix = "ב" if self._language == "hebrew" else ""
        day_number = hebrew_number(self.hdate.day, language=self._language)
        year_number = hebrew_number(self.hdate.year, language=self._language)
        result = f"{self.dow} {day_number} {in_prefix}{self.hdate.month} {year_number}"

        if self.omer.total_days > 0:
            result = f"{result} {self.omer}"

        # Append holiday description if any
        if self.holidays:
            result = f"{result} {', '.join(str(holiday) for holiday in self.holidays)}"
        return result

    def __repr__(self) -> str:
        """Return a representation of HDate for programmatic use."""
        return (
            f"HDate(date={self.gdate!r}, diaspora={self.diaspora}, "
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
        hdate = (
            self._hdate
            if self._last_updated == "hdate"
            else HebrewDate.from_gdate(self._gdate)
        )
        hdate.set_language(self.language)
        return hdate

    @hdate.setter
    def hdate(self, date: HebrewDate) -> None:
        """Set the dates of the HDate object based on a given Hebrew date."""

        if not isinstance(date, HebrewDate):
            raise TypeError(f"date: {date} is not of type HebrewDate")

        self._last_updated = "hdate"
        self._hdate = date
        self.omer = Omer(date=self.hdate, language=self._language)

    @property
    def gdate(self) -> dt.date:
        """Return the Gregorian date for the given Hebrew date object."""
        if self._last_updated == "gdate":
            return self._gdate
        return self._hdate.to_gdate()

    @gdate.setter
    def gdate(self, date: dt.date) -> None:
        """Set the Gregorian date for the given Hebrew date object."""
        self._last_updated = "gdate"
        self._gdate = date

    @property
    def hebrew_date(self) -> str:
        """Return the hebrew date string in the selected language."""
        return str(self.hdate)

    @property
    def parasha(self) -> str:
        """Return the upcoming parasha in the selected language."""
        parasha = self.get_reading()
        parasha.set_language(self._language)
        return str(parasha)

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
        return len(self.holidays) > 0

    @property
    def is_yom_tov(self) -> bool:
        """Return True if this date is a Yom Tov."""
        return any(holiday.type == HolidayTypes.YOM_TOV for holiday in self.holidays)

    @property
    def holidays(self) -> list[Holiday]:
        """Return the abstract holiday information from holidays table."""
        _holidays_list = self.get_holidays_for_year()
        holidays_list = [
            holiday
            for holiday, holiday_hdate in _holidays_list
            if holiday_hdate == self.hdate
        ]

        for holiday in holidays_list:
            holiday.set_language(self._language)

        return holidays_list

    @property
    def dow(self) -> Weekday:
        """Return day of week enum."""
        # datetime weekday maps Monday->0, Sunday->6; this remaps to Sunday->1.
        _dow = self.gdate.weekday() + 2 if self.gdate.weekday() != 6 else 1
        dow = Weekday(_dow)
        dow.set_language(self._language)
        return dow

    @property
    def daf_yomi(self) -> str:
        """Return a string representation of the daf yomi."""
        days_since_start_cycle_11 = (self.gdate - htables.DAF_YOMI_CYCLE_11_START).days
        page_number = days_since_start_cycle_11 % (htables.DAF_YOMI_TOTAL_PAGES)
        for mesechta in htables.DAF_YOMI_MESECHTOS:
            if page_number >= mesechta.pages:
                page_number -= mesechta.pages
            else:
                break
        daf_number = page_number + 2
        mesechta.set_language(self._language)
        daf = hebrew_number(daf_number, language=self._language, short=True)
        return f"{mesechta} {daf}"

    @property
    def next_day(self) -> "HDate":
        """Return the HDate for the next day."""
        return HDate(self.gdate + dt.timedelta(1), self.diaspora, self._language)

    @property
    def previous_day(self) -> "HDate":
        """Return the HDate for the previous day."""
        return HDate(self.gdate + dt.timedelta(-1), self.diaspora, self._language)

    @property
    def upcoming_shabbat(self) -> "HDate":
        """Return the HDate for either the upcoming or current Shabbat.

        If it is currently Shabbat, returns the HDate of the Saturday.
        """
        if self.is_shabbat:
            return self
        # If it's Sunday, fast forward to the next Shabbat.
        saturday = self.gdate + dt.timedelta((12 - self.gdate.weekday()) % 7)
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
    ) -> list[tuple[Holiday, HebrewDate]]:
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
        def valid_holiday_dates(
            holidays_list: list[Holiday],
        ) -> Generator[tuple[Holiday, HebrewDate]]:
            for holiday in holidays_list:
                for date_instance in holiday_dates_cross_product(holiday):
                    if len(holiday.date) >= 2:
                        try:
                            yield (
                                holiday,
                                HebrewDate(
                                    year=self.hdate.year,
                                    month=date_instance[1],
                                    day=date_instance[0],
                                ),
                            )
                        except ValueError:
                            continue

        valid_holidays = list(valid_holiday_dates(_holidays_list))

        # Filter any special cases defined by True/False functions
        holidays_list = [
            (holiday, date)
            for (holiday, date) in valid_holidays
            if all(func(date) for func in holiday.date_functions_list)
        ]
        return holidays_list

    @property
    def upcoming_yom_tov(self) -> HDate:
        """Find the next upcoming yom tov (i.e. no-melacha holiday).

        If it is currently the day of yom tov (irrespective of zmanim), returns
        that yom tov.
        """
        if self.is_yom_tov:
            return self
        this_year = self.get_holidays_for_year([HolidayTypes.YOM_TOV])
        next_rosh_hashana = HDate(
            HebrewDate(self.hdate.year + 1, Months.TISHREI, 1),
            self.diaspora,
            self._language,
        )
        next_year = next_rosh_hashana.get_holidays_for_year([HolidayTypes.YOM_TOV])

        # Filter anything that's past, and make them HDate objects
        holidays_list = [
            holiday_hdate
            for _, holiday_hdate in chain(this_year, next_year)
            if holiday_hdate >= self.hdate
        ]

        holidays_list.sort(key=lambda h: h.to_gdate())

        return HDate(holidays_list[0], self.diaspora, self._language)

    def get_reading(self) -> Parasha:
        """Return number of hebrew parasha."""
        _year_type = (HebrewDate.year_size(self.hdate.year) % 10) - 3
        rosh_hashana = HebrewDate(self.hdate.year, Months.TISHREI, 1)
        pesach = HebrewDate(self.hdate.year, Months.NISAN, 15)
        year_type = (
            self.diaspora * 1000
            + rosh_hashana.dow() * 100
            + _year_type * 10
            + pesach.dow()
        )

        _LOGGER.debug("Year type: %d", year_type)

        # Number of days since rosh hashana
        days = (self.hdate - rosh_hashana).days
        # Number of weeks since rosh hashana
        weeks = (days + rosh_hashana.dow() - 1) // 7
        _LOGGER.debug("Since Rosh Hashana - Days: %d, Weeks %d", days, weeks)

        # If it's currently Simchat Torah, return VeZot Haberacha.
        if weeks == 3:
            if (
                days <= 22
                and self.diaspora
                and self.dow != Weekday.SATURDAY
                or days <= 21
                and not self.diaspora
            ):
                return Parasha.VEZOT_HABRACHA

        # Special case for Simchat Torah in diaspora.
        if weeks == 4 and days == 22 and self.diaspora:
            return Parasha.VEZOT_HABRACHA

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
