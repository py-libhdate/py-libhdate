"""Test the holidays module."""

from hdate.holidays import HolidayManager


def test_holiday_manager() -> None:
    """Test the holiday manager."""
    assert isinstance(HolidayManager(diaspora=False), HolidayManager)
