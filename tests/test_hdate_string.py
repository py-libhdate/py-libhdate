# -*- coding: utf-8 -*-

import random

import pytest

import hdate.date as dt

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic


class TestOmer(object):
    """Test get_omer_string"""

    OMER_STRINGS = [
        (1, u"היום יום אחד לעומר"),
        (2, u"היום שני ימים לעומר"),
        (3, u"היום שלושה ימים לעומר"),
        (7, u"היום שבעה ימים שהם שבוע אחד לעומר"),
        (8, u"היום שמונה ימים שהם שבוע אחד ויום אחד לעומר"),
        (10, u"היום עשרה ימים שהם שבוע אחד ושלושה ימים לעומר"),
        (13, u"היום שלושה עשר יום שהם שבוע אחד וששה ימים לעומר"),
        (14, u"היום ארבעה עשר יום שהם שני שבועות לעומר"),
        (17, u"היום שבעה עשר יום שהם שני שבועות ושלושה ימים לעומר"),
        (19, u"היום תשעה עשר יום שהם שני שבועות וחמשה ימים לעומר"),
        (28, u"היום שמונה ועשרים יום שהם ארבעה שבועות לעומר"),
        (30, u"היום שלושים יום שהם ארבעה שבועות ושני ימים לעומר"),
        (37, u"היום שבעה ושלושים יום שהם חמשה שבועות ושני ימים לעומר"),
        (45, u"היום חמשה וארבעים יום שהם ששה שבועות ושלושה ימים לעומר"),
        (49, u"היום תשעה וארבעים יום שהם שבעה שבועות לעומר"),
    ]

    @pytest.mark.parametrize("omer_day,hebrew_string", OMER_STRINGS)
    def test_get_omer_string(self, omer_day, hebrew_string):
        assert dt.get_omer_string(omer_day) == hebrew_string

    def test_illegal_value(self):
        with pytest.raises(ValueError):
            dt.get_omer_string(random.randint(50, 100))
        with pytest.raises(ValueError):
            dt.get_omer_string(random.randint(-100, 0))


class TestHebrewNumbers(object):
    """Test hebrew_number"""

    NUMBERS = [
        (1, u"א'", u"א"),
        (9, u"ט'", u"ט"),
        (10, u"י'", u"י"),
        (11, u'י"א', u"יא"),
        (15, u'ט"ו', u"טו"),
        (127, u'קכ"ז', u"קכז"),
        (435, u'תל"ה', u"תלה"),
        (770, u'תש"ע', u"תשע"),
        (969, u'תתקס"ט', u"תתקסט"),
        (1015, u"א' ט\"ו", u"א' טו"),
    ]

    @pytest.mark.parametrize("number,expected_string,expected_short", NUMBERS)
    def test_hebrew_number(self, number, expected_string, expected_short):
        assert dt.hebrew_number(number) == expected_string

    @pytest.mark.parametrize("number,expected_string,expected_short", NUMBERS)
    def test_hebrew_number_short_true(self, number, expected_string, expected_short):
        assert dt.hebrew_number(number, short=True) == expected_short

    def test_illegal_value(self):
        with pytest.raises(ValueError):
            dt.hebrew_number(random.randint(10000, 20000))
        with pytest.raises(ValueError):
            dt.hebrew_number(random.randint(-100, -1))

    def test_hebrew_number_hebrew_false(self):
        number = random.randint(0, 100000)
        assert dt.hebrew_number(number, hebrew=False) == str(number)

    def test_hebrew_number_hebrew_false_short_true(self):
        number = random.randint(0, 100000)
        assert dt.hebrew_number(number, hebrew=False, short=True) == str(number)
