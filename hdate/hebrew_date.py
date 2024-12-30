"""Pure Hebrew date class."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Union

import hdate.converters as conv
from hdate.htables import Months
from hdate.translator import TranslatorMixin


def get_chalakim(hours: int, parts: int) -> int:
    """Return the number of total parts (chalakim)."""
    return (hours * PARTS_IN_HOUR) + parts


PARTS_IN_HOUR = 1080
PARTS_IN_DAY = 24 * PARTS_IN_HOUR
PARTS_IN_WEEK = 7 * PARTS_IN_DAY
PARTS_IN_MONTH = PARTS_IN_DAY + get_chalakim(12, 793)  # Fix for regular month


@dataclass
class HebrewDate(TranslatorMixin):
    """Define a Hebrew date object."""

    year: int = 0
    month: Union[Months, int] = Months.TISHREI
    day: int = 1

    def __post_init__(self) -> None:
        if not 0 < self.day < 31:
            raise ValueError(f"day ({self.day}) legal values are 1-30")
        self.month = (
            self.month if isinstance(self.month, Months) else Months(self.month)
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
        days = other.days  # Number of days to add
        day, month, year = self.day, self.month, self.year
        while days > 0:
            days_left_in_month = self.get_month_days(Months(month), year) - day
            if days_left_in_month > days:
                day += days
                break
            days -= days_left_in_month
            day = 1
            month = self.get_next_month(Months(month), year)
            if month == Months.TISHREI:
                year += 1

        return HebrewDate(year, month, day)

    def __sub__(self, other: object) -> dt.timedelta:
        if not isinstance(other, HebrewDate):
            return NotImplemented
        days = self.to_jdn() - other.to_jdn()
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

    def get_month_days(self, month: Months, year: int) -> int:
        """Return the number of days in a month."""
        if month in (
            Months.TISHREI,
            Months.SHVAT,
            Months.ADAR_I,
            Months.NISAN,
            Months.SIVAN,
            Months.AV,
        ):
            return 30
        if month in (
            Months.TEVET,
            Months.ADAR,
            Months.ADAR_II,
            Months.IYYAR,
            Months.TAMMUZ,
            Months.ELUL,
        ):
            return 29
        if month == Months.KISLEV:
            return 29 if HebrewDate.year_size(year) in (353, 383) else 30
        if month == Months.MARCHESHVAN:
            return 30 if HebrewDate.year_size(year) in (355, 385) else 29
        return 0

    def get_next_month(self, month: Months, year: int) -> Months:
        """Return the next month."""

        def is_leap(year: int) -> bool:
            return year % 19 in (0, 3, 6, 8, 11, 14, 17)

        if is_leap(year):
            if month == Months.SHVAT:
                return Months.ADAR_I
            if month == Months.ADAR_I:
                return Months.ADAR_II
            if month == Months.ADAR_II:
                return Months.NISAN
        next_month = month + 1 if month < Months.ELUL else Months.TISHREI
        return Months(next_month)
