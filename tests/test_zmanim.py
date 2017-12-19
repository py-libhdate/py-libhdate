import datetime
import random
from calendar import isleap

import pytest

import hdate

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic


class TestZmanim(object):

    @pytest.mark.parametrize('execution_number', list(range(5)))
    def test_same_doy_is_equal(self, execution_number, random_date):
        other_year = random.randint(500, 3000)
        shift_day = datetime.timedelta(days=0)
        this_date = datetime.date(*random_date)

        if (isleap(this_date.year) != isleap(other_year) and
                this_date > datetime.date(this_date.year, 2, 28)):
            if isleap(other_year):
                shift_day = datetime.timedelta(days=-1)
            else:
                shift_day = datetime.timedelta(days=1)

        if (isleap(this_date.year) and not isleap(other_year) and
                this_date.month == 2 and this_date.day == 29):
            # Special case we can't simply replace the year as there's
            # no leap day in the other year
            other_date = datetime.date(other_year, 3, 1)
        else:
            other_date = this_date.replace(year=other_year) + shift_day

        assert (hdate.Zmanim(this_date).get_utc_sun_time_full() ==
                hdate.Zmanim(other_date).get_utc_sun_time_full())
