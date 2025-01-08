"""Test confiugration file."""

import pytest

from hdate.location import Location


@pytest.fixture
def location(request: pytest.FixtureRequest) -> Location:
    """Create a Location object for a given location name."""
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
