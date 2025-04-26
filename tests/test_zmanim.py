"""Test Zmanim objects."""

import datetime as dt
import sys
from typing import Optional, cast

import pytest
from hypothesis import given, strategies

from hdate import Zmanim
from hdate.location import Location

_ASTRAL = "astral" in sys.modules

NYC_LAT = 40.7128
NYC_LNG = -74.0060


def compare_dates(
    date1: Optional[dt.datetime], date2: Optional[dt.datetime], grace: int = 0
) -> None:
    """Compare 2 dates to be more or less equal."""
    if not (date1 or date2):
        assert date1 == date2
    else:
        _grace = 5 if (not _ASTRAL and grace == 0) else grace
        grace_td = dt.timedelta(minutes=_grace)
        assert date1 is not None
        assert date2 is not None
        assert date1 - grace_td <= date2 <= date1 + grace_td


def compare_times(time1: dt.time, time2: dt.time, grace: int = 0) -> None:
    """Compare times to be equal."""
    compare_dates(
        dt.datetime.combine(dt.date.today(), time1),
        dt.datetime.combine(dt.date.today(), time2),
        grace,
    )


def test_bad_date() -> None:
    """Check that a bad value argument to zmanim raises an error"""
    with pytest.raises(TypeError):
        Zmanim(date="bad value")  # type: ignore


@given(
    this_date=strategies.dates(
        min_value=dt.date(1800, 1, 1), max_value=dt.date(3000, 1, 1)
    ).filter(lambda d: not (d.month == 2 and d.day == 29)),
    year_diff=strategies.integers(min_value=0, max_value=200),
)
def test_same_doy_is_equal(this_date: dt.date, year_diff: int) -> None:
    """Test two doy to have equal zmanim."""
    other_date = dt.date(year_diff + this_date.year, this_date.month, this_date.day)
    this_zmanim = Zmanim(this_date).zmanim
    other_zmanim = Zmanim(other_date).zmanim
    grace = 10
    for name, zman in this_zmanim.items():
        other = other_zmanim[name]
        assert zman.minutes - grace <= other.minutes <= zman.minutes + grace, zman.name


@pytest.mark.parametrize(
    "location, result",
    [("London", dt.time(21, 22)), ("Punta Arenas", dt.time(17, 31))],
    indirect=["location"],
)
def test_extreme_zmanim(location: Location, result: dt.time) -> None:
    """Test that Zmanim north to 50 degrees latitude is correct."""
    day = dt.date(2024, 6, 18)
    compare_times(
        Zmanim(date=day, location=location).shkia.local.time(), result, grace=5
    )


# Times are assumed for NYC.
CANDLES_TEST = [
    (dt.datetime(2018, 9, 7, 13, 1), 18, dt.datetime(2018, 9, 7, 19, 0), False),
    (dt.datetime(2018, 9, 7, 19, 4), 18, dt.datetime(2018, 9, 7, 19, 0), True),
    (dt.datetime(2018, 9, 8, 13, 1), 18, None, True),
    (dt.datetime(2018, 9, 19, 22, 1), 18, None, False),
    (dt.datetime(2018, 9, 9, 16, 1), 20, dt.datetime(2018, 9, 9, 18, 55), False),
    (dt.datetime(2018, 9, 9, 19, 30), 18, dt.datetime(2018, 9, 9, 18, 57), True),
    # Candle lighting matches the time that would be havdalah.
    (dt.datetime(2018, 9, 10, 8, 1), 18, dt.datetime(2018, 9, 10, 19, 55), True),
    (dt.datetime(2018, 9, 10, 20, 20), 18, dt.datetime(2018, 9, 10, 19, 55), True),
]


@pytest.mark.parametrize(
    ["now", "offset", "candle_lighting", "melacha_assur"], CANDLES_TEST
)
@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_candle_lighting(
    now: dt.datetime,
    offset: int,
    candle_lighting: Optional[dt.datetime],
    melacha_assur: bool,
    location: Location,
) -> None:
    """Test candle lighting values."""
    # Use a constant offset for Havdalah for unit test stability.
    zmanim = Zmanim(
        date=now.date(),
        location=location,
        candle_lighting_offset=offset,
        havdalah_offset=42,
    )
    actual = zmanim.candle_lighting
    if actual is not None:
        actual = actual.replace(tzinfo=None)
    compare_dates(actual, candle_lighting)
    assert zmanim.issur_melacha_in_effect(now) == melacha_assur


# Times are assumed for NYC.
HAVDALAH_TEST = [
    (dt.datetime(2018, 9, 7, 13, 1), 42, None, False),
    (dt.datetime(2018, 9, 7, 20, 1), 42, None, True),
    (dt.datetime(2018, 9, 8, 13, 1), 42, dt.datetime(2018, 9, 8, 19, 59), True),
    (dt.datetime(2018, 9, 8, 13, 1), 0, dt.datetime(2018, 9, 8, 19, 58), True),
    (dt.datetime(2018, 9, 19, 22, 1), 18, dt.datetime(2018, 9, 19, 19, 16), False),
    (dt.datetime(2018, 9, 9, 16, 1), 0, None, False),
    (dt.datetime(2018, 9, 9, 19, 30), 0, None, True),
    (dt.datetime(2018, 9, 11, 16, 1), 0, dt.datetime(2018, 9, 11, 19, 53), True),
    # No havdalah in the middle of Yom Tov.
    (dt.datetime(2018, 9, 10, 8, 1), 0, None, True),
    (dt.datetime(2018, 9, 10, 20, 20), 0, None, True),
]


