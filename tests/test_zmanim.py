import datetime
import random
import sys
from calendar import isleap
from datetime import datetime as dt, timedelta as td

import pytest
import pytz

from hdate import Zmanim
from hdate.common import Location

_ASTRAL = "astral" in sys.modules

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic

NYC_LAT = 40.7128
NYC_LNG = -74.0060


def compare_dates(date1, date2):
    if not (date1 or date2):
        assert date1 == date2
    else:
        grace = td(minutes=5 if not _ASTRAL else 0)
        assert date1 - grace <= date2 <= date1 + grace


def compare_times(time1, time2):
    compare_dates(
        dt.combine(dt.today(), time1),
        dt.combine(dt.today(), time2))


class TestZmanim(object):
    def test_bad_date(self):
        with pytest.raises(TypeError):
            Zmanim(date="bad value")

    @pytest.mark.parametrize("execution_number", list(range(5)))
    def test_same_doy_is_equal(self, execution_number, random_date):
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

    def test_using_tzinfo(self):
        day = datetime.date(2018, 9, 8)
        timezone_str = "America/New_York"
        timezone = pytz.timezone(timezone_str)
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

        compare_times(Zmanim(date=day, location=location_tz_str).zmanim[
            "first_stars"
        ].time(), datetime.time(19, 45))

        compare_times(Zmanim(date=day, location=location).zmanim[
            "first_stars"
        ].time(), datetime.time(19, 45))

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
