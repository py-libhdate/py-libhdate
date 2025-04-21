"""Tests for the Daf Yomi attribute."""

import datetime as dt

from hdate import HDateInfo


def test_daf_yomi() -> None:
    """Test value of Daf Yomi."""
    # Random test date
    myhdate = HDateInfo(date=dt.date(2014, 4, 28), language="en")
    assert str(myhdate.daf_yomi) == "Beitzah 29"
    # Beginning/end of cycle:
    myhdate = HDateInfo(date=dt.date(2020, 1, 4), language="en")
    assert str(myhdate.daf_yomi) == "Niddah 73"
    myhdate = HDateInfo(date=dt.date(2020, 1, 5), language="en")
    assert str(myhdate.daf_yomi) == "Berachos 2"
    myhdate = HDateInfo(date=dt.date(2020, 3, 7), language="he")
    assert str(myhdate.daf_yomi) == "ברכות סד"
    myhdate = HDateInfo(date=dt.date(2020, 3, 8), language="he")
    assert str(myhdate.daf_yomi) == "שבת ב"
