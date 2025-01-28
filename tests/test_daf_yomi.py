"""Tests for the Daf Yomi attribute."""

import datetime as dt

from hdate import HDate


def test_daf_yomi() -> None:
    """Test value of Daf Yomi."""
    # Random test date
    myhdate = HDate(date=dt.date(2014, 4, 28), language="english")
    assert str(myhdate.daf_yomi) == "Beitzah 29"
    # Beginning/end of cycle:
    myhdate = HDate(date=dt.date(2020, 1, 4), language="english")
    assert str(myhdate.daf_yomi) == "Niddah 73"
    myhdate = HDate(date=dt.date(2020, 1, 5), language="english")
    assert str(myhdate.daf_yomi) == "Berachos 2"
    myhdate = HDate(date=dt.date(2020, 3, 7), language="hebrew")
    assert str(myhdate.daf_yomi) == "ברכות סד"
    myhdate = HDate(date=dt.date(2020, 3, 8), language="hebrew")
    assert str(myhdate.daf_yomi) == "שבת ב"
