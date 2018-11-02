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
        assert HDate(test_date).hebrew_date == "כ\"ד מרחשוון ה\' תשע\"ט"
        assert HDate(
            test_date, hebrew=False).hebrew_date == "24 Marcheshvan 5779"
