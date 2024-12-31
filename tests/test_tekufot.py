"""Test Tekufot objects."""

import datetime as dt

import pytest

from hdate.location import Location
from hdate.tekufot import Tekufot

# 1) Define the test matrix: 3 dates and 3 (tradition, language) combos

TRAD_LANG_COMBOS = [
    ("israel", "english"),
    ("diaspora_ashkenazi", "french"),
    ("diaspora_sephardi", "hebrew"),
]

# 2) Create a dictionary mapping each unique combination of (date, tradition, language)
#    to the exact phrase you expect.
#    Replace the placeholder strings ("Phrase_1", etc.) with the real phrases you have.
EXPECTED_PHRASES = {
    (
        "2024-12-13",
        "israel",
        "english",
    ): "Mashiv ha-ruach u-morid ha-geshem - Barech aleinu",
    (
        "2024-12-13",
        "diaspora_ashkenazi",
        "french",
    ): "Machiv ha-roua'h oumoride ha-guéchem - Barech aleinu",
    (
        "2024-12-13",
        "diaspora_sephardi",
        "hebrew",
    ): "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ",
    (
        "2025-04-25",
        "israel",
        "english",
    ): "Morid ha-tal - Barkheinu",
    (
        "2025-04-25",
        "diaspora_ashkenazi",
        "french",
    ): "(Silence) - Barkhénou",
    (
        "2025-04-25",
        "diaspora_sephardi",
        "hebrew",
    ): "מוֹרִיד הַטַּל - בָּרְכֵנוּ",
    (
        "2026-10-10",
        "israel",
        "english",
    ): "Mashiv ha-ruach u-morid ha-geshem - Barkheinu",
    (
        "2026-10-10",
        "diaspora_ashkenazi",
        "french",
    ): "Machiv ha-roua'h oumoride ha-guéchem - Barkhénou",
    (
        "2026-10-10",
        "diaspora_sephardi",
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
            diaspora=False,
            location=loc,
            language="english",
            tradition="israel",
        )

    @pytest.mark.parametrize(
        "date_str,tradition,language",
        [
            (d, t, l)
            for d in ["2024-12-13", "2025-04-25", "2026-10-10"]
            for (t, l) in TRAD_LANG_COMBOS
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
            diaspora=(tradition != "israel"),  # diaspora=True Outside Israel
        )

        tekufot = Tekufot(
            date=dt.datetime.strptime(date_str, "%Y-%m-%d").date(),
            diaspora=(tradition != "israel"),
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
