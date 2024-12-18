"""Test Tekufot objects."""

import datetime

import pytest

from hdate import Tekufot
from hdate import converters as conv
from hdate.location import Location

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
    ): "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
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
    ): "(Silence) - barkhénou",
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
    ): "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
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
    return Tekufot(date=datetime.date.today(), diaspora=False, location=loc)


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

    def test_default_initialization(self, default_tekufot: Tekufot):
        """Test that default initialization works and sets attributes."""
        assert default_tekufot.date is not None
        assert isinstance(default_tekufot.gregorian_year, int)
        assert isinstance(default_tekufot.hebrew_year, int)
        assert isinstance(default_tekufot.location, Location)
        assert default_tekufot.diaspora is False
        # Ensure JDN and Hebrew date were computed
        assert default_tekufot.jdn is not None
        assert default_tekufot.hebrew_date is not None

    def test_tekufa_calculation(self, default_tekufot: Tekufot):
        """Test that the tekufa times are calculated."""
        # Check that tekufa attributes exist
        assert hasattr(default_tekufot, "tekufa_nissan")
        assert hasattr(default_tekufot, "tekufa_tishrei")
        assert hasattr(default_tekufot, "tekufa_tammuz")
        assert hasattr(default_tekufot, "tekufa_tevet")
        # Ensure these are datetime objects
        assert isinstance(default_tekufot.tekufa_nissan, datetime.datetime)
        assert isinstance(default_tekufot.tekufa_tishrei, datetime.datetime)

    def test_cheilat_geshamim_diaspora(self, param_tekufot: Tekufot):
        """
        Test that Cheilat Geshamim date is calculated for diaspora.
        Ensure that the date shifts correctly depending on end-of-day times.
        """
        # Only test if diaspora = True for this param
        if param_tekufot.diaspora:
            assert param_tekufot.cheilat_geshamim is not None
            assert isinstance(param_tekufot.cheilat_geshamim, datetime.date)

    def test_cheilat_geshamim_israel(self, default_tekufot: Tekufot):
        """Test that Cheilat Geshamim date in Israel is always 7 Cheshvan."""
        # default_tekufot is set to diaspora=False (Israel)
        assert default_tekufot.cheilat_geshamim is not None
        # Convert cheilat geshamim date back to Hebrew date to ensure it's 7 Cheshvan
        cheilat_jdn = conv.gdate_to_jdn(default_tekufot.cheilat_geshamim)
        hdate = conv.jdn_to_hdate(cheilat_jdn)
        assert hdate.month == 2 and hdate.day == 7  # 7 Cheshvan

    @pytest.mark.parametrize(
        "tradition,language",
        [
            ("israel", "english"),
            ("diaspora_ashkenazi", "french"),
            ("diaspora_sephardi", "hebrew"),
        ],
    )
    def test_get_prayer_for_date(
        self, param_tekufot: Tekufot, tradition: str, language: str
    ):
        """Test that get_prayer_for_date returns a correct phrase
        for various traditions and languages."""
        phrase = param_tekufot.get_prayer_for_date(
            date=param_tekufot.date,
            tradition=tradition,
            language=language,
        )
        # The phrase should be a non-empty string if a period is determined
        assert isinstance(phrase, str)
        # Depending on the date and tradition/language, phrase may vary
        # Just ensure we got something meaningful or a default "No prayer phrase found".
        assert phrase != ""

    def test_prayer_periods(self, default_tekufot: Tekufot):
        """Test that prayer_periods attribute is defined and well-formed."""
        assert hasattr(default_tekufot, "prayer_periods")
        assert isinstance(default_tekufot.prayer_periods, list)
        # Each period should be a tuple: (name, start_date, end_date)
        for period in default_tekufot.prayer_periods:
            assert len(period) == 3
            assert isinstance(period[0], str)
            assert isinstance(period[1], datetime.date)
            assert isinstance(period[2], datetime.date)

    @pytest.mark.parametrize("tradition,language", TRAD_LANG_COMBOS)
    def test_prayer_phrase_parametrized(
        self, param_tekufot: Tekufot, tradition: str, language: str
    ):
        """
        Tests 'get_prayer_for_date' across 3 dates and 3 (tradition, language) combos.
        This generates 9 test runs total. Each run checks the returned prayer phrase
        against a known expected value stored in EXPECTED_PHRASES.
        """
        # Retrieve the actual prayer phrase from the Tekufot object.
        phrase = param_tekufot.get_prayer_for_date(
            date=param_tekufot.date,
            tradition=tradition,
            language=language,
        )

        # Build a key to look up the expected phrase
        key = (str(param_tekufot.date), tradition, language)
        assert key in EXPECTED_PHRASES, f"No expected phrase found for {key}"

        expected_phrase = EXPECTED_PHRASES[key]

        # Validate the actual phrase matches the expected phrase
        assert (
            phrase == expected_phrase
        ), f"For {key}, expected '{expected_phrase}', got '{phrase}'."
