"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a representation either in English, French or Hebrew
of the Jewish calendrical date and times for a given location
"""

from __future__ import annotations

import datetime as dt
from typing import Optional, Union

from hdate.daf_yomi import DafYomiDatabase, Masechta
from hdate.gematria import hebrew_number
from hdate.hebrew_date import HebrewDate, Weekday
from hdate.holidays import Holiday, HolidayDatabase, HolidayTypes
from hdate.omer import Omer
from hdate.parasha import Parasha, ParashaDatabase
from hdate.translator import TranslatorMixin


class HDate(TranslatorMixin):
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

    def __str__(self) -> str:
        """Return a full Unicode representation of HDate."""
        in_prefix = "ב" if self._language == "hebrew" else ""
        day_number = hebrew_number(self.hdate.day, language=self._language)
        year_number = hebrew_number(self.hdate.year, language=self._language)
        result = (
            f"{self.hdate.dow()} "
            f"{day_number} {in_prefix}{self.hdate.month} {year_number}"
        )

        if self.omer:
            result = f"{result} {self.omer}"

        if self.holidays:
            result = f"{result} {', '.join(str(holiday) for holiday in self.holidays)}"
        return result

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
    def omer(self) -> Optional[Omer]:
        """Return the Omer object."""
        _omer = Omer(date=self.hdate, language=self._language)
        return _omer if _omer.total_days > 0 else None

    @property
    def parasha(self) -> Parasha:
        """Return the upcoming parasha."""
        db = ParashaDatabase(self.diaspora)
        parasha = db.lookup(self.hdate)
        parasha.set_language(self._language)
        return parasha

    @property
    def holidays(self) -> list[Holiday]:
        """Return the abstract holiday information from holidays table."""
        holidays_list = HolidayDatabase(diaspora=self.diaspora).lookup(self.hdate)

        for holiday in holidays_list:
            holiday.set_language(self._language)

        return holidays_list

    @property
    def daf_yomi(self) -> Masechta:
        """Return a string representation of the daf yomi."""
        db = DafYomiDatabase()
        daf = db.lookup(self.gdate)
        daf.set_language(self._language)
        return daf

    @property
    def is_shabbat(self) -> bool:
        """Return True if this date is Shabbat, specifically Saturday.

        Returns False on Friday because the HDate object has no notion of time.
        For more detailed nuance, use the Zmanim object.
        """
        return self.hdate.dow() == Weekday.SATURDAY

    @property
    def is_holiday(self) -> bool:
        """Return True if this date is a holiday (any kind)."""
        return len(self.holidays) > 0

    @property
    def is_yom_tov(self) -> bool:
        """Return True if this date is a Yom Tov."""
        return any(holiday.type == HolidayTypes.YOM_TOV for holiday in self.holidays)

    @property
    def next_day(self) -> HDate:
        """Return the HDate for the next day."""
        return HDate(self.gdate + dt.timedelta(1), self.diaspora, self._language)

    @property
    def previous_day(self) -> HDate:
        """Return the HDate for the previous day."""
        return HDate(self.gdate + dt.timedelta(-1), self.diaspora, self._language)

    @property
    def upcoming_shabbat(self) -> HDate:
        """Return the HDate for either the upcoming or current Shabbat.

        If it is currently Shabbat, returns the HDate of the Saturday.
        """
        if self.is_shabbat:
            return self

        next_shabbat = self.gdate + dt.timedelta(Weekday.SATURDAY - self.hdate.dow())
        return HDate(next_shabbat, diaspora=self.diaspora, language=self._language)

    @property
    def upcoming_yom_tov(self) -> HDate:
        """Find the next upcoming yom tov (i.e. no-melacha holiday).

        If it is currently the day of yom tov (irrespective of zmanim), returns
        that yom tov.
        """
        if self.is_yom_tov:
            return self

        mgr = HolidayDatabase(diaspora=self.diaspora)
        date = mgr.lookup_next_holiday(self.hdate, [HolidayTypes.YOM_TOV])

        return HDate(date, self.diaspora, self._language)

    @property
    def upcoming_shabbat_or_yom_tov(self) -> HDate:
        """Return the HDate for the upcoming or current Shabbat or Yom Tov.

        If it is currently Shabbat, returns the HDate of the Saturday.
        If it is currently Yom Tov, returns the HDate of the first day
        (rather than "leil" Yom Tov). To access Leil Yom Tov, use
        upcoming_shabbat_or_yom_tov.previous_day.
        """
        if self.is_shabbat or self.is_yom_tov:
            return self

        if self.upcoming_yom_tov.gdate < self.upcoming_shabbat.gdate:
            return self.upcoming_yom_tov
        return self.upcoming_shabbat

    @property
    def first_day(self) -> HDate:
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
    def last_day(self) -> HDate:
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
