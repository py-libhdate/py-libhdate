"""Tests dealing with parshat hashavua."""

import datetime as dt

import pytest
from hypothesis import given, settings, strategies
from syrupy.assertion import SnapshotAssertion

from hdate import HDate, HebrewDate
from hdate.hebrew_date import Months
from hdate.parasha import Parasha

YEAR_TYPES = [
    # שנים מעוברות
    # זשה
    5763,
    # זחג
    5757,
    # השג
    5774,
    # החא
    5768,
    # גכז
    5755,
    # בשז
    5776,
    # בחה
    5749,
    # שנים פשוטות
    # השא
    5754,
    # בשה
    5756,
    # זחא
    5761,
    # גכה
    5769,
    # זשג
    5770,
    # הכז
    5775,
    # בחג
    5777,
    5778,
]


@pytest.mark.parametrize("year", YEAR_TYPES)
@pytest.mark.parametrize("diaspora", [True, False])
def test_get_reading_israel(
    diaspora: bool, year: int, snapshot: SnapshotAssertion
) -> None:
    """Test parshat hashavua in Israel."""
    rosh_hashana = HebrewDate(year, Months.TISHREI, 1)
    mydate = HDate(rosh_hashana, diaspora=diaspora).upcoming_shabbat

    while mydate.hdate.year == year:
        print("Testing: ", mydate)
        assert mydate.parasha == snapshot
        mydate.gdate += dt.timedelta(7)


@pytest.mark.parametrize("year", YEAR_TYPES)
@pytest.mark.parametrize("diaspora", [True, False])
def test_vezot_habracha(diaspora: bool, year: int) -> None:
    """Test Vezot Habracha showing correctly."""
    if diaspora:
        simchat_tora = HebrewDate(year, Months.TISHREI, 23)
    else:
        simchat_tora = HebrewDate(year, Months.TISHREI, 22)
    mydate = HDate(simchat_tora, diaspora=diaspora)
    assert mydate.parasha == 54


@pytest.mark.parametrize("diaspora", [True, False])
@given(year=strategies.integers(min_value=4000, max_value=6000))
def test_nitzavim_always_before_rosh_hashana(year: int, diaspora: bool) -> None:
    """A property: Nitzavim alway falls before rosh hashana."""
    rosh_hashana = HebrewDate(year, Months.TISHREI, 1)
    previous_shabbat = rosh_hashana + dt.timedelta(days=-rosh_hashana.dow())
    mydate = HDate(previous_shabbat, diaspora=diaspora)
    print(f"Testing date: {mydate}")
    assert mydate.parasha in (Parasha.NITZAVIM, Parasha.NITZAVIM_VAYEILECH)


@pytest.mark.parametrize("diaspora", [True, False])
@given(year=strategies.integers(min_value=4000, max_value=6000))
@settings(deadline=None)  # Calculation of reading is slow
def test_vayelech_or_haazinu_always_after_rosh_hashana(
    year: int, diaspora: bool
) -> None:
    """A property: Vayelech or Haazinu always falls after rosh hashana."""
    rosh_hashana = HebrewDate(year, Months.TISHREI, 1)
    mydate = HDate(rosh_hashana, diaspora=diaspora).upcoming_shabbat
    print(f"Testing date: {mydate}")
    assert mydate.parasha in (Parasha.VAYEILECH, Parasha.HAAZINU, Parasha.NONE)


def test_last_week_of_the_year() -> None:
    """The last day of the year is parshat Vayelech."""
    mydate = HDate()
    mydate.hdate = HebrewDate(5779, Months.ELUL, 29)
    assert mydate.parasha == Parasha.VAYEILECH
