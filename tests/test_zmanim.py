import datetime
import random
from calendar import isleap
from datetime import datetime as dt

import pytest
import pytz

from hdate import Zmanim
from hdate.common import Location

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic

NYC_LAT = 40.7128
NYC_LNG = -74.0060


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

        assert (
            Zmanim(this_date).get_utc_sun_time_full()
            == Zmanim(other_date).get_utc_sun_time_full()
        )

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

        assert Zmanim(date=day, location=location_tz_str).zmanim[
            "first_stars"
        ].time() == datetime.time(19, 48)

        assert Zmanim(date=day, location=location).zmanim[
            "first_stars"
        ].time() == datetime.time(19, 48)

    # Times are assumed for NYC.
    CANDLES_TEST = [
        (dt(2018, 9, 7, 13, 1), 18, dt(2018, 9, 7, 19, 4), False),
        (dt(2018, 9, 7, 20, 1), 18, dt(2018, 9, 7, 19, 4), True),
        (dt(2018, 9, 8, 13, 1), 18, None, True),
        (dt(2018, 9, 19, 22, 1), 18, None, False),
        (dt(2018, 9, 9, 16, 1), 20, dt(2018, 9, 9, 18, 59), False),
        (dt(2018, 9, 9, 19, 30), 18, dt(2018, 9, 9, 19, 1), True),
        # Candle lighting matches the time that would be havdalah.
        (dt(2018, 9, 10, 8, 1), 18, dt(2018, 9, 10, 19, 59), True),
        (dt(2018, 9, 10, 20, 20), 18, dt(2018, 9, 10, 19, 59), True),
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
        assert actual == candle_lighting
        assert zmanim.issur_melacha_in_effect == melacha_assur

    # Times are assumed for NYC.
    HAVDALAH_TEST = [
        (dt(2018, 9, 7, 13, 1), 42, None, False),
        (dt(2018, 9, 7, 20, 1), 42, None, True),
        (dt(2018, 9, 8, 13, 1), 42, dt(2018, 9, 8, 20, 2), True),
        (dt(2018, 9, 8, 13, 1), 0, dt(2018, 9, 8, 20, 2), True),
        (dt(2018, 9, 19, 22, 1), 18, dt(2018, 9, 19, 19, 20), False),
        (dt(2018, 9, 9, 16, 1), 0, None, False),
        (dt(2018, 9, 9, 19, 30), 0, None, True),
        (dt(2018, 9, 11, 16, 1), 0, dt(2018, 9, 11, 19, 57), True),
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
        assert actual == havdalah
        assert zmanim.issur_melacha_in_effect == melacha_assur
