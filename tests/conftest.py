"""Fixtures for py.test."""

from calendar import isleap
import random
import pytest


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
    return year, month, day
