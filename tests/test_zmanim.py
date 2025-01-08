"""Test Zmanim objects."""

import datetime as dt
import sys
from typing import Optional
from zoneinfo import ZoneInfo

import pytest
from hypothesis import given, strategies

from hdate import Zmanim
from hdate.location import Location

_ASTRAL = "astral" in sys.modules

NYC_LAT = 40.7128
NYC_LNG = -74.0060

LONDON_LAT = 51.5074
LONDON_LNG = -0.1278

PUNTA_ARENAS_LAT = -53.1678  # Southern example
PUNTA_ARENAS_LNG = -70.9167


def compare_dates(
    date1: Optional[dt.datetime],
    date2: Optional[dt.datetime],
    allow_grace: bool = False,
) -> None:
    """Compare 2 dates to be more or less equal."""
    if not (date1 or date2):
        assert date1 == date2
    else:
        grace = dt.timedelta(minutes=5 if (not _ASTRAL or allow_grace) else 0)
        assert date1 is not None
        assert date2 is not None
        assert date1 - grace <= date2 <= date1 + grace


def compare_times(time1: dt.time, time2: dt.time, allow_grace: bool = False) -> None:
    """Compare times to be equal."""
    compare_dates(
        dt.datetime.combine(dt.date.today(), time1),
        dt.datetime.combine(dt.date.today(), time2),
        allow_grace,
    )


class TestZmanim:
    """Zmanim tests"""

    def test_bad_date(self) -> None:
        """Check that a bad value argument to zmanim raises an error"""
        with pytest.raises(TypeError):
            Zmanim(date="bad value")  # type: ignore

    @given(
        strategies.shared(strategies.dates(), key="base_date").flatmap(
            lambda d: strategies.tuples(
                strategies.just(d),
                strategies.dates().filter(
                    lambda x: x.year != d.year and x.month == d.month and x.day == d.day
                ),
            )
        )
    )
    def test_same_doy_is_equal(self, dates: tuple[dt.date, dt.date]) -> None:
        """Test two doy to be equal."""
        this_date, other_date = dates
        this_zmanim = Zmanim(this_date).get_utc_sun_time_full()
        other_zmanim = Zmanim(other_date).get_utc_sun_time_full()
        grace = 0 if not _ASTRAL else 14
        for zman in this_zmanim:
            other = next(o for o in other_zmanim if o.name == zman.name)
            assert (
                zman.minutes - grace <= other.minutes <= zman.minutes + grace
            ), zman.name

    def test_extreme_zmanim(self) -> None:
        """Test that Zmanim north to 50 degrees latitude is correct."""
        day = dt.date(2024, 6, 18)
        compare_times(
            Zmanim(
                date=day,
                location=Location(
                    name="London",
                    latitude=LONDON_LAT,
                    longitude=LONDON_LNG,
                    timezone="Europe/London",
                    diaspora=True,
                ),
            )
            .zmanim["sunset"]
            .time(),
            dt.time(21, 22),
            allow_grace=True,
        )
        compare_times(
            Zmanim(
                date=day,
                location=Location(
                    name="Punta Arenas",
                    latitude=PUNTA_ARENAS_LAT,
                    longitude=PUNTA_ARENAS_LNG,
                    timezone="America/Punta_Arenas",
                    diaspora=True,
                ),
            )
            .zmanim["sunset"]
            .time(),
            dt.time(17, 31),
            allow_grace=True,
        )

    def test_using_tzinfo(self) -> None:
        """Test tzinfo to be correct."""
        day = dt.date(2018, 9, 8)
        timezone_str = "America/New_York"
        timezone = ZoneInfo(timezone_str)
        location_tz_str = Location(
            "New York", NYC_LAT, NYC_LNG, timezone_str, diaspora=True
        )
        location = Location("New York", NYC_LAT, NYC_LNG, timezone, diaspora=True)

        compare_times(
            Zmanim(date=day, location=location_tz_str).zmanim["first_stars"].time(),
            dt.time(19, 47),
        )

        compare_times(
            Zmanim(date=day, location=location).zmanim["first_stars"].time(),
            dt.time(19, 47),
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
    def test_candle_lighting(
        self,
        now: dt.datetime,
        offset: int,
        candle_lighting: Optional[dt.datetime],
        melacha_assur: bool,
    ) -> None:
        """Test candle lighting values."""
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone="America/New_York",
            diaspora=True,
        )
        # Use a constant offset for Havdalah for unit test stability.
        zmanim = Zmanim(
            date=now.date(),
            location=location_tz_str,
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

    @pytest.mark.parametrize(
        ["now", "offset", "havdalah", "melacha_assur"], HAVDALAH_TEST
    )
    def test_havdalah(
        self,
        now: dt.datetime,
        offset: int,
        havdalah: Optional[dt.datetime],
        melacha_assur: bool,
    ) -> None:
        """Test havdalah times."""
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone="America/New_York",
            diaspora=True,
        )
        # Use a constant offset for Havdalah for unit test stability.
        zmanim = Zmanim(
            date=now.date(), location=location_tz_str, havdalah_offset=offset
        )
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
    def test_motzei_shabbat_chag(
        self, now: dt.datetime, offset: int, motzei_shabbat_chag: bool
    ) -> None:
        """Test motzei shabbat chag boolean is correct."""
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone="America/New_York",
            diaspora=True,
        )
        # Use a constant offset for Havdalah for unit test stability.
        zmanim = Zmanim(
            date=now.date(), location=location_tz_str, havdalah_offset=offset
        )
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

    @pytest.mark.parametrize(
        ["now", "offset", "erev_shabbat_chag"], EREV_SHABBAT_CHAG_TEST
    )
    def test_erev_shabbat_hag(
        self, now: dt.datetime, offset: int, erev_shabbat_chag: bool
    ) -> None:
        """Test erev shabbat chag boolean is correct."""
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone="America/New_York",
            diaspora=True,
        )
        # Use a constant offset for Havdalah for unit test stability.
        zmanim = Zmanim(
            date=now.date(), location=location_tz_str, havdalah_offset=offset
        )
        assert zmanim.erev_shabbat_chag(now) == erev_shabbat_chag

    def test_candle_lighting_erev_shabbat_is_yom_tov(self) -> None:
        """Test for candle lighting when erev shabbat is yom tov"""
        day = dt.date(2024, 10, 18)
        actual_candle_lighting = dt.datetime(
            2024, 10, 18, 17, 52, 00, tzinfo=ZoneInfo("America/New_York")
        )
        coord = Location(
            "New York", 40.7128, -74.0060, "America/New_York", diaspora=True
        )
        zman = Zmanim(
            date=day,
            location=coord,
            candle_lighting_offset=18,
        )
        assert zman.candle_lighting == actual_candle_lighting
