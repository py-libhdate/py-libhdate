"""Test Zmanim objects."""

import datetime
import random
import sys
from calendar import isleap
from datetime import datetime as dt
from datetime import timedelta as td

import pytest

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from hdate import Zmanim
from hdate.location import Location

_ASTRAL = "astral" in sys.modules

NYC_LAT = 40.7128
NYC_LNG = -74.0060

LONDON_LAT = 51.5074
LONDON_LNG = -0.1278

PUNTA_ARENAS_LAT = -53.1678  # Southern example
PUNTA_ARENAS_LNG = -70.9167


def compare_dates(date1, date2, allow_grace=False):
    """Compare 2 dates to be more or less equal."""
    if not (date1 or date2):
        assert date1 == date2
    else:
        grace = td(minutes=5 if (not _ASTRAL or allow_grace) else 0)
        assert date1 - grace <= date2 <= date1 + grace


def compare_times(time1, time2, allow_grace=False):
    """Compare times to be equal."""
    compare_dates(
        dt.combine(dt.today(), time1), dt.combine(dt.today(), time2), allow_grace
    )


class TestZmanim:
    """Zmanim tests"""

    def test_bad_date(self):
        """Check that a bad value argument to zmanim raises an error"""
        with pytest.raises(TypeError):
            Zmanim(date="bad value")

    @pytest.mark.parametrize("execution_number", list(range(5)))
    def test_same_doy_is_equal(self, execution_number, random_date):
        """Test two doy to be equal."""
        print(f"Run number {execution_number}")
        other_year = random.randint(500, 3000)
        shift_day = datetime.timedelta(days=0)
        this_date = random_date

        if isleap(this_date.year) != isleap(other_year) and this_date > datetime.date(
            this_date.year, 2, 28
        ):
            if isleap(other_year):
                shift_day = datetime.timedelta(days=-1)
            else:
                shift_day = datetime.timedelta(days=1)

        if (
            isleap(this_date.year)
            and not isleap(other_year)
            and this_date.month == 2
            and this_date.day == 29
        ):
            # Special case we can't simply replace the year as there's
            # no leap day in the other year
            other_date = datetime.date(other_year, 3, 1)
        else:
            other_date = this_date.replace(year=other_year) + shift_day

        this_zmanim = Zmanim(this_date).get_utc_sun_time_full()
        other_zmanim = Zmanim(other_date).get_utc_sun_time_full()
        grace = 0 if not _ASTRAL else 14
        for key, value in this_zmanim.items():
            assert value - grace <= other_zmanim[key] <= value + grace, key

    def test_extreme_zmanim(self):
        """Test that Zmanim north to 50 degrees latitude is correct."""
        day = datetime.date(2024, 6, 18)
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
            datetime.time(21, 22),
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
            datetime.time(17, 31),
            allow_grace=True,
        )

    def test_using_tzinfo(self):
        """Test tzinfo to be correct."""
        day = datetime.date(2018, 9, 8)
        timezone_str = "America/New_York"
        timezone = ZoneInfo(timezone_str)
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone=timezone_str,
            diaspora=True,
        )
        location = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone=timezone,
            diaspora=True,
        )

        compare_times(
            Zmanim(date=day, location=location_tz_str).zmanim["first_stars"].time(),
            datetime.time(19, 45),
        )

        compare_times(
            Zmanim(date=day, location=location).zmanim["first_stars"].time(),
            datetime.time(19, 45),
        )

    # Times are assumed for NYC.
    CANDLES_TEST = [
        (dt(2018, 9, 7, 13, 1), 18, dt(2018, 9, 7, 19, 0), False),
        (dt(2018, 9, 7, 19, 4), 18, dt(2018, 9, 7, 19, 0), True),
        (dt(2018, 9, 8, 13, 1), 18, None, True),
        (dt(2018, 9, 19, 22, 1), 18, None, False),
        (dt(2018, 9, 9, 16, 1), 20, dt(2018, 9, 9, 18, 55), False),
        (dt(2018, 9, 9, 19, 30), 18, dt(2018, 9, 9, 18, 57), True),
        # Candle lighting matches the time that would be havdalah.
        (dt(2018, 9, 10, 8, 1), 18, dt(2018, 9, 10, 19, 55), True),
        (dt(2018, 9, 10, 20, 20), 18, dt(2018, 9, 10, 19, 55), True),
    ]

    @pytest.mark.parametrize(
        ["now", "offset", "candle_lighting", "melacha_assur"], CANDLES_TEST
    )
    def test_candle_lighting(self, now, offset, candle_lighting, melacha_assur):
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
            date=now,
            location=location_tz_str,
            candle_lighting_offset=offset,
            havdalah_offset=42,
        )
        actual = zmanim.candle_lighting
        if actual is not None:
            actual = actual.replace(tzinfo=None)
        compare_dates(actual, candle_lighting)
        assert zmanim.issur_melacha_in_effect == melacha_assur

    # Times are assumed for NYC.
    HAVDALAH_TEST = [
        (dt(2018, 9, 7, 13, 1), 42, None, False),
        (dt(2018, 9, 7, 20, 1), 42, None, True),
        (dt(2018, 9, 8, 13, 1), 42, dt(2018, 9, 8, 19, 59), True),
        (dt(2018, 9, 8, 13, 1), 0, dt(2018, 9, 8, 19, 58), True),
        (dt(2018, 9, 19, 22, 1), 18, dt(2018, 9, 19, 19, 16), False),
        (dt(2018, 9, 9, 16, 1), 0, None, False),
        (dt(2018, 9, 9, 19, 30), 0, None, True),
        (dt(2018, 9, 11, 16, 1), 0, dt(2018, 9, 11, 19, 53), True),
        # No havdalah in the middle of Yom Tov.
        (dt(2018, 9, 10, 8, 1), 0, None, True),
        (dt(2018, 9, 10, 20, 20), 0, None, True),
    ]

    @pytest.mark.parametrize(
        ["now", "offset", "havdalah", "melacha_assur"], HAVDALAH_TEST
    )
    def test_havdalah(self, now, offset, havdalah, melacha_assur):
        """Test havdalah times."""
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone="America/New_York",
            diaspora=True,
        )
        # Use a constant offset for Havdalah for unit test stability.
        zmanim = Zmanim(date=now, location=location_tz_str, havdalah_offset=offset)
        actual = zmanim.havdalah
        if actual is not None:
            actual = actual.replace(tzinfo=None)
        compare_dates(actual, havdalah)
        assert zmanim.issur_melacha_in_effect == melacha_assur

    # Times are assumed for NYC.
    MOTZEI_SHABBAT_CHAG_TEST = [
        (dt(2018, 9, 7, 13, 1), 42, False),
        (dt(2018, 9, 7, 20, 1), 42, False),
        (dt(2018, 9, 8, 13, 1), 42, False),
        (dt(2018, 9, 8, 22, 1), 0, True),
        (dt(2018, 9, 9, 16, 1), 0, False),
        (dt(2018, 9, 9, 19, 30), 0, False),
        (dt(2018, 9, 10, 16, 1), 0, False),
        (dt(2018, 9, 10, 19, 30), 0, False),
        (dt(2018, 9, 11, 16, 1), 0, False),
        (dt(2018, 9, 11, 20, 1), 0, True),
        (dt(2018, 9, 19, 22, 1), 18, True),
    ]

    @pytest.mark.parametrize(
        ["now", "offset", "motzei_shabbat_chag"], MOTZEI_SHABBAT_CHAG_TEST
    )
    def test_motzei_shabbat_chag(self, now, offset, motzei_shabbat_chag):
        """Test motzei shabbat chag boolean is correct."""
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone="America/New_York",
            diaspora=True,
        )
        # Use a constant offset for Havdalah for unit test stability.
        zmanim = Zmanim(date=now, location=location_tz_str, havdalah_offset=offset)
        assert zmanim.motzei_shabbat_chag == motzei_shabbat_chag

    # Times are assumed for NYC.
    EREV_SHABBAT_CHAG_TEST = [
        (dt(2018, 9, 7, 13, 1), 42, True),  # fri
        (dt(2018, 9, 7, 20, 1), 42, False),
        (dt(2018, 9, 8, 13, 1), 42, False),  # sat
        (dt(2018, 9, 8, 20, 1), 0, False),
        (dt(2018, 9, 9, 16, 1), 0, True),  # erev rosh hashana
        (dt(2018, 9, 9, 19, 30), 0, False),
        (dt(2018, 9, 10, 16, 1), 0, False),  # rosh hashana I
        (dt(2018, 9, 10, 19, 30), 0, False),
        (dt(2018, 9, 11, 16, 1), 0, False),  # rosh hashana II
        (dt(2018, 9, 11, 20, 1), 0, False),
        (dt(2018, 9, 18, 13, 1), 18, True),  # erev yom kipur
        (dt(2018, 9, 18, 22, 1), 18, False),
        (dt(2018, 9, 19, 13, 1), 18, False),
        (dt(2018, 9, 19, 22, 1), 18, False),
    ]

    @pytest.mark.parametrize(
        ["now", "offset", "erev_shabbat_chag"], EREV_SHABBAT_CHAG_TEST
    )
    def test_erev_shabbat_hag(self, now, offset, erev_shabbat_chag):
        """Test erev shabbat chag boolean is correct."""
        location_tz_str = Location(
            name="New York",
            latitude=NYC_LAT,
            longitude=NYC_LNG,
            timezone="America/New_York",
            diaspora=True,
        )
        # Use a constant offset for Havdalah for unit test stability.
        zmanim = Zmanim(date=now, location=location_tz_str, havdalah_offset=offset)
        assert zmanim.erev_shabbat_chag == erev_shabbat_chag
