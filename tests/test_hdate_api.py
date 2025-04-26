"""
These tests are based on the API calls made to hdate by homeassistant (and
maybe other apps in the future).
"""

import datetime as dt
import sys
from typing import cast

import pytest
from _pytest.capture import CaptureFixture
from syrupy.assertion import SnapshotAssertion

from hdate import HDateInfo, Location, Zmanim
from hdate.translator import Language, set_language

_ASTRAL = "astral" in sys.modules


class TestHDateAPI:
    """Test the HDateInfo API provided in the README."""

    def test_readme_example_english(self, capsys: CaptureFixture[str]) -> None:
        """Test the README example in English."""

        set_language("en")
        test_date = dt.date(2016, 4, 18)
        hdate = HDateInfo(test_date)
        print(hdate)
        captured = capsys.readouterr()
        assert captured.out == "Monday 10 Nisan 5776\n"

    def test_readme_example_hebrew(self, capsys: CaptureFixture[str]) -> None:
        """Test the README example in Hebrew."""
        test_date = dt.date(2016, 4, 26)
        hdate = HDateInfo(test_date)
        print(hdate)
        captured = capsys.readouterr()
        assert captured.out == "יום שלישי י\"ח בניסן ה' תשע\"ו ג' לעומר חול המועד פסח\n"

    @pytest.mark.parametrize(
        ("language", "expected"),
        [
            ("he", 'כ"ד מרחשוון ה\' תשע"ט'),
            ("en", "24 Marcheshvan 5779"),
            ("fr", "24 Heshvan 5779"),
        ],
    )
    def test_get_hebrew_date(self, language: Language, expected: str) -> None:
        """Print the hebrew date."""
        test_date = dt.datetime(2018, 11, 2)
        set_language(language)
        assert str(HDateInfo(test_date).hdate) == expected

    @pytest.mark.parametrize(
        ("language", "expected"),
        [("he", "חיי שרה"), ("en", "Chayei Sara"), ("fr", "Haye Sarah")],
    )
    def test_get_upcoming_parashs(self, language: Language, expected: str) -> None:
        """Check that the upcoming parasha is correct."""
        test_date = dt.datetime(2018, 11, 2)
        set_language(language)
        assert str(HDateInfo(test_date).parasha) == expected

    @pytest.mark.parametrize(
        ("language", "expected"),
        [("he", "וזאת הברכה"), ("en", "Vezot Habracha"), ("fr", "Vezot Haberakha")],
    )
    def test_get_upcoming_parasha_vezot_habracha(
        self, language: Language, expected: str
    ) -> None:
        """Check that the upcoming parasha is correct for vezot habracha."""
        test_date = dt.datetime(2018, 9, 30)
        set_language(language)
        assert str(HDateInfo(test_date).parasha) == expected

    @pytest.mark.parametrize(
        ("language", "expected"),
        [("he", "חנוכה"), ("en", "Chanukah"), ("fr", "Hanoukka")],
    )
    def test_get_holiday(self, language: Language, expected: str) -> None:
        """Check that the holiday description is correct."""
        test_date = dt.datetime(2018, 12, 3)
        set_language(language)
        assert str(HDateInfo(test_date).holidays[0]) == expected

    def test_gevurot_geshamim(self, snapshot: SnapshotAssertion) -> None:
        """Test the Gevurot Geshamim property."""

        test_date = dt.date(2025, 2, 6)
        assert HDateInfo(test_date).gevurot_geshamim == snapshot


