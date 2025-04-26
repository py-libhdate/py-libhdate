"""Tests for the Daf Yomi attribute."""

import datetime as dt

from hdate import HDateInfo
from hdate.translator import set_language


def test_daf_yomi() -> None:
    """Test value of Daf Yomi."""
    # Random test date
    set_language("en")
    assert str(HDateInfo(date=dt.date(2014, 4, 28)).daf_yomi) == "Beitzah 29"
    # Beginning/end of cycle:
    assert str(HDateInfo(date=dt.date(2020, 1, 4)).daf_yomi) == "Niddah 73"
    assert str(HDateInfo(date=dt.date(2020, 1, 5)).daf_yomi) == "Berachos 2"
    set_language("he")
    assert str(HDateInfo(date=dt.date(2020, 3, 7)).daf_yomi) == "ברכות סד"
    assert str(HDateInfo(date=dt.date(2020, 3, 8)).daf_yomi) == "שבת ב"
