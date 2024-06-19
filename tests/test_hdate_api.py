"""
These tests are based on the API calls made to hdate by homeassistant (and
maybe other apps in the future).
"""

import sys
from datetime import date, datetime

from hdate import HDate, Location, Zmanim

_ASTRAL = "astral" in sys.modules


class TestHDateAPI:
    """Test the HDate API provided in the README."""

    def test_readme_example_english(self, capsys):
        """Test the README example in English."""

        test_date = date(2016, 4, 18)
        hdate = HDate(test_date, hebrew=False)
        print(hdate)
        captured = capsys.readouterr()
        assert captured.out == "Monday 10 Nisan 5776\n"

    def test_readme_example_hebrew(self, capsys):
        """Test the README example in Hebrew."""
        test_date = date(2016, 4, 26)
        hdate = HDate(test_date, hebrew=True)
        print(hdate)
        captured = capsys.readouterr()
        assert captured.out == "יום שלישי י\"ח בניסן ה' תשע\"ו ג' בעומר חול המועד פסח\n"

    def test_get_hebrew_date(self):
        """Print the hebrew date."""
        test_date = datetime(2018, 11, 2)
        assert HDate(test_date).hebrew_date == 'כ"ד מרחשוון ה\' תשע"ט'
        assert HDate(test_date, hebrew=False).hebrew_date == "24 Marcheshvan 5779"

    def test_get_upcoming_parasha(self):
        """Check that the upcoming parasha is correct."""
        test_date = datetime(2018, 11, 2)
        assert HDate(test_date).parasha == "חיי שרה"
        assert HDate(test_date, hebrew=False).parasha == "Chayei Sara"

    def test_get_upcoming_parasha_vezot_habracha(self):
        """Check that the upcoming parasha is correct for vezot habracha."""
        test_date = datetime(2018, 9, 30)
        assert HDate(test_date).parasha == "וזאת הברכה"
        assert HDate(test_date, hebrew=False).parasha == "Vezot Habracha"

    def test_get_holiday_description(self):
        """Check that the holiday description is correct."""
        test_date = datetime(2018, 12, 3)
        assert HDate(test_date).holiday_description == "חנוכה"
        assert HDate(test_date, hebrew=False).holiday_description == "Chanukah"


class TestZmanimAPI:
    """Test the API provided in the README."""

    def test_readme_example_hebrew(self, capsys):
        """Test for hebrew."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=date(2016, 4, 18), location=coord)
        print(zman)
        captured = capsys.readouterr()
        if not _ASTRAL:
            return
        assert (
            captured.out == "עלות השחר - 04:52:00\n"
            "זמן טלית ותפילין - 05:18:00\n"
            "הנץ החמה - 06:08:00\n"
            'סוף זמן ק"ש מג"א - 08:46:00\n'
            'סוף זמן ק"ש גר"א - 09:23:00\n'
            'סוף זמן תפילה מג"א - 10:04:00\n'
            'סוף זמן תפילה גר"א - 10:28:00\n'
            "חצות היום - 12:40:00\n"
            "מנחה גדולה - 13:10:30\n"
            "מנחה קטנה - 16:25:30\n"
            "פלג המנחה - 17:50:45\n"
            "שקיעה - 19:12:00\n"
            "צאת הכוכבים - 19:38:00\n"
            "חצות הלילה - 00:40:00\n"
        )

    def test_readme_example_english(self, capsys):
        """Test for english."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=date(2016, 4, 18), location=coord, hebrew=False)
        print(zman)
        captured = capsys.readouterr()
        if not _ASTRAL:
            return
        assert (
            captured.out == "Alot HaShachar - 04:52:00\n"
            "Talit & Tefilin's time - 05:18:00\n"
            "Sunrise - 06:08:00\n"
            'Shema EOT MG"A - 08:46:00\n'
            'Shema EOT GR"A - 09:23:00\n'
            'Tefila EOT MG"A - 10:04:00\n'
            'Tefila EOT GR"A - 10:28:00\n'
            "Midday - 12:40:00\n"
            "Big Mincha - 13:10:30\n"
            "Small Mincha - 16:25:30\n"
            "Plag Mincha - 17:50:45\n"
            "Sunset - 19:12:00\n"
            "First stars - 19:38:00\n"
            "Midnight - 00:40:00\n"
        )

    def test_issur_melacha_weekday(self):
        """Test for issur melacha on a weekday."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=date(2018, 11, 12), location=coord)
        assert not zman.issur_melacha_in_effect

    def test_issur_melacha_shabbat_morning(self):
        """Test for issur melacha on shabbat morning."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2018, 11, 10, 9), location=coord)
        assert zman.issur_melacha_in_effect

    def test_issur_melacha_friday_morning(self):
        """Test for issur melacha on friday morning."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2018, 11, 9, 9, 45), location=coord)
        assert not zman.issur_melacha_in_effect

    def test_issur_melacha_friday_evening(self):
        """Test for issur melacha on friday evening."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2018, 11, 9, 16, 45), location=coord)
        assert zman.issur_melacha_in_effect

    def test_issur_melacha_motsaei_shabbat(self):
        """Test for issur melacha on Motsaei shabbat."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2018, 11, 10, 17, 45), location=coord)
        assert not zman.issur_melacha_in_effect

    def test_issur_melacha_shavuot_morning(self):
        """Test for issur melacha on shavuot morning."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2019, 6, 9, 9), location=coord)
        assert zman.issur_melacha_in_effect

    def test_issur_melacha_pesach_vi_morning(self):
        """Test for issur melacha on erev shvii shel pesach morning."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2019, 4, 25, 9, 45), location=coord)
        assert not zman.issur_melacha_in_effect

    def test_issur_melacha_shavuot_evening(self):
        """Test for issur melacha on shavuot evening."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2019, 6, 8, 21, 45), location=coord)
        assert zman.issur_melacha_in_effect

    def test_issur_melacha_motsaei_shavuot(self):
        """Test for issur melacha on motsaei shavuot."""
        coord = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        zman = Zmanim(date=datetime(2019, 6, 9, 20, 30), location=coord)
        assert not zman.issur_melacha_in_effect

    def test_issur_melacha_pesach_ii_morning(self):
        """Test for issur melacha on the second day of pesach in the diaspora."""
        coord = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        zman = Zmanim(date=datetime(2019, 4, 21, 9), location=coord)
        assert zman.issur_melacha_in_effect

    def test_issur_melacha_pesach_ii_evening(self):
        """Test for issur melacha on the eve of second day of pesach in the diaspora."""
        coord = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        zman = Zmanim(date=datetime(2019, 4, 20, 21, 45), location=coord)
        assert zman.issur_melacha_in_effect

    def test_issur_melacha_motsaei_pesach_ii(self):
        """Test for issur melacha on the end of second day of pesach in the diaspora."""
        coord = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        zman = Zmanim(date=datetime(2019, 4, 21, 20, 30), location=coord)
        assert not zman.issur_melacha_in_effect

    def test_zmanim_localized_datetime(self):
        """Test for issur melacha if datetime is localized."""
        coord = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        zman = Zmanim(
            date=datetime(2019, 4, 21, 20, 30, tzinfo=coord.timezone), location=coord
        )
        assert not zman.issur_melacha_in_effect
