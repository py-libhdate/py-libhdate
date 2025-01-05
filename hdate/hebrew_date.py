"""Pure Hebrew date class."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import IntEnum
from typing import Union

import hdate.converters as conv
from hdate.translator import TranslatorMixin


def get_chalakim(hours: int, parts: int) -> int:
    """Return the number of total parts (chalakim)."""
    return (hours * PARTS_IN_HOUR) + parts


PARTS_IN_HOUR = 1080
PARTS_IN_DAY = 24 * PARTS_IN_HOUR
PARTS_IN_WEEK = 7 * PARTS_IN_DAY
PARTS_IN_MONTH = PARTS_IN_DAY + get_chalakim(12, 793)  # Fix for regular month


class Days(TranslatorMixin, IntEnum):
    """Enum class for the days of the week."""

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7


class Months(TranslatorMixin, IntEnum):
    """Enum class for the Hebrew months."""

    TISHREI = 1
    MARCHESHVAN = 2
    KISLEV = 3
    TEVET = 4
    SHVAT = 5
    ADAR = 6
    NISAN = 7
    IYYAR = 8
    SIVAN = 9
    TAMMUZ = 10
    AV = 11
    ELUL = 12
    ADAR_I = 13
    ADAR_II = 14


LONG_MONTHS = (
    Months.TISHREI,
    Months.SHVAT,
    Months.ADAR_I,
    Months.NISAN,
    Months.SIVAN,
    Months.AV,
)
SHORT_MONTHS = (
    Months.TEVET,
    Months.ADAR,
    Months.ADAR_II,
    Months.IYYAR,
    Months.TAMMUZ,
    Months.ELUL,
)
CHANGING_MONTHS = (Months.MARCHESHVAN, Months.KISLEV)


@dataclass
class HebrewDate(TranslatorMixin):
    """Define a Hebrew date object."""

    year: int = 0
    month: Union[Months, int] = Months.TISHREI
    day: int = 1

    def __post_init__(self) -> None:
        self.month = (
            self.month if isinstance(self.month, Months) else Months(self.month)
        )
        if self.year != 0:
            leap_year = self.is_leap_year()
            if (leap_year and self.month == Months.ADAR) or (
                not leap_year and self.month in (Months.ADAR_I, Months.ADAR_II)
            ):
                raise ValueError(
                    f"{self.month} is not a valid month for year {self.year} "
                    f"({'leap' if leap_year else 'non-leap'})"
                )
        if not 0 < self.day <= (max_days := self.days_in_month(self.month)):
            raise ValueError(
                f"Day {self.day} is illegal: "
                f"legal values are 1-{max_days} for {self.month}"
            )

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
        if self.year > 3760:  # Use gdate to calculate addition
            new_gdate = self.to_gdate() + other
            return HebrewDate.from_gdate(new_gdate)
        days = other.days
        new = HebrewDate(self.year, self.month, self.day)
        while days > 0:
            if (days_left := self.days_in_month(Months(new.month)) - new.day) > days:
                new.day += days
                break
            days -= days_left
            if new.month == Months.SHVAT and new.is_leap_year():
                new.month = Months.ADAR_I
            elif new.month == Months.ADAR_II:
                new.month = Months.NISAN
            elif new.month == Months.ELUL:
                new.year += 1
                new.month = Months.TISHREI
            else:
                new.month += 1
            new.day = 1
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

    def to_jdn(self) -> int:
        """
        Compute Julian day from Hebrew day, month and year.

        Return: julian day number
        """
        day = self.day
        month = self.month.value if isinstance(self.month, Months) else self.month

        if self.month == Months.ADAR_I:
            month = 6
        if self.month == Months.ADAR_II:
            month = 6
            day += 30

        # Calculate days since 1,1,3744
        day = HebrewDate._days_from_3744(self.year) + (59 * (month - 1) + 1) // 2 + day

        # length of year
        length_of_year = HebrewDate.year_size(self.year)
        # Special cases for this year
        if length_of_year % 10 > 4 and month > 2:  # long Heshvan
            day += 1
        if length_of_year % 10 < 4 and month > 3:  # short Kislev
            day -= 1
        if length_of_year > 365 and month > 6:  # leap year
            day += 30

        # adjust to julian
        return day + 1715118

    @staticmethod
    def from_jdn(jdn: int) -> HebrewDate:
        """Convert from the Julian day to the Hebrew day."""
        # calculate Gregorian date
        date = conv.jdn_to_gdate(jdn)

        # Guess Hebrew year is Gregorian year + 3760
        year = date.year + 3760

        jdn_tishrey1 = HebrewDate(year, Months.TISHREI, 1).to_jdn()
        jdn_tishrey1_next_year = HebrewDate(year + 1, Months.TISHREI, 1).to_jdn()

        # Check if computed year was underestimated
        if jdn_tishrey1_next_year <= jdn:
            year = year + 1
            jdn_tishrey1 = jdn_tishrey1_next_year
            jdn_tishrey1_next_year = HebrewDate(year + 1, Months.TISHREI, 1).to_jdn()

        size_of_year = HebrewDate.year_size(year)

        # days into this year, first month 0..29
        days = jdn - jdn_tishrey1

        # last 8 months always have 236 days
        if days >= (size_of_year - 236):  # in last 8 months
            days = days - (size_of_year - 236)
            month = days * 2 // 59
            day = days - (month * 59 + 1) // 2 + 1

            month = month + 4 + 1

            # if leap
            if size_of_year > 355 and month <= 6:
                month = month + 8
        else:  # in 4-5 first months
            # Special cases for this year
            if size_of_year % 10 > 4 and days == 59:  # long Heshvan (day 30)
                month = 1
                day = 30
            elif size_of_year % 10 > 4 and days > 59:  # long Heshvan
                month = (days - 1) * 2 // 59
                day = days - (month * 59 + 1) // 2
            elif size_of_year % 10 < 4 and days > 87:  # short kislev
                month = (days + 1) * 2 // 59
                day = days - (month * 59 + 1) // 2 + 2
            else:  # regular months
                month = days * 2 // 59
                day = days - (month * 59 + 1) // 2 + 1

            month = month + 1

        return HebrewDate(year, Months(month), day)

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
        if month in LONG_MONTHS:
            return 30
        if month in SHORT_MONTHS:
            return 29
        if self.year == 0 and month in CHANGING_MONTHS:
            # Special case for relative dates, return the maximum number of days
            return 30
        if month == Months.KISLEV:
            return 29 if self.short_kislev() else 30
        if month == Months.MARCHESHVAN:
            return 30 if self.long_cheshvan() else 29
        return 0

    def is_leap_year(self) -> bool:
        """Return: True if the year is a leap year."""
        return self.year % 19 in (0, 3, 6, 8, 11, 14, 17)

    def get_next_month(self, month: Months, year: int) -> Months:
        """Return the next month."""

        if HebrewDate(year).is_leap_year():
            if month == Months.SHVAT:
                return Months.ADAR_I
            if month == Months.ADAR_I:
                return Months.ADAR_II
            if month == Months.ADAR_II:
                return Months.NISAN
        next_month = month + 1 if month < Months.ELUL else Months.TISHREI
        return Months(next_month)

    def dow(self) -> Days:
        """Return: day of the week."""
        weekday = Days((self.to_jdn() + 1) % 7 + 1)
        weekday.set_language(self._language)
        return weekday

    def short_kislev(self) -> bool:
        """Return whether this year has a short Kislev or not."""
        return self.year_size(self.year) in (353, 383)

    def long_cheshvan(self) -> bool:
        """Return whether this year has a long Cheshvan or not."""
        return self.year_size(self.year) in (355, 385)
