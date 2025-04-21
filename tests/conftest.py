"""Test confiugration file."""

import pytest
from hypothesis import strategies

from hdate.hebrew_date import HebrewDate, Months
from hdate.holidays import HolidayDatabase
from hdate.location import Location
from hdate.translator import set_language

MIN_YEAR = 4000
MAX_YEAR = 6000


@pytest.fixture(scope="session")
def holiday_db(request: pytest.FixtureRequest) -> HolidayDatabase:
    """Create the holiday database."""

    diaspora_db = HolidayDatabase(diaspora=True)
    israel_db = HolidayDatabase(diaspora=False)

    if hasattr(request, "param") and request.param is True:
        return diaspora_db

    return israel_db


@pytest.fixture(scope="session")
def location(request: pytest.FixtureRequest) -> Location:
    """
    Create a Location object for a given location name.

    This fixture is session scoped, so the creation of ZoneInfo objects
    is done once per session. This is to avoid issues with xdist parallel reading of
    the timezone data causing tests to hang.
    """
    locations = {
        "Jerusalem": Location(
            "Jerusalem", 31.778, 35.235, "Asia/Jerusalem", 754, False
        ),
        "Petah Tikva": Location(
            "פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54, False
        ),
        "New York": Location(
            "New York", 40.7128, -74.0060, "America/New_York", 0, True
        ),
        "London": Location("London", 51.5074, -0.1278, "Europe/London", 0, True),
        "Punta Arenas": Location(
            "Punta Arenas", -53.1500, -70.9167, "America/Punta_Arenas", 0, True
        ),
    }

    if request.param not in locations:
        raise ValueError(f"Invalid location: {request.param}")
    return locations[request.param]


@pytest.fixture(autouse=True)
def reset_context_language() -> None:
    """Reset the context language to the default value before each test."""
    set_language("he")


@strategies.composite
def valid_hebrew_date(draw: strategies.DrawFn) -> HebrewDate:
    """Generate a valid Hebrew date."""
    year = draw(strategies.integers(min_value=MIN_YEAR, max_value=MAX_YEAR))
    month = draw(strategies.sampled_from(Months.in_year(year)))
    days = month.days(year)
    day = draw(strategies.integers(min_value=1, max_value=days))

    return HebrewDate(year, month, day)
