"""Tests relating to Sefirat HaOmer."""

import datetime as dt
import typing

import pytest
from hypothesis import given, strategies
from syrupy.assertion import SnapshotAssertion

from hdate import HDateInfo, HebrewDate
from hdate.hebrew_date import Months
from hdate.omer import Nusach, Omer
from hdate.translator import Language
from tests.conftest import valid_hebrew_date


@pytest.mark.parametrize("nusach", list(Nusach))
@pytest.mark.parametrize("language", typing.get_args(Language))
def test_get_omer(
    language: Language, nusach: Nusach, snapshot: SnapshotAssertion
) -> None:
    """Test the value returned by calculating the Omer."""
    for omer_day in range(50):
        omer = Omer(total_days=omer_day, language=language, nusach=nusach)
        assert omer.count_str() == snapshot


@given(
    strategies.one_of(
        strategies.integers(max_value=-1), strategies.integers(min_value=50)
    )
)
def test_illegal_value(days: int) -> None:
    """Test passing illegal values to Omer."""
    with pytest.raises(ValueError):
        Omer(total_days=days)


@given(
    date=valid_hebrew_date().filter(  # pylint: disable=no-member
        lambda d: HebrewDate(0, Months.NISAN, 15) < d < HebrewDate(0, Months.SIVAN, 6)
    )
)
def test_valid_omer_day(date: HebrewDate) -> None:
    """Test valid value of the Omer."""
    omer = HDateInfo(date).omer
    assert omer is not None
    assert omer.total_days == (date - HebrewDate(0, Months.NISAN, 15)).days


@given(
    date=valid_hebrew_date().filter(  # pylint: disable=no-member
        lambda d: d <= HebrewDate(0, Months.NISAN, 15)
        or HebrewDate(0, Months.SIVAN, 6) <= d
    )
)
def test_invalid_omer_day(date: HebrewDate) -> None:
    """Test invalid value of the Omer."""
    omer = HDateInfo(date).omer
    assert omer is None


@given(
    weeks=strategies.integers(min_value=0, max_value=6),
    day=strategies.integers(min_value=1, max_value=7),
)
def test_omer_by_week_and_day(weeks: int, day: int) -> None:
    """Test Omer by week and day."""
    omer = Omer(week=weeks, day=day)
    assert omer.total_days == weeks * 7 + day
    assert omer.date == HebrewDate(0, Months.NISAN, 16) + dt.timedelta(
        days=omer.total_days - 1
    )


def test_omer_str(snapshot: SnapshotAssertion) -> None:
    """Test the string representation of the Omer."""
    assert str(Omer(total_days=0)) == snapshot
    assert str(Omer(total_days=25)) == snapshot
    assert str(Omer(total_days=25, nusach=Nusach.ASHKENAZ)) == snapshot
