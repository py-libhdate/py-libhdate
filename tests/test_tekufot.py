"""Test Tekufot objects."""

import datetime as dt

import pytest

from hdate.location import Location
from hdate.tekufot import Tekufot


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
        "date, expected_tekufot_keys",
        [
            ("2024-04-07", ["Nissan", "Tammuz", "Tishrei", "Tevet"]),
            ("2025-04-07", ["Nissan", "Tammuz", "Tishrei", "Tevet"]),
        ],
    )
    def test_get_tekufot_dict(
        self, date: str, expected_tekufot_keys: list[str], default_values: Tekufot
    ) -> None:
        """Test that Tekufot calculations return the correct keys."""
        tekufot = Tekufot(
            date=dt.datetime.strptime(date, "%Y-%m-%d").date(),
            location=default_values.location,
        )
        result = tekufot.get_tekufot()
        assert set(result.keys()) == set(expected_tekufot_keys), "Tekufot keys mismatch"

    @pytest.mark.parametrize(
        "date, expected_tekufot",
        [
            (
                "2024-11-01",
                {
                    "Tishrei": dt.datetime(2024, 10, 7, 3, 0),
                    "Tevet": dt.datetime(2025, 1, 6, 10, 30),
                    "Nissan": dt.datetime(2025, 4, 7, 18, 0),
                    "Tammuz": dt.datetime(2025, 7, 8, 1, 30),
                },
            ),
            (
                "2026-04-07",
                {
                    "Tishrei": dt.datetime(2025, 10, 7, 9, 0),
                    "Tevet": dt.datetime(2026, 1, 6, 16, 30),
                    "Nissan": dt.datetime(2026, 4, 8, 0, 0),
                    "Tammuz": dt.datetime(2026, 7, 8, 7, 30),
                },
            ),
        ],
    )
    def test_get_tekufot(
        self,
        date: str,
        expected_tekufot: dict[str, dt.datetime],
        default_values: Tekufot,
    ) -> None:
        """Test that Tekufot calculations return the correct datetime values."""
        tekufot = Tekufot(
            date=dt.datetime.strptime(date, "%Y-%m-%d").date(),
            location=default_values.location,
        )
        result = tekufot.get_tekufot()

        tzinfo = (
            default_values.location.timezone
            if isinstance(default_values.location.timezone, dt.tzinfo)
            else dt.timezone.utc
        )
        for key, expected_dt in expected_tekufot.items():
            assert result[key] == expected_dt.replace(
                tzinfo=tzinfo
            ), f"Mismatch for {key}: expected {expected_dt}, got {result[key]}"

    @pytest.mark.parametrize(
        "date, diaspora, expected_start",
        [
            ("2024-10-05", True, "2024-12-05"),  # Diaspora start for rain prayers
            ("2024-10-05", False, "2024-11-08"),  # Israel start for rain prayers
        ],
    )
    def test_get_cheilat_geshamim(
        self, date: str, diaspora: bool, expected_start: str
    ) -> None:
        """Test Cheilat Geshamim start dates based on location."""
        loc = Location(
            name="TestLocation",
            latitude=31.778,
            longitude=35.235,
            timezone="Asia/Jerusalem",
            diaspora=diaspora,
        )
        tekufot = Tekufot(
            date=dt.datetime.strptime(date, "%Y-%m-%d").date(),
            location=loc,
        )
        result = tekufot.get_cheilat_geshamim()
        assert (
            result.strftime("%Y-%m-%d") == expected_start
        ), "Cheilat Geshamim date mismatch"

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
        expected_phrases = {
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

        expected_phrase = expected_phrases[(date_str, tradition, language)]
        assert actual_phrase == expected_phrase, (
            f"\nDate: {date_str}, Tradition: {tradition}, Langue: {language}\n"
            f"Expected : {expected_phrase}\n"
            f"Result : {actual_phrase}"
        )
