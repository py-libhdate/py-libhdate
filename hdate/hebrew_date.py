"""Pure Hebrew date class."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import IntEnum
from functools import cache, lru_cache
from typing import TYPE_CHECKING, Callable, Literal, Optional, Union

import hdate.converters as conv
from hdate.gematria import hebrew_number
from hdate.translator import TranslatorMixin


def get_chalakim(hours: int, parts: int) -> int:
    """Return the number of total parts (chalakim)."""
    return (hours * PARTS_IN_HOUR) + parts


PARTS_IN_HOUR = 1080
PARTS_IN_DAY = 24 * PARTS_IN_HOUR
PARTS_IN_WEEK = 7 * PARTS_IN_DAY
PARTS_IN_MONTH = PARTS_IN_DAY + get_chalakim(12, 793)  # Fix for regular month


class Weekday(TranslatorMixin, IntEnum):
    """Enum class for the days of the week."""

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7


def short_kislev(year: int) -> bool:
    """Return whether this year has a short Kislev or not."""
    return HebrewDate.year_size(year) in (353, 383)


def long_cheshvan(year: int) -> bool:
    """Return whether this year has a long Cheshvan or not."""
    return HebrewDate.year_size(year) in (355, 385)


def is_leap_year(year: int) -> bool:
    """Return True if the Hebrew year is a leap year (2 Adars)"""
    return year % 19 in (0, 3, 6, 8, 11, 14, 17)


@lru_cache
def is_shabbat(date: Union[dt.date, HebrewDate]) -> bool:
    """Return whether a date is shabbat."""
    if isinstance(date, dt.date):
        return date.weekday() == 5
    return date.dow() == Weekday.SATURDAY


class Months(TranslatorMixin, IntEnum):
    """Enum class for the Hebrew months."""

    TISHREI = 1, 7, 30
    MARCHESHVAN = 2, 8, lambda year: 30 if long_cheshvan(year) or (year == 0) else 29
    KISLEV = 3, 9, lambda year: 30 if not short_kislev(year) or (year == 0) else 29
    TEVET = 4, 10, 29
    SHVAT = 5, 11, 30
    ADAR = 6, 12, 29  # Adar in a non-leap year
    ADAR_I = 7, 12, 30  # Adar I in a leap year
    ADAR_II = 8, 13, 29
    NISAN = 9, 1, 30
    IYYAR = 10, 2, 29
    SIVAN = 11, 3, 30
    TAMMUZ = 12, 4, 29
    AV = 13, 5, 30
    ELUL = 14, 6, 29

    if TYPE_CHECKING:
        biblical_order: int
        length: Union[int, Callable[[int], int]]

    def __new__(
        cls, value: int, ordinal: int, days: Union[int, Callable[[int], int]]
    ) -> Months:
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.biblical_order = ordinal
        obj.length = days
        return obj

    def next_month(self, year: int) -> Months:
        """Return the next month."""
        if self == Months.ELUL:
            return Months.TISHREI
        if self in {Months.ADAR, Months.ADAR_II}:
            return Months.NISAN
        if is_leap_year(year) and self == Months.SHVAT:
            return Months.ADAR_I
        return Months(self._value_ + 1)  # type: ignore # pylint: disable=E1120

    def prev_month(self, year: int) -> Months:
        """Return the previous month."""
        if self == Months.TISHREI:
            return Months.ELUL
        if self == Months.NISAN:
            return Months.ADAR_II if is_leap_year(year) else Months.ADAR
        if is_leap_year(year) and self == Months.ADAR_I:
            return Months.SHVAT
        return Months(self._value_ - 1)  # type: ignore # pylint: disable=E1120

    @classmethod
    def in_year(cls, year: int) -> list[Months]:
        """Return the months for the given year."""
        if is_leap_year(year):
            return [month for month in cls if month != Months.ADAR]
        return [month for month in cls if month not in (Months.ADAR_I, Months.ADAR_II)]

    def days(self, year: Optional[int] = None) -> int:
        """Return the number of days in this month."""
        if callable(self.length):
            if year is None:
                raise ValueError("Year is required to calculate days for this month")
            return self.length(year)
        return self.length

    def compare(self, other: Union[Months, int], order_type: str = "calendar") -> int:
        """
        Compare this month to another month.

        The comparison can be either "calendar" or "biblical". When using the biblical
        order, we consider NISAN as the first month. By default, we use the calendar
        order starting at TISHREI.
        """
        value = self.value if order_type == "calendar" else self.biblical_order

        if not isinstance(other, Months):
            return value - other

        other_value = other.value if order_type == "calendar" else other.biblical_order

        return value - other_value

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, (Months, int)):
            return NotImplemented
        return self.compare(value) == 0

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (Months, int)):
            return NotImplemented
        return self.compare(other) < 0

    def __le__(self, other: object) -> bool:
        if not isinstance(other, (Months, int)):
            return NotImplemented
        return self.compare(other) <= 0

    def __hash__(self) -> int:
        return IntEnum.__hash__(self)


LONG_MONTHS = tuple(month for month in Months if month.length == 30)
SHORT_MONTHS = tuple(month for month in Months if month.length == 29)
CHANGING_MONTHS = tuple(month for month in Months if callable(month.length))


@dataclass(frozen=True)
class HebrewDate(TranslatorMixin):
    """Define a Hebrew date object."""

    year: int = 0
    month: Months = Months.TISHREI
    day: int = 1

    def __post_init__(self) -> None:
        if isinstance(self.month, int):
            object.__setattr__(
                self,
                "month",
                Months(self.month),  # type: ignore # pylint: disable=E1120
            )
        self._validate()

    def valid_for_year(self, year: int) -> bool:
        """Check if the date is valid for the given year."""
        try:
            self._validate(year)
        except ValueError:
            return False
        return True

    def _validate(self, year: int = 0) -> None:
        """Validation method. Accepts a specific year to validate against."""
        # Unable to validate Month, days of month for Cheshvan and Kislev are 30
        validate_months = not (self.year == 0 and year == 0)

        # Use the provided year to validate if it's not 0
        year = self.year if year == 0 else year
        if validate_months and self.month not in Months.in_year(year):
            raise ValueError(
                f"{self.month} is not a valid month for year {year} "
                f"({'leap' if is_leap_year(year) else 'non-leap'})"
            )
        max_days = self.month.days(year)
        if not 0 < self.day <= max_days:
            raise ValueError(
                f"Day {self.day} is illegal: "
                f"legal values are 1-{max_days} for {self.month}"
            )

    def replace(
        self,
        year: Optional[int] = None,
        month: Optional[Months] = None,
        day: Optional[int] = None,
    ) -> HebrewDate:
        """Return a new HebrewDate with a different year/month/day."""
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        return type(self)(year, month, day)

    def __str__(self) -> str:
        day = hebrew_number(self.day)
        year = hebrew_number(self.year)
        return f"{day} {self.month} {year}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HebrewDate):
            return NotImplemented
        if self.year == 0 or other.year == 0:
            return (self.month, self.day) == (other.month, other.day)
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, HebrewDate):
            return NotImplemented
        if self.year == 0 or other.year == 0:
            return (self.month, self.day) < (other.month, other.day)
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, HebrewDate):
            return NotImplemented
        return self < other or self == other

    def __add__(self, other: object) -> HebrewDate:
        if not isinstance(other, dt.timedelta):
            return NotImplemented

        def _adjust_date(
            year: int,
            month: Months,
            day: int,
            direction: Literal["forward", "backward"],
        ) -> tuple[int, Months, int]:
            """Adjust the date based on the direction."""
            if direction == "forward":
                month = month.next_month(_year)
                if month == Months.TISHREI:
                    year += 1
                day = 0
            else:
                month = month.prev_month(_year)
                if month == Months.ELUL:
                    year -= 1
                day = month.days(_year)
            return year, month, day

        days = other.days
        _year, _month, _day = self.year, self.month, self.day
        while days != 0:
            days_left = _month.days(_year) - _day if days > 0 else _day

            if days_left >= abs(days):
                _day += days
                if _day == 0:
                    _year, _month, _day = _adjust_date(_year, _month, _day, "backward")
                break

            if days > 0:
                days -= days_left
                _year, _month, _day = _adjust_date(_year, _month, _day, "forward")
            else:
                days += days_left
                _year, _month, _day = _adjust_date(_year, _month, _day, "backward")
        return type(self)(_year, _month, _day)

    def __sub__(self, other: object) -> dt.timedelta:
        if not isinstance(other, HebrewDate):
            return NotImplemented
        if self.year == 0 or other.year == 0:
            adjusted_year = max(self.year, other.year)
            local_self = HebrewDate(adjusted_year, self.month, self.day)
            local_other = HebrewDate(adjusted_year, other.month, other.day)
        else:
            local_self = self
            local_other = other
        days = local_self.to_jdn() - local_other.to_jdn()
        return dt.timedelta(days=days)

    def __hash__(self) -> int:
        return hash((self.year, self.month, self.day))

    def to_jdn(self) -> int:
        """Compute Julian day number from HebrewDate."""
        month = Months.TISHREI
        day = HebrewDate._days_from_3744(self.year)
        while month != self.month:
            day += self.days_in_month(month)
            month = month.next_month(self.year)
        day += self.day
        return day + 1715118

    @staticmethod
    @lru_cache
    def from_jdn(jdn: int) -> HebrewDate:
        """Convert from the Julian day to the Hebrew day."""
        # calculate Gregorian date
        date = conv.jdn_to_gdate(jdn)

        # Guess Hebrew year is Gregorian year + 3760
        year = date.year + 3760

        rosh_hashana = HebrewDate(year, Months.TISHREI, 1)

        # Check if computed year was underestimated
        if HebrewDate(year + 1, Months.TISHREI, 1).to_jdn() <= jdn:
            rosh_hashana = HebrewDate(year + 1, Months.TISHREI, 1)

        days = dt.timedelta(days=jdn - rosh_hashana.to_jdn())

        return rosh_hashana + days

    @staticmethod
    @lru_cache
    def from_gdate(date: dt.date) -> HebrewDate:
        """Return Hebrew date from Gregorian date."""
        return HebrewDate.from_jdn(conv.gdate_to_jdn(date))

    def to_gdate(self) -> dt.date:
        """Return Gregorian date from Hebrew date."""
        return conv.jdn_to_gdate(self.to_jdn())

    @staticmethod
    @cache
    def _days_from_3744(hebrew_year: int) -> int:
        """Return: Number of days since the molad of year 3744."""
        # Start point for calculation is Molad new year 3744 (16BC)
        years_from_3744 = hebrew_year - 3744
        molad_3744 = get_chalakim(1 + 6, 779)  # Molad 3744 + 6 hours in parts

        # Time in months

        # Number of leap months
        leap_months = (years_from_3744 * 7 + 1) // 19
        leap_left = (years_from_3744 * 7 + 1) % 19  # Months left of leap cycle
        months = years_from_3744 * 12 + leap_months  # Total Number of months

        # Time in parts and days
        # Molad This year + Molad 3744 - corrections
        parts = months * PARTS_IN_MONTH + molad_3744
        # 28 days in month + corrections
        days = months * 28 + parts // PARTS_IN_DAY - 2

        # Time left for round date in corrections
        # 28 % 7 = 0 so only corrections counts
        parts_left_in_week = parts % PARTS_IN_WEEK
        parts_left_in_day = parts % PARTS_IN_DAY
        week_day = parts_left_in_week // PARTS_IN_DAY

        # Molad ד"ר ט"ג
        molad_get_red = (
            leap_left < 12
            and week_day == 3
            and parts_left_in_day >= get_chalakim(9 + 6, 204)
        )

        # Molad ט"פקת ו"טב
        molad_betu_takpat = (
            leap_left < 7
            and week_day == 2
            and parts_left_in_day >= get_chalakim(15 + 6, 589)
        )

        if molad_get_red or molad_betu_takpat:
            days += 1
            week_day += 1

        # Lo Adu rosh
        if week_day in (1, 4, 6):
            days += 1

        return days

    @staticmethod
    @cache
    def year_size(hebrew_year: int) -> int:
        """Return: total days in hebrew year."""
        return HebrewDate._days_from_3744(hebrew_year + 1) - HebrewDate._days_from_3744(
            hebrew_year
        )

    def days_in_month(self, month: Months) -> int:
        """Return the number of days in a month."""
        return month.days(self.year)

    def is_leap_year(self) -> bool:
        """Return: True if the year is a leap year."""
        return is_leap_year(self.year)

    def dow(self) -> Weekday:
        """Return: day of the week."""
        weekday = Weekday((self.to_jdn() + 1) % 7 + 1)
        return weekday

    def short_kislev(self) -> bool:
        """Return whether this year has a short Kislev or not."""
        return short_kislev(self.year)

    def long_cheshvan(self) -> bool:
        """Return whether this year has a long Cheshvan or not."""
        return long_cheshvan(self.year)
