"""Fixtures for py.test."""

import datetime
import random
from calendar import isleap

import pytest

import hdate


@pytest.fixture
def random_date():
    """Generate a random valid date."""
    year = random.randint(400, 2500)
    month = random.randint(1, 12)
    maxday = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30
    if month == 2:
        if isleap(year):
            maxday = 29
        else:
            maxday = 28
    day = random.randint(1, maxday)
    return datetime.date(year, month, day)


@pytest.fixture
def rand_hdate(random_date):
    """Given a random date, generate a random HDate."""
    return hdate.HDate(random_date)
