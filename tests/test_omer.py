"""Tests relating to Sefirat HaOmer."""

import pytest
from hypothesis import given, strategies
from syrupy.assertion import SnapshotAssertion

from hdate.omer import Omer


@pytest.mark.parametrize("omer_day", range(1, 50))
@pytest.mark.parametrize("language", ["hebrew", "english", "french"])
def test_get_omer(omer_day: int, language: str, snapshot: SnapshotAssertion) -> None:
    """Test the value returned by calculating the Omer."""
    omer = Omer(total_days=omer_day, language=language)
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
