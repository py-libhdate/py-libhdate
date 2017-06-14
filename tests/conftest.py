import datetime
import random
import pytest


@pytest.fixture
def random_date():
    year = random.randint(400, 2500)
    month = random.randint(1, 12)
    maxday = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30
    if month == 2:
        if year % 4 != 0 or (year % 100 != 0 and year % 400 != 0):
            maxday = 28
        else:
            maxday = 29
    day = random.randint(1, maxday)
    return year, month, day
