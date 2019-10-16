# -*- coding: utf-8 -*-

"""
These tests are based on the API calls made to hdate by homeassistant (and
maybe other apps in the future).
"""

from __future__ import print_function

from datetime import date, datetime

from hdate import HDate, Location, Zmanim


class TestHDateAPI(object):
    def test_readme_example_english(self, capsys):
        test_date = date(2016, 4, 18)
        hdate = HDate(test_date, hebrew=False)
        print(hdate)
        captured = capsys.readouterr()
        assert captured.out == "Monday 10 Nisan 5776\n"

    def test_readme_example_hebrew(self, capsys):
        test_date = date(2016, 4, 26)
        hdate = HDate(test_date, hebrew=True)
        print(hdate)
        captured = capsys.readouterr()
        assert (
            captured.out == u"יום שלישי י\"ח בניסן ה' תשע\"ו ג' בעומר חול המועד פסח\n"
        )

    def test_get_hebrew_date(self):
        """Print the hebrew date."""
        test_date = datetime(2018, 11, 2)
        assert HDate(test_date).hebrew_date == u'כ"ד מרחשוון ה\' תשע"ט'
        assert HDate(test_date, hebrew=False).hebrew_date == "24 Marcheshvan 5779"

    def test_get_upcoming_parasha(self):
        """Check that the upcoming parasha is correct."""
        test_date = datetime(2018, 11, 2)
        assert HDate(test_date).parasha == u"חיי שרה"
        assert HDate(test_date, hebrew=False).parasha == "Chayei Sara"

    def test_get_upcoming_parasha_vezot_habracha(self):
        """Check that the upcoming parasha is correct for vezot habracha."""
        test_date = datetime(2018, 9, 30)
        assert HDate(test_date).parasha == u"וזאת הברכה"
        assert HDate(test_date, hebrew=False).parasha == "Vezot Habracha"

    def test_get_holiday_description(self):
        """Check that the holiday description is correct."""
        test_date = datetime(2018, 12, 3)
        assert HDate(test_date).holiday_description == u"חנוכה"
        assert HDate(test_date, hebrew=False).holiday_description == "Chanukah"


class TestZmanimAPI(object):
    def test_readme_example_hebrew(self, capsys):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=date(2016, 4, 18), location=c)
        print(z)
        captured = capsys.readouterr()
        assert (
            captured.out == u"עלות השחר - 04:53:00\n"
            u"זמן טלית ותפילין - 05:19:00\n"
            u"הנץ החמה - 06:09:00\n"
            u'סוף זמן ק"ש מג"א - 08:46:00\n'
            u'סוף זמן ק"ש הגר"א - 09:24:00\n'
            u'סוף זמן תפילה מג"א - 10:03:40\n'
            u'סוף זמן תפילה גר"א - 10:29:00\n'
            u"חצות היום - 12:39:00\n"
            u"מנחה גדולה - 13:11:30\n"
            u"מנחה קטנה - 16:26:30\n"
            u"פלג מנחה - 17:48:45\n"
            u"שקיעה - 19:10:00\n"
            u"צאת הככבים - 19:35:00\n"
            u"חצות הלילה - 00:39:00\n\n"
        )

    def test_readme_example_english(self, capsys):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=date(2016, 4, 18), location=c, hebrew=False)
        print(z)
        captured = capsys.readouterr()
        assert (
            captured.out == "Alot HaShachar - 04:53:00\n"
            "Talit & Tefilin's time - 05:19:00\n"
            "Sunrise - 06:09:00\n"
            'Shema EOT MG"A - 08:46:00\n'
            'Shema EOT GR"A - 09:24:00\n'
            'Tefila EOT MG"A - 10:03:40\n'
            'Tefila EOT GR"A - 10:29:00\n'
            "Midday - 12:39:00\n"
            "Big Mincha - 13:11:30\n"
            "Small Mincha - 16:26:30\n"
            "Plag Mincha - 17:48:45\n"
            "Sunset - 19:10:00\n"
            "First stars - 19:35:00\n"
            "Midnight - 00:39:00\n\n"
        )

    def test_issur_melacha_weekday(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=date(2018, 11, 12), location=c)
        assert not z.issur_melacha_in_effect

    def test_issur_melacha_shabbat_morning(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2018, 11, 10, 9), location=c)
        assert z.issur_melacha_in_effect

    def test_issur_melacha_friday_morning(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2018, 11, 9, 9, 45), location=c)
        assert not z.issur_melacha_in_effect

    def test_issur_melacha_friday_evening(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2018, 11, 9, 16, 45), location=c)
        assert z.issur_melacha_in_effect

    def test_issur_melacha_motsaei_shabbat(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2018, 11, 10, 17, 45), location=c)
        assert not z.issur_melacha_in_effect

    def test_issur_melacha_shavuot_morning(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2019, 6, 9, 9), location=c)
        assert z.issur_melacha_in_effect

    def test_issur_melacha_pesach_vi_mornng(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2019, 4, 25, 9, 45), location=c)
        assert not z.issur_melacha_in_effect

    def test_issur_melacha_shavuot_evening(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2019, 6, 8, 21, 45), location=c)
        assert z.issur_melacha_in_effect

    def test_issur_melacha_motsaei_shavuot(self):
        c = Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=datetime(2019, 6, 9, 20, 30), location=c)
        assert not z.issur_melacha_in_effect

    def test_issur_melacha_pesach_ii_morning(self):
        c = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        z = Zmanim(date=datetime(2019, 4, 21, 9), location=c)
        assert z.issur_melacha_in_effect

    def test_issur_melacha_pesach_ii_evening(self):
        c = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        z = Zmanim(date=datetime(2019, 4, 20, 21, 45), location=c)
        assert z.issur_melacha_in_effect

    def test_issur_melacha_motsaei_pesach_ii(self):
        c = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        z = Zmanim(date=datetime(2019, 4, 21, 20, 30), location=c)
        assert not z.issur_melacha_in_effect

    def test_zmanim_localized_datetime(self):
        c = Location(
            name="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            diaspora=True,
        )
        z = Zmanim(date=c.timezone.localize(datetime(2019, 4, 21, 20, 30)), location=c)
        assert not z.issur_melacha_in_effect
