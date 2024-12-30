"""Tests for the HebrewDate class."""

from hypothesis import given, strategies

from hdate.hebrew_date import HebrewDate
from hdate.htables import Months

MIN_YEAR = 1
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

    days = HebrewDate(year).get_month_days(month)
    day = draw(strategies.integers(min_value=1, max_value=days))

    return HebrewDate(year, month, day)


@given(d1=valid_hebrew_date(), d2=valid_hebrew_date())
def test_hebrew_date_comparisons(d1: HebrewDate, d2: HebrewDate) -> None:
    """Test that the HebrewDate class implements all comparison operators correctly."""
    assert (d1 == d2) == ((d1.year, d1.month, d1.day) == (d2.year, d2.month, d2.day))
    assert (d1 < d2) == ((d1.year, d1.month, d1.day) < (d2.year, d2.month, d2.day))
    assert (d1 > d2) == ((d1.year, d1.month, d1.day) > (d2.year, d2.month, d2.day))
    assert (d1 <= d2) == ((d1.year, d1.month, d1.day) <= (d2.year, d2.month, d2.day))
    assert (d1 >= d2) == ((d1.year, d1.month, d1.day) >= (d2.year, d2.month, d2.day))
