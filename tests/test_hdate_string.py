# -*- coding: utf-8 -*-

import pytest
import hdate.hdate_string as hs

import random


class TestOmer(object):
    """Test get_omer_string"""

    OMER_STRINGS = [
        (1, "היום יום אחד לעומר"),
        (2, "היום שני ימים לעומר"),
        (3, "היום שלושה ימים לעומר"),
        (7, "היום שבעה ימים שהם שבוע אחד לעומר"),
        (8, "היום שמונה ימים שהם שבוע אחד ויום אחד לעומר"),
        (13, "היום שלושה עשר יום שהם שבוע אחד וששה ימים לעומר"),
        (14, "היום ארבעה עשר יום שהם שני שבועות לעומר"),
        (17, "היום שבעה עשר יום שהם שני שבועות ושלושה ימים לעומר"),
        (19, "היום תשעה עשר יום שהם שני שבועות וחמשה ימים לעומר"),
        (28, "היום שמונה ועשרים יום שהם ארבעה שבועות לעומר"),
        (37, "היום שבעה ושלושים יום שהם חמשה שבועות ושני ימים לעומר"),
        (45, "היום חמשה וארבעים יום שהם ששה שבועות ושלושה ימים לעומר"),
        (49, "היום תשעה וארבעים יום שהם שבעה שבועות לעומר")
    ]

    @pytest.mark.parametrize("omer_day,hebrew_string", OMER_STRINGS)
    def test_get_omer_string(self, omer_day, hebrew_string):
        assert (hs.get_omer_string(omer_day).decode("utf-8") ==
                hebrew_string.decode("utf-8"))

    def test_illegal_value(self):
        with pytest.raises(ValueError):
            hs.get_omer_string(random.randint(50, 100))
        with pytest.raises(ValueError):
            hs.get_omer_string(random.randint(-100, 0))

class TestHebrewNumbers(object):
    """Test hebrew_number"""

    NUMBERS = [
        (1, "א'"),
        (9, "ט'"),
        (10, "י'"),
        (11, "י\"א"),
        (15, "ט\"ו"),
        (127, "קכ\"ז"),
        (435, "תל\"ה"),
        (770, "תש\"ע"),
        (969, "תתקס\"ט"),
        (1015, "א' ט\"ו")
    ]

    @pytest.mark.parametrize("number,expected_string", NUMBERS)
    def test_hebrew_number(self, number, expected_string):
        assert hs.hebrew_number(number) == expected_string.decode("utf-8")

    def test_illegal_value(self):
        with pytest.raises(ValueError):
            hs.hebrew_number(random.randint(10000, 20000))
        with pytest.raises(ValueError):
            hs.hebrew_number(random.randint(-100, 0))

    def test_hebrew_number_hebrew_false(self):
        number = random.randint(0,100000)
        assert hs.hebrew_number(number, hebrew=False) == str(number)

