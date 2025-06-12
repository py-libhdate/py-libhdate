"""
Hebrew date meta-data.

HDateInfo allows querying various meta-data about Hebrew date, including
Holidays, Daf Yomi, Omer, and more.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from functools import cached_property
from typing import Union

from hdate.daf_yomi import DafYomiDatabase
from hdate.gematria import hebrew_number
from hdate.hebrew_date import HebrewDate, Weekday
from hdate.holidays import Holiday, HolidayDatabase, HolidayTypes
from hdate.omer import Omer
from hdate.parasha import ParashaDatabase
from hdate.tekufot import Nusachim, Tekufot
from hdate.translator import TranslatorMixin, get_language


@dataclass
class HDateInfo(TranslatorMixin):  # pylint: disable=too-many-instance-attributes
    """
    Hebrew date information class.

    Provides access to various properties of a given date.
    """

    date: Union[dt.date, HebrewDate] = field(default_factory=dt.date.today)
    diaspora: bool = False
    nusach: Nusachim = "sephardi"

    def __post_init__(self) -> None:
        # Initialize private variables
        self._last_updated = ""

        if isinstance(self.date, dt.date):
            self.gdate = self.date
            self._hdate = HebrewDate.from_gdate(self.date)
            self.date = self._hdate  # Replace self.date so comparison always works
        elif isinstance(self.date, HebrewDate):
            self.hdate = self.date
            self._gdate = self.date.to_gdate()
        else:
            raise TypeError("date has to be of type datetime.date or HebrewDate")

    @cached_property
    def _holidays(self) -> HolidayDatabase:
        """
        Return the HolidayDatabase instance.

        Use this as a cached property to avoid re-initializing and lazy load the
        database.
        """
        return HolidayDatabase(self.diaspora)

    def __str__(self) -> str:
        language = get_language()
        in_prefix = "ב" if language == "he" else ""
        day_number = hebrew_number(self.hdate.day)
        year_number = hebrew_number(self.hdate.year)
        result = (
            f"{self.hdate.dow()} "
            f"{day_number} {in_prefix}{self.hdate.month} {year_number}"
        )

        if self.omer.total_days > 0:
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
        return hdate

    @hdate.setter
    def hdate(self, date: HebrewDate) -> None:
        """Set the dates of the HDateInfo object based on a given Hebrew date."""

        if not isinstance(date, HebrewDate):
            raise TypeError(f"date: {date} is not of type HebrewDate")

        self._last_updated = "hdate"
        self._hdate = date

    @property
    def gdate(self) -> dt.date:
        """Return the Gregorian date for the given Hebrew date."""
        if self._last_updated == "gdate":
            return self._gdate
        return self._hdate.to_gdate()

    @gdate.setter
    def gdate(self, date: dt.date) -> None:
        """Set the Gregorian date for the given Hebrew date."""
        self._last_updated = "gdate"
        self._gdate = date

    @property
    def omer(self) -> Omer:
        """Return the Omer object."""
        return Omer(date=self.hdate)

    @property
    def parasha(self) -> str:
        """Return the upcoming parasha."""
        db = ParashaDatabase(self.diaspora)
        parasha = db.lookup(self.hdate)
        return str(parasha)

    @property
    def holidays(self) -> list[Holiday]:
        """Return the abstract holiday information from holidays table."""
        return self._holidays.lookup(self.hdate)

    @property
    def daf_yomi(self) -> str:
        """Return the daf yomi for the given date."""
        db = DafYomiDatabase()
        daf = db.lookup(self.gdate)
        return str(daf)

    @property
    def gevurot_geshamim(self) -> str:
        """Return the rain prayer (Tal uMatar, veTen Beracha, ...)."""
        tekufot = Tekufot(self.gdate, self.diaspora, self.nusach)
        return tekufot.get_prayer_for_date()

    @property
    def is_shabbat(self) -> bool:
        """Return True if this date is Shabbat.

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
    def next_day(self) -> HDateInfo:
        """Return the HDateInfo for the next day."""
        return HDateInfo(self.gdate + dt.timedelta(1), self.diaspora)

    @property
    def previous_day(self) -> HDateInfo:
        """Return the HDateInfo for the previous day."""
        return HDateInfo(self.gdate + dt.timedelta(-1), self.diaspora)

    @property
    def upcoming_shabbat(self) -> HDateInfo:
        """Return the HDateInfo for either the upcoming or current Shabbat."""
        if self.is_shabbat:
            return self

        next_shabbat = self.gdate + dt.timedelta(Weekday.SATURDAY - self.hdate.dow())
        return HDateInfo(next_shabbat, self.diaspora)

    @property
    def upcoming_erev_shabbat(self) -> HDateInfo:
        """Return the HDateInfo for the upcoming or current Erev Shabbat (Friday)."""
        return self.upcoming_shabbat.previous_day

    @property
    def upcoming_yom_tov(self) -> HDateInfo:
        """Return the HDateInfo for the upcoming or current Yom Tov."""
        if self.is_yom_tov:
            return self

        date = self._holidays.lookup_next_holiday(self.hdate, [HolidayTypes.YOM_TOV])

        return HDateInfo(date, self.diaspora)

    @property
    def upcoming_erev_yom_tov(self) -> HDateInfo:
        """Return the HDateInfo for the upcoming or current Erev Yom Tov."""
        if self.next_day.is_yom_tov:
            return self
        if self.is_yom_tov:  # Tomorrow is not yom tov, get next erev yom tov
            return self.next_day.upcoming_erev_yom_tov
        return self.upcoming_yom_tov.previous_day

    @property
    def upcoming_shabbat_or_yom_tov(self) -> HDateInfo:
        """Return the HDateInfo for the upcoming or current Shabbat or Yom Tov."""
        if self.is_shabbat or self.is_yom_tov:
            return self

        if self.upcoming_yom_tov.gdate < self.upcoming_shabbat.gdate:
            return self.upcoming_yom_tov
        return self.upcoming_shabbat

    @property
    def upcoming_erev_shabbat_or_erev_yom_tov(self) -> HDateInfo:
        """Return the HDateInfo for upcoming or current Erev Shabbat or Erev Yom Tov."""
        return self.upcoming_shabbat_or_yom_tov.previous_day

    @property
    def first_day(self) -> HDateInfo:
        """Return the first day of Yom Tov or Shabbat.

        This is useful for three-day holidays, for example: it will return the
        first in a string of Yom Tov + Shabbat.
        If this HDateInfo is Shabbat followed by no Yom Tov, returns the Saturday.
        If this HDateInfo is neither Yom Tov, nor Shabbat, this just returns
        itself.
        """
        day_iter = self
        while day_iter.previous_day.is_yom_tov or day_iter.previous_day.is_shabbat:
            day_iter = day_iter.previous_day
        return day_iter

    @property
    def last_day(self) -> HDateInfo:
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
