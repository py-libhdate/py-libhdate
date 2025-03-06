"""Tests for the HebrewDate class."""

import datetime as dt
from typing import Optional

import pytest
from hypothesis import assume, example, given, strategies
from syrupy.assertion import SnapshotAssertion

from hdate.hebrew_date import (
    CHANGING_MONTHS,
    LONG_MONTHS,
    SHORT_MONTHS,
    HebrewDate,
    Months,
    is_leap_year,
    is_shabbat,
)
from tests.conftest import valid_hebrew_date

MIN_YEAR = 3762
MAX_YEAR = 6000


def test_is_leap_year() -> None:
    """Test that is_leap_year() working as expected for leap year."""
    leap_date = HebrewDate(5784, Months.TISHREI, 1)
    assert leap_date.is_leap_year()


def test_is_not_leap_year() -> None:
    """Test that is_leap_year() working as expected for non-leap year."""
    leap_date = HebrewDate(5783, Months.TISHREI, 1)
    assert not leap_date.is_leap_year()


@given(date=strategies.datetimes())
def test_is_shabbat(date: dt.date) -> None:
    """Test that is_shabbat woirks correctly for both Hebrew and Gregorian dates."""
    assert is_shabbat(date) == is_shabbat(HebrewDate.from_gdate(date))


@given(
    month=strategies.sampled_from(Months),
    year=strategies.integers(min_value=MIN_YEAR, max_value=MAX_YEAR),
)
def test_next_prev_month(month: Months, year: int) -> None:
    """Test that next_month() and prev_month() work as expected."""
    assume(month in Months.in_year(year))
    next_month = month.next_month(year)
    assert next_month.prev_month(year) == month
    assert next_month != month
    if next_month != Months.TISHREI:
        assert next_month > month
    if month != Months.ELUL:
        assert month < next_month


@given(strategies.integers(min_value=MIN_YEAR, max_value=MAX_YEAR))
def test_get_all_months(year: int) -> None:
    """Test that all months are returned."""
    if is_leap_year(year):
        assert len(Months.in_year(year)) == 13
        assert all(m != Months.ADAR for m in Months.in_year(year))
        assert any(m in {Months.ADAR_I, Months.ADAR_II} for m in Months.in_year(year))
    else:
        assert len(Months.in_year(year)) == 12
        assert all(
            m not in {Months.ADAR_I, Months.ADAR_II} for m in Months.in_year(year)
        )
        assert any(m == Months.ADAR for m in Months.in_year(year))


@given(strategies.integers(min_value=MIN_YEAR, max_value=MAX_YEAR))
def test_sum_all_month_days(year: int) -> None:
    """Test that the sum of all days in all months is correct."""
    if is_leap_year(year):
        assert sum(m.days(year) for m in Months.in_year(year)) in {383, 384, 385}
    else:
        assert sum(m.days(year) for m in Months.in_year(year)) in {353, 354, 355}


def test_lists_of_months() -> None:
    """Test that the lists of months are correct."""
    assert set(LONG_MONTHS) == {
        Months.TISHREI,
        Months.SHVAT,
        Months.ADAR_I,
        Months.NISAN,
        Months.SIVAN,
        Months.AV,
    }
    assert set(SHORT_MONTHS) == {
        Months.TEVET,
        Months.ADAR,
        Months.ADAR_II,
        Months.IYYAR,
        Months.TAMMUZ,
        Months.ELUL,
    }
    assert CHANGING_MONTHS == (Months.MARCHESHVAN, Months.KISLEV)


def test_months_order() -> None:
    """Test that the months are in the correct order."""
    assert Months.TISHREI < Months.MARCHESHVAN < Months.KISLEV < Months.TEVET
    assert Months.TEVET < Months.SHVAT < Months.ADAR < Months.NISAN < Months.IYYAR
    assert Months.IYYAR < Months.SIVAN < Months.TAMMUZ < Months.AV < Months.ELUL
    assert Months.SHVAT < Months.ADAR_I < Months.ADAR_II < Months.NISAN


@pytest.mark.parametrize(
    "month, expected",
    [(Months.IYYAR, 29), (Months.TISHREI, 30), (Months.MARCHESHVAN, None)],
)
def test_get_months_days_no_year(month: Months, expected: Optional[int]) -> None:
    """Call the days method on the months without the year value."""
    if isinstance(expected, int):
        assert month.days() == expected
    else:
        with pytest.raises(ValueError):
            assert month.days() == expected


@given(strategies.integers(min_value=1, max_value=14))
def test_date_assign_int_months(value: int) -> None:
    """Test that assignment of an integet to Monts works as expected."""
    date = HebrewDate(month=value)  # type: ignore
    month = Months(value)  # type: ignore  # pylint: disable=E1120
    assert date == HebrewDate(month=month)
    assert isinstance(date.month, Months)


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


@given(
    d1=valid_hebrew_date(),
    days=strategies.integers(min_value=-500, max_value=500),
)
@example(d1=HebrewDate(4000, Months.SHVAT, 1), days=30)
def test_hebrew_date_addition(d1: HebrewDate, days: int) -> None:
    """Test HebrewDate addition and subtraction."""
    delta = dt.timedelta(days=days)
    d2 = d1 + delta
    assert d2 - d1 == delta
    negative_delta = dt.timedelta(days=-days)
    assert d2 + negative_delta == d1


@pytest.mark.xfail(reason="Will fail if relative date does not exist in current year.")
@given(d1=valid_hebrew_date(), d2=relative_hebrew_date())
@example(d2=HebrewDate(0, Months.MARCHESHVAN, 30))
def test_hebrew_date_addition_with_no_year(d1: HebrewDate, d2: HebrewDate) -> None:
    """Test HebrewDate addition and subtraction when there is no year."""
    diff = d2 - d1
    assert d1 + diff == d2


def test_to_jdn_snapshot(snapshot: SnapshotAssertion) -> None:
    """Test the to_jdn method."""
    assert HebrewDate(5785, Months.TEVET, 5).to_jdn() == snapshot


def test_from_jdn_snapshot(snapshot: SnapshotAssertion) -> None:
    """Test the from_jdn method."""
    assert HebrewDate.from_jdn(2451545) == snapshot


def test_to_gdate_snapshot(snapshot: SnapshotAssertion) -> None:
    """Test the to_gdate method."""
    assert HebrewDate(5785, Months.TEVET, 5).to_gdate() == snapshot


def test_from_gdate_snapshot(snapshot: SnapshotAssertion) -> None:
    """Test the from_gdate method."""
    assert HebrewDate.from_gdate(dt.date(2025, 1, 5)) == snapshot
