"""Test Tekufot objects."""

import datetime as dt
from typing import cast

import pytest

from hdate.location import Location
from hdate.tekufot import Tekufot


@pytest.mark.parametrize(
    "date, expected_tekufot_keys",
    [
        (dt.date(2024, 4, 7), ["Nissan", "Tammuz", "Tishrei", "Tevet"]),
        (dt.date(2025, 4, 7), ["Nissan", "Tammuz", "Tishrei", "Tevet"]),
    ],
)
@pytest.mark.parametrize("location", ["Jerusalem"], indirect=True)
def test_get_tekufot_dict(
    date: dt.date, expected_tekufot_keys: list[str], location: Location
) -> None:
    """Test that Tekufot calculations return the correct keys."""
    tekufot = Tekufot(date=date, location=location)
    result = tekufot.get_tekufot()
    assert set(result.keys()) == set(expected_tekufot_keys), "Tekufot keys mismatch"


@pytest.mark.parametrize(
    "date, expected_tekufot",
    [
        (
            dt.date(2024, 11, 1),
            {
                "Tishrei": dt.datetime(2024, 10, 7, 3, 0),
                "Tevet": dt.datetime(2025, 1, 6, 10, 30),
                "Nissan": dt.datetime(2025, 4, 7, 18, 0),
                "Tammuz": dt.datetime(2025, 7, 8, 1, 30),
            },
        ),
        (
            dt.date(2026, 4, 7),
            {
                "Tishrei": dt.datetime(2025, 10, 7, 9, 0),
                "Tevet": dt.datetime(2026, 1, 6, 16, 30),
                "Nissan": dt.datetime(2026, 4, 8, 0, 0),
                "Tammuz": dt.datetime(2026, 7, 8, 7, 30),
            },
        ),
    ],
)
@pytest.mark.parametrize("location", ["Jerusalem"], indirect=True)
def test_get_tekufot(
    date: dt.date, expected_tekufot: dict[str, dt.datetime], location: Location
) -> None:
    """Test that Tekufot calculations return the correct datetime values."""
    tekufot = Tekufot(date=date, location=location)
    result = tekufot.get_tekufot()
    for key, expected_dt in expected_tekufot.items():
        assert result[key] == expected_dt.replace(
            tzinfo=cast(dt.tzinfo, location.timezone)
        ), f"Mismatch for {key}: expected {expected_dt}, got {result[key]}"


@pytest.mark.parametrize(
    "date, location, expected_start",
    [
        (dt.date(2024, 10, 5), "New York", dt.date(2024, 12, 5)),
        (dt.date(2024, 10, 5), "Jerusalem", dt.date(2024, 11, 8)),
    ],
    indirect=["location"],
)
def test_get_cheilat_geshamim(
    date: dt.date, expected_start: dt.date, location: Location
) -> None:
    """Test Cheilat Geshamim start dates based on location."""
    tekufot = Tekufot(date=date, location=location)
    result = tekufot.get_cheilat_geshamim()
    assert result == expected_start, "Cheilat Geshamim date mismatch"


@pytest.mark.parametrize(
    "date, tradition, language, expected",
    [
        (
            dt.date(2024, 12, 13),
            "ashkenazi",
            "english",
            "Mashiv ha-ruach u-morid ha-geshem - VeTen Tal uMatar Livracha",
        ),
        (
            dt.date(2024, 12, 13),
            "sephardi",
            "hebrew",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ",
        ),
        (dt.date(2025, 4, 25), "sephardi", "english", "Morid ha-tal - Barkheinu"),
        (dt.date(2025, 4, 25), "ashkenazi", "english", "(Silence) - VeTen Beracha"),
        (dt.date(2025, 4, 25), "ashkenazi", "hebrew", "(שתיקה) - וְתֵן בְּרָכָה"),
        (
            dt.date(2026, 10, 10),
            "ashkenazi",
            "english",
            "Mashiv ha-ruach u-morid ha-geshem - VeTen Beracha",
        ),
        (
            dt.date(2026, 10, 10),
            "sephardi",
            "hebrew",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ",
        ),
    ],
)
@pytest.mark.parametrize("location", ["New York"], indirect=True)
def test_tekufot_prayer_for_date(
    date: dt.date, tradition: str, language: str, location: Location, expected: str
) -> None:
    """
    Tests that the method get_prayer_for_date returns the expected phrase
    for each combination of (date, tradition, language).
    """
    tekufot = Tekufot(
        date=date, location=location, tradition=tradition, language=language
    )
    actual_phrase = tekufot.get_prayer_for_date()
    assert actual_phrase == expected, (
        f"\nDate: {date}, Tradition: {tradition}, Langue: {language}\n"
        f"Expected : {expected}\n"
        f"Result : {actual_phrase}"
    )
