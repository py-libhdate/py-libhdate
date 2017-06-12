import pytest
import datetime
import random

import hdate

@pytest.fixture
def random_date():
    year = random.randint(400,2500)
    month = random.randint(1, 12)
    maxday = 31 if month in [1,3,5,7,8,10,12] else 30
    if month == 2:
        if year % 4 != 0 or (year % 100 != 0 and year % 400 != 0):
            maxday = 28
        else:
            maxday = 29
    day = random.randint(1,maxday)
    return year, month, day

class TestSetDate(object):

    def test_default_today(self):
        assert hdate.set_date(None) == datetime.date.today()

    def test_random_date(self, random_date):
        randomday = datetime.date(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    @pytest.mark.parametrize('execution_number', range(5))
    def test_random_datetime(self, execution_number, random_date):
        randomday = datetime.datetime(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    def test_illegal_value(self):
        with pytest.raises(TypeError):
            hdate.set_date(100)

class TestHDate(object):

    @pytest.fixture
    def default_values(self):
        return hdate.HDate()

    @pytest.fixture
    def random_date(self, random_date):
        date = datetime.date(*random_date)
        return hdate.HDate(date)

    def test_default_weekday(self, default_values):
        expected_weekday = datetime.datetime.today().weekday() + 2
        expected_weekday = expected_weekday if expected_weekday < 8 else 1
        assert default_values._weekday == expected_weekday

    @pytest.mark.parametrize('execution_number', range(10))
    def test_random_weekday(self, execution_number, random_date):
        expected_weekday = random_date._gdate.weekday() + 2
        expected_weekday = expected_weekday if expected_weekday < 8 else 1
        assert random_date._weekday == expected_weekday
