"""Methods for going back and forth between various calendars."""

import datetime

from hdate.hebrew_date import HebrewDate
from hdate.htables import Months


def get_chalakim(hours, parts):
    """Return the number of total parts (chalakim)."""
    return (hours * PARTS_IN_HOUR) + parts


PARTS_IN_HOUR = 1080
PARTS_IN_DAY = 24 * PARTS_IN_HOUR
PARTS_IN_WEEK = 7 * PARTS_IN_DAY
PARTS_IN_MONTH = PARTS_IN_DAY + get_chalakim(12, 793)  # Fix for regular month


def _days_from_3744(hebrew_year):
    """Return: Number of days since 3,1,3744."""
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

    # pylint: disable=too-many-boolean-expressions
    # pylint-comment: Splitting the 'if' below might create a bug in case
    # the order is not kept.

    # Molad ד"ר ט"ג
    if (
        (
            leap_left < 12
            and week_day == 3
            and parts_left_in_day >= get_chalakim(9 + 6, 204)
        )
        or
        # Molad ט"פקת ו"טב
        (
            leap_left < 7
            and week_day == 2
            and parts_left_in_day >= get_chalakim(15 + 6, 589)
        )
    ):
        days += 1
        week_day += 1

    # pylint: enable=too-many-boolean-expressions

    # ADU
    if week_day in (1, 4, 6):
        days += 1

    return days


def get_size_of_hebrew_year(hebrew_year):
    """Return: total days in hebrew year."""
    return _days_from_3744(hebrew_year + 1) - _days_from_3744(hebrew_year)


def gdate_to_jdn(date):
    """
    Compute Julian day from Gregorian day, month and year.

    Algorithm from wikipedia's julian_day article.
    Return: The julian day number
    """
    not_jan_or_feb = (14 - date.month) // 12
    year_since_4800bc = date.year + 4800 - not_jan_or_feb
    month_since_4800bc = date.month + 12 * not_jan_or_feb - 3
    jdn = (
        date.day
        + (153 * month_since_4800bc + 2) // 5
        + 365 * year_since_4800bc
        + (year_since_4800bc // 4 - year_since_4800bc // 100 + year_since_4800bc // 400)
        - 32045
    )
    return jdn


def hdate_to_jdn(date):
    """
    Compute Julian day from Hebrew day, month and year.

    Return: julian day number,
            1 of tishrey julians,
            1 of tishrey julians next year
    """
    day = date.day
    month = date.month.value
    if date.month == Months.ADAR_I:
        month = 6
    if date.month == Months.ADAR_II:
        month = 6
        day += 30

    # Calculate days since 1,1,3744
    day = _days_from_3744(date.year) + (59 * (month - 1) + 1) // 2 + day

    # length of year
    length_of_year = get_size_of_hebrew_year(date.year)
    # Special cases for this year
    if length_of_year % 10 > 4 and month > 2:  # long Heshvan
        day += 1
    if length_of_year % 10 < 4 and month > 3:  # short Kislev
        day -= 1
    if length_of_year > 365 and month > 6:  # leap year
        day += 30

    # adjust to julian
    return day + 1715118


def jdn_to_gdate(jdn):
    """
    Convert from the Julian day to the Gregorian day.

    Algorithm from 'Julian and Gregorian Day Numbers' by Peter Meyer.
    Return: day, month, year
    """
    # pylint: disable=invalid-name

    # The algorithm is a verbatim copy from Peter Meyer's article
    # No explanation in the article is given for the variables
    # Hence the exceptions for pylint and for flake8 (E741)

    l = jdn + 68569  # noqa: E741
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4  # noqa: E741
    i = (4000 * (l + 1)) // 1461001  # that's 1,461,001
    l = l - (1461 * i) // 4 + 31  # noqa: E741
    j = (80 * l) // 2447
    day = l - (2447 * j) // 80
    l = j // 11  # noqa: E741
    month = j + 2 - (12 * l)
    year = 100 * (n - 49) + i + l  # that's a lower-case L

    return datetime.date(year, month, day)


def jdn_to_hdate(jdn):
    """Convert from the Julian day to the Hebrew day."""
    # calculate Gregorian date
    date = jdn_to_gdate(jdn)

    # Guess Hebrew year is Gregorian year + 3760
    year = date.year + 3760

    jdn_tishrey1 = hdate_to_jdn(HebrewDate(year, Months.TISHREI, 1))
    jdn_tishrey1_next_year = hdate_to_jdn(HebrewDate(year + 1, Months.TISHREI, 1))

    # Check if computed year was underestimated
    if jdn_tishrey1_next_year <= jdn:
        year = year + 1
        jdn_tishrey1 = jdn_tishrey1_next_year
        jdn_tishrey1_next_year = hdate_to_jdn(HebrewDate(year + 1, Months.TISHREI, 1))

    size_of_year = get_size_of_hebrew_year(year)

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
