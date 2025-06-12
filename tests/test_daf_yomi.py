"""Tests for the Daf Yomi attribute."""

import datetime as dt

import pytest

from hdate import HDateInfo
from hdate.translator import Language, set_language


@pytest.mark.parametrize(
    ("language", "date", "expected"),
    [
        pytest.param("en", dt.date(2014, 4, 28), "Beitzah 29", id="random"),
        pytest.param("en", dt.date(2020, 1, 4), "Niddah 73", id="end of cycle"),
        pytest.param("en", dt.date(2020, 1, 5), "Berachos 2", id="beginning of cycle"),
        pytest.param("he", dt.date(2020, 3, 7), "ברכות סד", id="random_hebrew"),
        pytest.param("he", dt.date(2020, 3, 8), "שבת ב", id="start_masechet_hebrew"),
    ],
)
def test_daf_yomi(language: Language, date: dt.date, expected: str) -> None:
    """Test value of Daf Yomi."""
    set_language(language)
    assert HDateInfo(date=date).daf_yomi == expected
