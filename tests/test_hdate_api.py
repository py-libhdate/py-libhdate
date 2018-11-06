# -*- coding: utf-8 -*-

"""
These tests are based on the API calls made to hdate by homeassistant (and
maybe other apps in the future).
"""

from __future__ import print_function

from collections import namedtuple
from datetime import date, datetime

from hdate import HDate, Zmanim

City = namedtuple(
    "City", ["name", "latitude", "longitude", "timezone", "elevation"])


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
        assert (captured.out ==
                u"יום שלישי י\"ח בניסן ה' תשע\"ו ג' בעומר חול המועד פסח\n")

    def test_get_hebrew_date(self):
        """Print the hebrew date."""
        test_date = datetime(2018, 11, 2)
        assert HDate(test_date).hebrew_date == u"כ\"ד מרחשוון ה\' תשע\"ט"
        assert HDate(
            test_date, hebrew=False).hebrew_date == "24 Marcheshvan 5779"

    def test_get_upcoming_parasha(self):
        """Check that the upcoming parasha is correct."""
        test_date = datetime(2018, 11, 2)
        assert HDate(test_date).parasha == u"חיי שרה"
        assert HDate(
            test_date, hebrew=False).parasha == "Chayei Sara"

    def test_get_upcoming_parasha_vezot_habracha(self):
        """Check that the upcoming parasha is correct for vezot habracha."""
        test_date = datetime(2018, 9, 30)
        assert HDate(test_date).parasha == u"וזאת הברכה"
        assert HDate(
            test_date, hebrew=False).parasha == "Vezot Habracha"

    def test_get_holiday_description(self):
        """Check that the holiday description is correct."""
        test_date = datetime(2018, 12, 3)
        assert HDate(test_date).holiday_description == u"חנוכה"
        assert HDate(
            test_date, hebrew=False).holiday_description == "Chanukah"


class TestZmanimAPI(object):

    def test_readme_example_hebrew(self, capsys):
        c = City("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=date(2016, 4, 18),
                   latitude=c.latitude, longitude=c.longitude,
                   timezone=c.timezone)
        print(z)
        captured = capsys.readouterr()
        assert (captured.out ==
                u"עלות השחר - 04:53\n"
                u"זמן טלית ותפילין - 05:19\n"
                u"הנץ החמה - 06:09\n"
                u"סוף זמן ק\"ש מג\"א - 08:46\n"
                u"סוף זמן ק\"ש הגר\"א - 09:24\n"
                u"סוף זמן תפילה מג\"א - 10:03\n"
                u"סוף זמן תפילה גר\"א - 10:29\n"
                u"חצות היום - 12:39\n"
                u"מנחה גדולה - 13:11\n"
                u"מנחה קטנה - 16:26\n"
                u"פלג מנחה - 17:48\n"
                u"שקיעה - 19:10\n"
                u"צאת הככבים - 19:35\n"
                u"חצות הלילה - 00:39\n\n")

    def test_readme_example_english(self, capsys):
        c = City("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
        z = Zmanim(date=date(2016, 4, 18),
                   latitude=c.latitude, longitude=c.longitude,
                   timezone=c.timezone, hebrew=False)
        print(z)
        captured = capsys.readouterr()
        assert (captured.out ==
                "Alot HaShachar - 04:53\n"
                "Talit & Tefilin\'s time - 05:19\n"
                "Sunrise - 06:09\n"
                "Shema EOT MG\"A - 08:46\n"
                "Shema EOT GR\"A - 09:24\n"
                "Tefila EOT MG\"A - 10:03\n"
                "Tefila EOT GR\"A - 10:29\n"
                "Midday - 12:39\n"
                "Big Mincha - 13:11\n"
                "Small Mincha - 16:26\n"
                "Plag Mincha - 17:48\n"
                "Sunset - 19:10\n"
                "First stars - 19:35\n"
                "Midnight - 00:39\n\n")
