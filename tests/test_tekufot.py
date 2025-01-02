"""Test Tekufot objects."""

import datetime as dt

import pytest

from hdate.location import Location
from hdate.tekufot import Tekufot

# 1) Create a dictionary mapping each unique combination of (date, tradition, language)
#    to the exact phrase you expect.
#    Replace the placeholder strings ("Phrase_1", etc.) with the real phrases you have.
EXPECTED_PHRASES = {
    (
        "2024-12-13",
        "ashkenazi",
        "english",
    ): "Mashiv ha-ruach u-morid ha-geshem - VeTen Tal uMatar Livracha",
    (
        "2024-12-13",
        "sephardi",
        "hebrew",
    ): "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ",
    (
        "2025-04-25",
        "sephardi",
        "english",
    ): "Morid ha-tal - Barkheinu",
    (
        "2025-04-25",
        "ashkenazi",
        "english",
    ): "(Silence) - VeTen Beracha",
    (
        "2025-04-25",
        "ashkenazi",
        "hebrew",
    ): "(שתיקה) - וְתֵן בְּרָכָה",
    (
        "2026-10-10",
        "ashkenazi",
        "english",
    ): "Mashiv ha-ruach u-morid ha-geshem - VeTen Beracha",
    (
        "2026-10-10",
        "sephardi",
        "hebrew",
    ): "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ",
}


class TestTekufot:
    """Tests for the Tekufot class."""

    @pytest.fixture
    def default_values(self) -> Tekufot:
        """Create a Tekufot object for today's date with default settings."""
        loc = Location(
            name="Jerusalem",
            latitude=31.778,
            longitude=35.235,
            timezone="Asia/Jerusalem",
            diaspora=False,
        )
        return Tekufot(
            date=dt.date.today(),
            location=loc,
            language="english",
            tradition="sephardi",
        )

    @pytest.mark.parametrize(
        "date_str,tradition,language",
        [
            ("2024-12-13", "ashkenazi", "english"),
            ("2024-12-13", "sephardi", "hebrew"),
            ("2025-04-25", "sephardi", "english"),
            ("2025-04-25", "ashkenazi", "english"),
            ("2025-04-25", "ashkenazi", "hebrew"),
            ("2026-10-10", "ashkenazi", "english"),
            ("2026-10-10", "sephardi", "hebrew"),
        ],
    )
    def test_tekufot_prayer_for_date(
        self: "TestTekufot", date_str: str, tradition: str, language: str
    ) -> None:
        """
        Tests that the method get_prayer_for_date returns the expected phrase
        for each combination of (date, tradition, language).
        """

        loc = Location(
            name="TestLocation",
            latitude=40.0,
            longitude=-74.0,
            timezone="America/New_York",
            diaspora=True,
        )

        tekufot = Tekufot(
            date=dt.datetime.strptime(date_str, "%Y-%m-%d").date(),
            location=loc,
            tradition=tradition,
            language=language,
        )

        actual_phrase = tekufot.get_prayer_for_date()

        expected_phrase = EXPECTED_PHRASES[(date_str, tradition, language)]
        assert actual_phrase == expected_phrase, (
            f"\nDate: {date_str}, Tradition: {tradition}, Langue: {language}\n"
            f"Expected : {expected_phrase}\n"
            f"Result : {actual_phrase}"
        )
