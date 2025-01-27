"""Tests relating to Sefirat HaOmer."""

import pytest
from hypothesis import given, strategies
from syrupy.assertion import SnapshotAssertion

from hdate import HDate, HebrewDate
from hdate.hebrew_date import Months
from hdate.omer import Nusach, Omer
from tests.conftest import valid_hebrew_date


@pytest.mark.parametrize("nusach", list(Nusach))
@pytest.mark.parametrize("language", ["hebrew", "english", "french"])
def test_get_omer(language: str, nusach: Nusach, snapshot: SnapshotAssertion) -> None:
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
    omer = HDate(date).omer
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
    omer = HDate(date).omer
    assert omer is None
