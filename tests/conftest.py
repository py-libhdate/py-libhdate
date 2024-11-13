"""Fixtures for py.test."""

from calendar import isleap
from datetime import date
from random import randint

import pytest

from hdate import HDate


@pytest.fixture
def random_date() -> date:
    """Generate a random valid date."""
    year = randint(400, 2500)
    month = randint(1, 12)
    maxday = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30
    if month == 2:
        if isleap(year):
            maxday = 29
        else:
            maxday = 28
    day = randint(1, maxday)
    return date(year, month, day)


@pytest.fixture
def rand_hdate(random_date: date) -> HDate:  # pylint: disable=redefined-outer-name
    """Given a random date, generate a random HDate."""
    return HDate(random_date)
