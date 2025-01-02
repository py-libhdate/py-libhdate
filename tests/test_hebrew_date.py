"""Tests for the HebrewDate class."""

import datetime as dt

import pytest
from hypothesis import given, strategies

from hdate.hebrew_date import HebrewDate
from hdate.htables import Months

MIN_YEAR = 3762
MAX_YEAR = 6000


@strategies.composite
def valid_hebrew_date(draw: strategies.DrawFn) -> HebrewDate:
    """Generate a valid Hebrew date."""
    year = draw(strategies.integers(min_value=MIN_YEAR, max_value=MAX_YEAR))

    months = list(Months)
    if HebrewDate(year).is_leap_year():
        months.remove(Months.ADAR)
    else:
        months.remove(Months.ADAR_I)
        months.remove(Months.ADAR_II)
    month = draw(strategies.sampled_from(months))

    days = HebrewDate(year).days_in_month(month)
    day = draw(strategies.integers(min_value=1, max_value=days))

    return HebrewDate(year, month, day)


@strategies.composite
def relative_hebrew_date(draw: strategies.DrawFn) -> HebrewDate:
    """Generate a Hebrew date with no year."""
    month = draw(strategies.sampled_from(list(Months)))
    max_day = HebrewDate().days_in_month(month)
    day = draw(strategies.integers(min_value=1, max_value=max_day))
    return HebrewDate(0, month, day)


@given(d1=valid_hebrew_date(), d2=valid_hebrew_date())
def test_hebrew_date_comparisons(d1: HebrewDate, d2: HebrewDate) -> None:
    """Test that the HebrewDate class implements all comparison operators correctly."""
    assert (d1 == d2) == ((d1.year, d1.month, d1.day) == (d2.year, d2.month, d2.day))
    assert (d1 != d2) == ((d1.year, d1.month, d1.day) != (d2.year, d2.month, d2.day))
    assert (d1 < d2) == ((d1.year, d1.month, d1.day) < (d2.year, d2.month, d2.day))
    assert (d1 > d2) == ((d1.year, d1.month, d1.day) > (d2.year, d2.month, d2.day))
    assert (d1 <= d2) == ((d1.year, d1.month, d1.day) <= (d2.year, d2.month, d2.day))
    assert (d1 >= d2) == ((d1.year, d1.month, d1.day) >= (d2.year, d2.month, d2.day))


@given(d1=valid_hebrew_date(), d2=relative_hebrew_date())
def test_relative_hebrew_date_comparisons(d1: HebrewDate, d2: HebrewDate) -> None:
    """Test HebrewDatecomparison operators when there is no year."""
    assert (d1 == d2) == ((d1.month, d1.day) == (d2.month, d2.day))
    assert (d1 != d2) == ((d1.month, d1.day) != (d2.month, d2.day))
    assert (d1 < d2) == ((d1.month, d1.day) < (d2.month, d2.day))
    assert (d1 > d2) == ((d1.month, d1.day) > (d2.month, d2.day))
    assert (d1 <= d2) == ((d1.month, d1.day) <= (d2.month, d2.day))
    assert (d1 >= d2) == ((d1.month, d1.day) >= (d2.month, d2.day))


@pytest.mark.xfail(reason="Needs support for leap years")
@given(
    d1=valid_hebrew_date(),
    days=strategies.integers(min_value=-500, max_value=500),
)
def test_hebrew_date_addition(d1: HebrewDate, days: int) -> None:
    """Test HebrewDate addition and subtraction."""
    delta = dt.timedelta(days=days)
    d2 = d1 + delta
    assert d2 - d1 == delta


@pytest.mark.xfail(reason="Needs support for leap years")
@given(d1=valid_hebrew_date(), d2=relative_hebrew_date())
def test_hebrew_date_addition_with_no_year(d1: HebrewDate, d2: HebrewDate) -> None:
    """Test HebrewDate addition and subtraction when there is no year."""
    diff = d2 - d1
    assert d1 + diff == d2
