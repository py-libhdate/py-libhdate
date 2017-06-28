import pytest
import hdate

from calendar import isleap
import random
import datetime

class TestZmanim(object):

    def test_same_doy_is_equal(self, random_date):
        other_year = random.randint(500, 3000)
        shift_day = datetime.timedelta(days=0)
        this_date = datetime.date(*random_date)

        if (isleap(this_date.year) != isleap(other_year) and
            this_date > datetime.date(this_date.year, 2, 28)):
                if isleap(other_year):
                    shift_day = datetime.timedelta(days=-1)
                else:
                    shift_day = datetime.timedelta(days=1)

        other_date = this_date.replace(year=other_year) + shift_day

        assert (hdate.Zmanim(this_date).get_utc_sun_time_full() ==
                hdate.Zmanim(other_date).get_utc_sun_time_full())
