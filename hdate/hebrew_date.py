"""Pure Hebrew date class."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING, Callable, Optional, Union, cast

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


class ComparisonMode(IntFlag):
    """Enum class for the comparison modes."""

    STRICT: tuple[int, set[int]] = 0, set()
    ADAR_IS_ADAR_I = 1, {6, 7}
    ADAR_IS_ADAR_II = 2, {6, 8}
    ADAR_IS_ANY = 3, {6 - 8}

    if TYPE_CHECKING:
        equal_month_values: set[int]

    def __new__(cls, value: int, equal_month_values: set[int]) -> ComparisonMode:
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.equal_month_values = equal_month_values
        return obj

    def __or__(self, other: object) -> ComparisonMode:
        if not isinstance(other, ComparisonMode):
            return NotImplemented
        value = super().__or__(other)
        value.equal_month_values = self.equal_month_values | other.equal_month_values
        return value


def short_kislev(year: int) -> bool:
    """Return whether this year has a short Kislev or not."""
    return HebrewDate.year_size(year) in (353, 383)


def long_cheshvan(year: int) -> bool:
    """Return whether this year has a long Cheshvan or not."""
    return HebrewDate.year_size(year) in (355, 385)


def is_leap_year(year: int) -> bool:
    """Return True if the Hebrew year is a leap year (2 Adars)"""
    return year % 19 in (0, 3, 6, 8, 11, 14, 17)


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
        obj.comparison_mode = ComparisonMode.STRICT
        return obj

    def __add__(self, value: object) -> Months:
        if not isinstance(value, int):
            return NotImplemented
        return Months(self._value_ + value)  # type: ignore # pylint: disable=E1120

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

    def set_comparison_mode(self, mode: ComparisonMode) -> None:
        """Set the comparison mode."""
        self.comparison_mode = mode

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
        mode = self.comparison_mode | other.comparison_mode

        if (
            self.value in mode.equal_month_values
            and other.value in mode.equal_month_values
        ):
            return 0
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


@dataclass
class HebrewDate(TranslatorMixin):
    """Define a Hebrew date object."""

    year: int = 0
    month: Union[Months, int] = Months.TISHREI
    day: int = 1

    def __post_init__(self) -> None:
        self.month = (
            self.month
            if isinstance(self.month, Months)
            else Months(self.month)  # type: ignore # pylint: disable=E1120
        )
        self._validate()
        self.month.set_language(self._language)

    def valid_for_year(self, year: int) -> bool:
        """Check if the date is valid for the given year."""
        try:
            self._validate(year)
        except ValueError:
            return False
        return True

    def _validate(self, year: int = 0) -> None:
        validate_months = True
        if self.year == 0 and year == 0:
            # Unable to validate Month, days of month for Cheshvan and Kislev are 30
            validate_months = False

        # Use the provided year to validate if it's not 0
        year = self.year if year == 0 else year
        if validate_months and self.month not in Months.in_year(year):
            raise ValueError(
                f"{self.month} is not a valid month for year {year} "
                f"({'leap' if is_leap_year(year) else 'non-leap'})"
            )
        if not 0 < self.day <= (max_days := cast(Months, self.month).days(year)):
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
            month = cast(Months, self.month)
        if day is None:
            day = self.day
        return type(self)(year, month, day)

    def __str__(self) -> str:
        """Return the hebrew date string in the selected language."""
        day = hebrew_number(self.day, language=self._language)
        year = hebrew_number(self.year, language=self._language)
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
        days = other.days
        new = type(self)(self.year, self.month, self.day)
        while days != 0:
            days_left = (
                cast(Months, new.month).days(new.year) - new.day
                if days > 0
                else new.day
            )

            if days_left >= abs(days):
                new.day += days
                break

            if days > 0:
                days -= days_left
                new.month = cast(Months, new.month).next_month(new.year)
                if new.month == Months.TISHREI:
                    new.year += 1
                new.day = 0
            else:
                days += days_left
                new.month = cast(Months, new.month).prev_month(new.year)
                if new.month == Months.ELUL:
                    new.year -= 1
                new.day = new.month.days(new.year)
        return new

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
    def from_gdate(date: dt.date) -> HebrewDate:
        """Return Hebrew date from Gregorian date."""
        return HebrewDate.from_jdn(conv.gdate_to_jdn(date))

    def to_gdate(self) -> dt.date:
        """Return Gregorian date from Hebrew date."""
        return conv.jdn_to_gdate(self.to_jdn())

    @staticmethod
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
        weekday.set_language(self._language)
        return weekday

    def short_kislev(self) -> bool:
        """Return whether this year has a short Kislev or not."""
        return short_kislev(self.year)

    def long_cheshvan(self) -> bool:
        """Return whether this year has a long Cheshvan or not."""
        return long_cheshvan(self.year)
