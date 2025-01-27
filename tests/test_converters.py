"""Test the conversion functions."""

import datetime as dt

from hypothesis import given, strategies

from hdate import converters as conv
from hdate.hebrew_date import HebrewDate
from tests.conftest import valid_hebrew_date


@given(date=strategies.dates())
def test_gdate_to_gdate(date: dt.date) -> None:
    """ "Transform Gregorian date to Gregorian date."""
    assert conv.jdn_to_gdate(conv.gdate_to_jdn(date)) == date


@given(date=valid_hebrew_date())
def test_hdate_to_hdate(date: HebrewDate) -> None:
    """Transform Hebrew date to Hebrew date (single Adar)."""
    assert HebrewDate.from_jdn(date.to_jdn()) == date
