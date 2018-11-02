# -*- coding: utf-8 -*-

"""
These tests are based on the API calls made to hdate by homeassistant (and
maybe other apps in the future).
"""

from __future__ import print_function

from datetime import datetime

from hdate.date import HDate


class TestHDateAPI(object):

    def test_get_hdate_hebrew(self):
        """Print the hebrew date in hebrew."""
        test_date = datetime(2018, 11, 2)
        assert HDate(test_date).hebrew_date == "כ\"ד מרחשוון ה\' תשע\"ט"
