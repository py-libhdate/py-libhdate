# -*- coding: utf-8 -*-

"""
These tests are based on the API calls made to hdate by homeassistant (and
maybe other apps in the future).
"""

from __future__ import print_function

from datetime import datetime

from hdate.date import HDate


class TestHDateAPI(object):

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
