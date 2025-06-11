"""Methods for going back and forth between Gregorian date and Julian day."""

import datetime as dt
from functools import lru_cache
from typing import Union


@lru_cache
def gdate_to_jdn(date: Union[dt.date, dt.datetime]) -> int:
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


@lru_cache
def jdn_to_gdate(jdn: int) -> dt.date:
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

    return dt.date(year, month, day)
