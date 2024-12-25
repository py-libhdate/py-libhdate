"""Tests relating to Sefirat HaOmer."""

import random

import pytest

import hdate.date as dt

OMER_STRINGS = [
    (1, "היום יום אחד לעומר"),
    (2, "היום שני ימים לעומר"),
    (3, "היום שלושה ימים לעומר"),
    (7, "היום שבעה ימים שהם שבוע אחד לעומר"),
    (8, "היום שמונה ימים שהם שבוע אחד ויום אחד לעומר"),
    (10, "היום עשרה ימים שהם שבוע אחד ושלושה ימים לעומר"),
    (13, "היום שלושה עשר יום שהם שבוע אחד וששה ימים לעומר"),
    (14, "היום ארבעה עשר יום שהם שני שבועות לעומר"),
    (17, "היום שבעה עשר יום שהם שני שבועות ושלושה ימים לעומר"),
    (19, "היום תשעה עשר יום שהם שני שבועות וחמשה ימים לעומר"),
    (28, "היום שמונה ועשרים יום שהם ארבעה שבועות לעומר"),
    (30, "היום שלושים יום שהם ארבעה שבועות ושני ימים לעומר"),
    (37, "היום שבעה ושלושים יום שהם חמשה שבועות ושני ימים לעומר"),
    (45, "היום חמשה וארבעים יום שהם ששה שבועות ושלושה ימים לעומר"),
    (49, "היום תשעה וארבעים יום שהם שבעה שבועות לעומר"),
]


@pytest.mark.parametrize("omer_day,hebrew_string", OMER_STRINGS)
def test_get_omer_string(omer_day: int, hebrew_string: str) -> None:
    """Test the value returned by calculating the Omer string."""
    assert dt.get_omer_string(omer_day, language="hebrew") == hebrew_string


def test_illegal_value() -> None:
    """Test passing illegal values to Omer."""
    with pytest.raises(ValueError):
        dt.get_omer_string(random.randint(50, 100))
    with pytest.raises(ValueError):
        dt.get_omer_string(random.randint(-100, 0))