class TestZmanimAPI:
    """Test the API provided in the README."""

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_readme_example_hebrew(
        self, location: Location, snapshot: SnapshotAssertion
    ) -> None:
        """Test for hebrew."""
        zman = Zmanim(date=dt.date(2016, 4, 18), location=location)
        if not _ASTRAL:
            return
        assert str(zman) == snapshot

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_readme_example_english(
        self, location: Location, snapshot: SnapshotAssertion
    ) -> None:
        """Test for english."""
        set_language("en")
        zman = Zmanim(date=dt.date(2016, 4, 18), location=location)
        if not _ASTRAL:
            return
        assert str(zman) == snapshot

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_weekday(self, location: Location) -> None:
        """Test for issur melacha on a weekday."""
        zman = Zmanim(date=dt.date(2018, 11, 12), location=location)
        assert not zman.issur_melacha_in_effect(dt.datetime(2018, 11, 12, 1, 2))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_shabbat_morning(self, location: Location) -> None:
        """Test for issur melacha on shabbat morning."""
        zman = Zmanim(date=dt.date(2018, 11, 10), location=location)
        assert zman.issur_melacha_in_effect(dt.datetime(2018, 11, 10, 9))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_friday_morning(self, location: Location) -> None:
        """Test for issur melacha on friday morning."""
        zman = Zmanim(date=dt.date(2018, 11, 9), location=location)
        assert not zman.issur_melacha_in_effect(dt.datetime(2018, 11, 9, 9, 45))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_friday_evening(self, location: Location) -> None:
        """Test for issur melacha on friday evening."""
        zman = Zmanim(date=dt.date(2018, 11, 9), location=location)
        assert zman.issur_melacha_in_effect(dt.datetime(2018, 11, 9, 16, 45))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_motsaei_shabbat(self, location: Location) -> None:
        """Test for issur melacha on Motsaei shabbat."""
        zman = Zmanim(date=dt.date(2018, 11, 10), location=location)
        assert not zman.issur_melacha_in_effect(dt.datetime(2018, 11, 10, 17, 45))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_shavuot_morning(self, location: Location) -> None:
        """Test for issur melacha on shavuot morning."""
        zman = Zmanim(date=dt.date(2019, 6, 9), location=location)
        assert zman.issur_melacha_in_effect(dt.datetime(2019, 6, 9, 9))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_pesach_vi_morning(self, location: Location) -> None:
        """Test for issur melacha on erev shvii shel pesach morning."""
        zman = Zmanim(date=dt.date(2019, 4, 25), location=location)
        assert not zman.issur_melacha_in_effect(dt.datetime(2019, 4, 25, 9, 45))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_shavuot_evening(self, location: Location) -> None:
        """Test for issur melacha on shavuot evening."""
        zman = Zmanim(date=dt.date(2019, 6, 8), location=location)
        assert zman.issur_melacha_in_effect(dt.datetime(2019, 6, 8, 21, 45))

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_issur_melacha_motsaei_shavuot(self, location: Location) -> None:
        """Test for issur melacha on motsaei shavuot."""
        zman = Zmanim(date=dt.date(2019, 6, 9), location=location)
        assert not zman.issur_melacha_in_effect(dt.datetime(2019, 6, 9, 20, 30))

    @pytest.mark.parametrize("location", ["New York"], indirect=True)
    def test_issur_melacha_pesach_ii_morning(self, location: Location) -> None:
        """Test for issur melacha on the second day of pesach in the diaspora."""
        zman = Zmanim(date=dt.date(2019, 4, 21), location=location)
        assert zman.issur_melacha_in_effect(dt.datetime(2019, 4, 21, 9))

    @pytest.mark.parametrize("location", ["New York"], indirect=True)
    def test_issur_melacha_pesach_ii_evening(self, location: Location) -> None:
        """Test for issur melacha on the eve of second day of pesach in the diaspora."""
        zman = Zmanim(date=dt.date(2019, 4, 20), location=location)
        assert zman.issur_melacha_in_effect(dt.datetime(2019, 4, 20, 21, 45))

    @pytest.mark.parametrize("location", ["New York"], indirect=True)
    def test_issur_melacha_motsaei_pesach_ii(self, location: Location) -> None:
        """Test for issur melacha on the end of second day of pesach in the diaspora."""
        zman = Zmanim(date=dt.date(2019, 4, 21), location=location)
        assert not zman.issur_melacha_in_effect(dt.datetime(2019, 4, 21, 20, 30))

    @pytest.mark.parametrize("location", ["New York"], indirect=True)
    def test_zmanim_localized_datetime(self, location: Location) -> None:
        """Test for issur melacha if datetime is localized."""
        _timezone = cast(dt.tzinfo, location.timezone)
        zman = Zmanim(date=dt.date(2019, 4, 21), location=location)
        assert not zman.issur_melacha_in_effect(
            dt.datetime(2019, 4, 21, 20, 30, tzinfo=_timezone)
        )