@pytest.mark.parametrize(["now", "offset", "havdalah", "melacha_assur"], HAVDALAH_TEST)
@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_havdalah(
    now: dt.datetime,
    offset: int,
    havdalah: Optional[dt.datetime],
    melacha_assur: bool,
    location: Location,
) -> None:
    """Test havdalah times."""
    zmanim = Zmanim(date=now.date(), location=location, havdalah_offset=offset)
    actual = zmanim.havdalah
    if actual is not None:
        actual = actual.replace(tzinfo=None)
    compare_dates(actual, havdalah)
    assert zmanim.issur_melacha_in_effect(now) == melacha_assur


# Times are assumed for NYC.
MOTZEI_SHABBAT_CHAG_TEST = [
    (dt.datetime(2018, 9, 7, 13, 1), 42, False),
    (dt.datetime(2018, 9, 7, 20, 1), 42, False),
    (dt.datetime(2018, 9, 8, 13, 1), 42, False),
    (dt.datetime(2018, 9, 8, 22, 1), 0, True),
    (dt.datetime(2018, 9, 9, 16, 1), 0, False),
    (dt.datetime(2018, 9, 9, 19, 30), 0, False),
    (dt.datetime(2018, 9, 10, 16, 1), 0, False),
    (dt.datetime(2018, 9, 10, 19, 30), 0, False),
    (dt.datetime(2018, 9, 11, 16, 1), 0, False),
    (dt.datetime(2018, 9, 11, 20, 1), 0, True),
    (dt.datetime(2018, 9, 19, 22, 1), 18, True),
]


@pytest.mark.parametrize(
    ["now", "offset", "motzei_shabbat_chag"], MOTZEI_SHABBAT_CHAG_TEST
)
@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_motzei_shabbat_chag(
    now: dt.datetime, offset: int, motzei_shabbat_chag: bool, location: Location
) -> None:
    """Test motzei shabbat chag boolean is correct."""
    # Use a constant offset for Havdalah for unit test stability.
    zmanim = Zmanim(date=now.date(), location=location, havdalah_offset=offset)
    assert zmanim.motzei_shabbat_chag(now) == motzei_shabbat_chag


# Times are assumed for NYC.
EREV_SHABBAT_CHAG_TEST = [
    (dt.datetime(2018, 9, 7, 13, 1), 42, True),  # fri
    (dt.datetime(2018, 9, 7, 20, 1), 42, False),
    (dt.datetime(2018, 9, 8, 13, 1), 42, False),  # sat
    (dt.datetime(2018, 9, 8, 20, 1), 0, False),
    (dt.datetime(2018, 9, 9, 16, 1), 0, True),  # erev rosh hashana
    (dt.datetime(2018, 9, 9, 19, 30), 0, False),
    (dt.datetime(2018, 9, 10, 16, 1), 0, False),  # rosh hashana I
    (dt.datetime(2018, 9, 10, 19, 30), 0, False),
    (dt.datetime(2018, 9, 11, 16, 1), 0, False),  # rosh hashana II
    (dt.datetime(2018, 9, 11, 20, 1), 0, False),
    (dt.datetime(2018, 9, 18, 13, 1), 18, True),  # erev yom kipur
    (dt.datetime(2018, 9, 18, 22, 1), 18, False),
    (dt.datetime(2018, 9, 19, 13, 1), 18, False),
    (dt.datetime(2018, 9, 19, 22, 1), 18, False),
]


@pytest.mark.parametrize(["now", "offset", "erev_shabbat_chag"], EREV_SHABBAT_CHAG_TEST)
@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_erev_shabbat_hag(
    now: dt.datetime, offset: int, erev_shabbat_chag: bool, location: Location
) -> None:
    """Test erev shabbat chag boolean is correct."""
    # Use a constant offset for Havdalah for unit test stability.
    zmanim = Zmanim(date=now.date(), location=location, havdalah_offset=offset)
    assert zmanim.erev_shabbat_chag(now) == erev_shabbat_chag


@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_candle_lighting_erev_shabbat_is_yom_tov(location: Location) -> None:
    """Test for candle lighting when erev shabbat is yom tov"""
    day = dt.date(2024, 10, 18)
    if _ASTRAL:
        actual_candle_lighting = dt.datetime(
            2024, 10, 18, 17, 52, 00, tzinfo=cast(dt.tzinfo, location.timezone)
        )
    else:
        actual_candle_lighting = dt.datetime(
            2024, 10, 18, 17, 55, 00, tzinfo=cast(dt.tzinfo, location.timezone)
        )
    zman = Zmanim(date=day, location=location, candle_lighting_offset=18)
    assert zman.candle_lighting == actual_candle_lighting


@given(name=strategies.text().filter(lambda s: s not in dir(Zmanim)))
def test_non_existing_attribute(name: str) -> None:
    """Test trying to access a Zmanim attribute that isn't in the class."""
    with pytest.raises(AttributeError):
        z = Zmanim()
        assert z.__getattr__(name) is None  # pylint: disable=unnecessary-dunder-call


def test_attributes_in_dir() -> None:
    """Test that Zmanim attributes are in the dir."""
    keys = {
        "alot_hashachar",
        "netz_hachama",
        "plag_hamincha",
        "shkia",
        "tset_hakohavim",
    }
    assert keys.issubset(set(dir(Zmanim())))
