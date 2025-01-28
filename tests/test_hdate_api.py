"""
These tests are based on the API calls made to hdate by homeassistant (and
maybe other apps in the future).
"""

import datetime as dt
import sys
from typing import cast

import pytest
import syrupy
from _pytest.capture import CaptureFixture

from hdate import HDate, Location, Zmanim

_ASTRAL = "astral" in sys.modules


class TestHDateAPI:
    """Test the HDate API provided in the README."""

    def test_readme_example_english(self, capsys: CaptureFixture[str]) -> None:
        """Test the README example in English."""

        test_date = dt.date(2016, 4, 18)
        hdate = HDate(test_date, language="english")
        print(hdate)
        captured = capsys.readouterr()
        assert captured.out == "Monday 10 Nisan 5776\n"

    def test_readme_example_hebrew(self, capsys: CaptureFixture[str]) -> None:
        """Test the README example in Hebrew."""
        test_date = dt.date(2016, 4, 26)
        hdate = HDate(test_date, language="hebrew")
        print(hdate)
        captured = capsys.readouterr()
        assert captured.out == "יום שלישי י\"ח בניסן ה' תשע\"ו ג' לעומר חול המועד פסח\n"

    def test_get_hebrew_date(self) -> None:
        """Print the hebrew date."""
        test_date = dt.datetime(2018, 11, 2)
        assert str(HDate(test_date).hdate) == 'כ"ד מרחשוון ה\' תשע"ט'
        assert str(HDate(test_date, language="english").hdate) == "24 Marcheshvan 5779"
        assert str(HDate(test_date, language="french").hdate) == "24 Heshvan 5779"

    def test_get_upcoming_parasha(self) -> None:
        """Check that the upcoming parasha is correct."""
        test_date = dt.datetime(2018, 11, 2)
        assert str(HDate(test_date).parasha) == "חיי שרה"
        assert str(HDate(test_date, language="english").parasha) == "Chayei Sara"

    def test_get_upcoming_parasha_vezot_habracha(self) -> None:
        """Check that the upcoming parasha is correct for vezot habracha."""
        test_date = dt.datetime(2018, 9, 30)
        assert str(HDate(test_date).parasha) == "וזאת הברכה"
        assert str(HDate(test_date, language="english").parasha) == "Vezot Habracha"
        assert str(HDate(test_date, language="french").parasha) == "Vezot Haberakha"

    def test_get_holiday_description(self) -> None:
        """Check that the holiday description is correct."""
        test_date = dt.datetime(2018, 12, 3)
        assert str(HDate(test_date).holidays[0]) == "חנוכה"
        assert str(HDate(test_date, language="english").holidays[0]) == "Chanukah"
        assert str(HDate(test_date, language="french").holidays[0]) == "Hanoukka"


class TestZmanimAPI:
    """Test the API provided in the README."""

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_readme_example_hebrew(
        self, location: Location, snapshot: syrupy.assertion.SnapshotAssertion
    ) -> None:
        """Test for hebrew."""
        zman = Zmanim(date=dt.date(2016, 4, 18), location=location)
        if not _ASTRAL:
            return
        assert str(zman) == snapshot

    @pytest.mark.parametrize("location", ["Petah Tikva"], indirect=True)
    def test_readme_example_english(
        self, location: Location, snapshot: syrupy.assertion.SnapshotAssertion
    ) -> None:
        """Test for english."""
        zman = Zmanim(date=dt.date(2016, 4, 18), location=location, language="english")
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
