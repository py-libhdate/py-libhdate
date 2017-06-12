import pytest
import datetime
import random

import hdate

class TestSetDate(object):
    
    @pytest.fixture
    def random_date(self):
        year = random.randint(0,2500)
        month = random.randint(1, 12)
        maxday = 31 if month in [1,3,5,7,8,10,12] else 30
        if month == 2:
            if year % 4 != 0 or (year % 100 != 0 and year % 400 != 0):
                maxday = 28
            else:
                maxday = 29
        day = random.randint(1,maxday)
        return year, month, day
        
    def test_default_today(self):
        assert hdate.set_date(None) == datetime.date.today()

    def test_random_date(self, random_date):
        randomday = datetime.date(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    def test_random_datetime(self, random_date):
        randomday = datetime.datetime(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    def test_illegal_value(self):
        with pytest.raises(TypeError):
            hdate.set_date(100)
