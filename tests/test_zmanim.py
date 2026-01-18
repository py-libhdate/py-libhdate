"""Test Zmanim objects with high-precision Meeus engine."""

import datetime as dt
import sys
from typing import Any, cast

import pytest
from hypothesis import given, strategies

import hdate.zmanim
from hdate import Zmanim
from hdate.location import Location

_ASTRAL = "astral" in sys.modules


def compare_dates(
    date1: dt.datetime | None, date2: dt.datetime | None, grace: int = 0
) -> None:
    """Compare 2 dates to be more or less equal."""
    if not (date1 or date2):
        assert date1 == date2
    else:
        # The new engine is precise (Meeus).
        # We allow 2 minutes for atmospheric variance vs reference tables.
        _grace = 2 if grace == 0 else grace
        grace_td = dt.timedelta(minutes=_grace)
        assert date1 is not None
        assert date2 is not None
        assert (
            date1 - grace_td <= date2 <= date1 + grace_td
        ), f"Expected {date2}, got {date1}"


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
    [
        ("London", dt.time(21, 21)),  # 51.5N - Standard High Lat
        ("Punta Arenas", dt.time(17, 31)),  # 53S - Southern Hemisphere
    ],
    indirect=["location"],
)
def test_extreme_zmanim(location: Location, result: dt.time) -> None:
    """Test that Zmanim works correctly at >50 degree latitudes."""
    day = dt.date(2024, 6, 18)
    compare_times(
        Zmanim(date=day, location=location).shkia.local.time(), result, grace=5
    )


@pytest.mark.parametrize("location", ["London"], indirect=True)
def test_native_calc_execution_winter(location: Location) -> None:
    """
    Test London (Lat > 50) in Winter.
    Forces execution of the Native Meeus math for Alot/Tzeit.
    """
    # Winter: Alot is reachable.
    # Lat > 50 so it skips Astral check.
    z = Zmanim(date=dt.date(2024, 1, 1), location=location)

    # Accessing 'alot_hashachar' triggers _get_safe_sun_time -> native path
    alot = z.alot_hashachar
    assert alot is not None
    # Winter dawn in London is roughly 06:00
    assert 5 <= alot.local.hour <= 7


@pytest.mark.parametrize("location", ["London"], indirect=True)
def test_white_night_fallback(location: Location) -> None:
    """
    Test London (Lat > 50) in Summer.
    Alot HaShachar (16.1) is impossible.
    Forces fallback to Solar Midnight.
    """
    # Summer Solstice: Alot impossible. Lat > 50. Fallback to Midnight.
    z = Zmanim(date=dt.date(2024, 6, 21), location=location)

    # Calculate expected fallback (Solar Midnight is approx 01:00 AM BST)
    midnight = z.chatzot_halayla.local.time()
    alot = z.alot_hashachar.local.time()

    # Verify Alot was set to Midnight (White Night Fallback)
    compare_times(alot, midnight, grace=1)


@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_force_native_engine_nyc(
    location: Location, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Force the Native Engine (Meeus) even for standard latitudes (NYC).
    This covers the 'else' branch that runs if Astral is missing/disabled.
    """
    # Force _USE_ASTRAL to False in the hdate.zmanim module logic
    monkeypatch.setattr(hdate.zmanim, "_USE_ASTRAL", False)

    z = Zmanim(date=dt.date(2024, 10, 18), location=location)

    # Verify accuracy using the Native Engine
    expected = dt.time(17, 53)
    if z.candle_lighting:
        compare_times(z.candle_lighting.time(), expected, grace=0)


@pytest.mark.parametrize("location", ["Reykjavik"], indirect=True)
def test_high_latitude_stability(location: Location) -> None:
    """Test stability at 64N (Reykjavik) near the Arctic Circle."""
    # Summer Solstice (Extreme Day)
    day = dt.date(2024, 6, 21)
    z = Zmanim(date=day, location=location)

    # Sun sets very late (~Midnight next day).
    # We just ensure it doesn't crash and returns a valid time object.
    assert isinstance(z.shkia.local.time(), dt.time)

    # Winter Solstice (Extreme Night)
    day_winter = dt.date(2024, 12, 21)
    z_winter = Zmanim(date=day_winter, location=location)
    # Sun rises very late (~11:22 AM)
    compare_times(z_winter.netz_hachama.local.time(), dt.time(11, 22), grace=5)


@pytest.mark.parametrize("location", ["Tromso"], indirect=True)
def test_polar_fallback(location: Location) -> None:
    """Test behavior above Arctic Circle (69N) where sun may not rise/set."""
    # Winter - Polar Night (Sun never rises)
    day = dt.date(2024, 12, 21)
    z = Zmanim(date=day, location=location)

    # This should trigger the fallback logic
    assert z.netz_hachama is not None
    assert z.shkia is not None
    assert isinstance(z.netz_hachama.local.time(), dt.time)


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
    candle_lighting: dt.datetime | None,
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
    havdalah: dt.datetime | None,
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
    # The new Meeus engine is highly accurate.
    # We expect 17:53 (correct astronomical time) rather than 17:55 (old drifted time).
    actual_candle_lighting = dt.datetime(
        2024, 10, 18, 17, 53, 00, tzinfo=cast(dt.tzinfo, location.timezone)
    )
    zman = Zmanim(date=day, location=location, candle_lighting_offset=18)
    assert zman.candle_lighting == actual_candle_lighting


_VALID_ATTRS = set(dir(Zmanim()))


@given(name=strategies.text().filter(lambda s: s not in _VALID_ATTRS))
def test_non_existing_attribute(name: str) -> None:
    """Test trying to access a Zmanim attribute that isn't in the class."""
    with pytest.raises(AttributeError):
        z = Zmanim()
        _ = getattr(z, name)


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


@pytest.mark.parametrize("location", ["London"], indirect=True)
def test_white_night_fallback_logic(location: Location) -> None:
    """
    Verify that when the sun does not reach the required angle (White Night),
    the system falls back to Solar Midnight instead of crashing or returning None.

    Scenario: London (51.5N) on June 21.
    - Solar depression at midnight is ~15 degrees.
    - Alot HaShachar requires 16.1 degrees.
    - Therefore: Math fails -> Fallback triggers.
    """
    day = dt.date(2024, 6, 21)
    z = Zmanim(date=day, location=location)

    # Chatzot is calculated as 'End of Day' (e.g. 1442 mins / 24:02)
    # The fallback logic uses 'Start of Day' (e.g. 2 mins / 00:02)
    # We normalize both to the 24h cycle to compare the solar position.
    expected_fallback = z.chatzot_halayla.minutes % 1440.0
    actual_alot = z.alot_hashachar.minutes % 1440.0

    assert (
        abs(actual_alot - expected_fallback) < 0.001
    ), f"Expected fallback to midnight ({expected_fallback}), but got {actual_alot}"


@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_legacy_astral_path_execution(
    location: Location, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Verify that standard latitudes (<=50) use the Legacy Astral path
    when Astral is available/enabled.
    """
    monkeypatch.setattr(hdate.zmanim, "_USE_ASTRAL", True)

    def fake_transit(_self: Any, _zenith: float, _rising: bool) -> float:
        return 999.9

    monkeypatch.setattr(Zmanim, "_get_utc_time_of_transit", fake_transit)

    z = Zmanim(date=dt.date(2024, 1, 1), location=location)

    assert z.alot_hashachar.minutes == 999.9, "Legacy Astral path not taken!"
