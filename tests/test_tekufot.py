"""Test Tekufot objects."""

import datetime

import pytest

from hdate import converters as conv
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


@pytest.fixture
def default_tekufot() -> Tekufot:
    """Create a Tekufot object for today's date with default settings."""
    loc = Location(
        name="Jerusalem",
        latitude=31.778,
        longitude=35.235,
        timezone="Asia/Jerusalem",
        diaspora=False,
    )
    return Tekufot(
        date=datetime.date.today(),
        diaspora=False,
        location=loc,
        language="english",
        tradition="israel",
    )


@pytest.fixture(params=["2024-12-13", "2025-04-25", "2026-10-10"])
def param_tekufot(request) -> Tekufot:
    """Parameterized Tekufot object with various dates."""
    loc = Location(
        name="New York",
        latitude=40.7128,
        longitude=-74.0060,
        timezone="America/New_York",
        diaspora=True,
    )
    return Tekufot(date=request.param, diaspora=True, location=loc)


class TestTekufot:
    """Tests for the Tekufot class."""

    def test_default_initialization(self, default_tekufot: Tekufot) -> None:
        """Test that default initialization works and sets attributes."""
        assert default_tekufot.date is not None
        assert isinstance(default_tekufot.gregorian_year, int)
        assert isinstance(default_tekufot.hebrew_year, int)
        assert isinstance(default_tekufot.location, Location)
        assert default_tekufot.diaspora is False
        # Ensure JDN and Hebrew date were computed
        assert default_tekufot.jdn is not None
        assert default_tekufot.hebrew_date is not None

    def test_tekufa_calculation(self, default_tekufot: Tekufot) -> None:
        """Test that the tekufa times are calculated."""
        # Check that tekufa attributes exist
        assert hasattr(default_tekufot, "tekufa_nissan")
        assert hasattr(default_tekufot, "tekufa_tishrei")
        assert hasattr(default_tekufot, "tekufa_tammuz")
        assert hasattr(default_tekufot, "tekufa_tevet")
        # Ensure these are datetime objects
        assert isinstance(default_tekufot.tekufa_nissan, datetime.datetime)
        assert isinstance(default_tekufot.tekufa_tishrei, datetime.datetime)

    def test_cheilat_geshamim_diaspora(self, param_tekufot: Tekufot) -> None:
        """
        Test that Cheilat Geshamim date is calculated for diaspora.
        Ensure that the date shifts correctly depending on end-of-day times.
        """
        # Only test if diaspora = True for this param
        if param_tekufot.diaspora:
            assert param_tekufot.get_cheilat_geshamim is not None
            assert isinstance(param_tekufot.get_cheilat_geshamim(), datetime.date)

    def test_cheilat_geshamim_israel(self, default_tekufot: Tekufot) -> None:
        """Test that Cheilat Geshamim date in Israel is always 7 Cheshvan."""
        # default_tekufot is set to diaspora=False (Israel)
        assert default_tekufot.get_cheilat_geshamim is not None
        # Convert cheilat geshamim date back to Hebrew date to ensure it's 7 Cheshvan
        cheilat_jdn = conv.gdate_to_jdn(default_tekufot.get_cheilat_geshamim())
        hdate = conv.jdn_to_hdate(cheilat_jdn)
        assert hdate.month == 2 and hdate.day == 7  # 7 Cheshvan

    @pytest.mark.parametrize(
        "date_str,tradition,language",
        [
            (d, t, l)
            for d in ["2024-12-13", "2025-04-25", "2026-10-10"]
            for (t, l) in TRAD_LANG_COMBOS
        ],
    )
    def test_tekufot_prayer_for_date(self, date_str, tradition, language):
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
            date=date_str,
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
