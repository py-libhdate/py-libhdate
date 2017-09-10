# -*- coding: utf-8 -*-

from builtins import str
from builtins import object
import pytest
import hdate.hdate_string as hs
import hdate.htables as ht

import random


class TestOmer(object):
    """Test get_omer_string"""

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
        (1, "א'", "א"),
        (9, "ט'", "ט"),
        (10, "י'", "י"),
        (11, "י\"א", "יא"),
        (15, "ט\"ו", "טו"),
        (127, "קכ\"ז", "קכז"),
        (435, "תל\"ה", "תלה"),
        (770, "תש\"ע", "תשע"),
        (969, "תתקס\"ט", "תתקסט"),
        (1015, "א' ט\"ו", "א' טו")
    ]

    @pytest.mark.parametrize("number,expected_string,expected_short", NUMBERS)
    def test_hebrew_number(self, number, expected_string, expected_short):
        assert hs.hebrew_number(number) == expected_string.decode("utf-8")

    @pytest.mark.parametrize("number,expected_string,expected_short", NUMBERS)
    def test_hebrew_number_short_true(self, number, expected_string,
                                      expected_short):
        assert (hs.hebrew_number(number, short=True) ==
                expected_short.decode("utf-8"))

    def test_illegal_value(self):
        with pytest.raises(ValueError):
            hs.hebrew_number(random.randint(10000, 20000))
        with pytest.raises(ValueError):
            hs.hebrew_number(random.randint(-100, 0))

    def test_hebrew_number_hebrew_false(self):
        number = random.randint(0, 100000)
        assert hs.hebrew_number(number, hebrew=False) == str(number)

    def test_hebrew_number_hebrew_false_short_true(self):
        number = random.randint(0, 100000)
        assert (hs.hebrew_number(number, hebrew=False, short=True) ==
                str(number))


class TestParasha(object):
    """Test parasha strings"""

    def test_get_parasha_default_args(self):
        parasha = random.randint(0, 61)
        assert hs.get_parashe(parasha) == hs.get_parashe(parasha, short=False,
                                                         hebrew=True)

    def test_get_parasha_hebrew_long(self):
        parasha = random.randint(0, 61)
        parasha_string = hs.get_parashe(parasha, short=False, hebrew=True)
        assert parasha_string.decode("utf-8")[:4] == "פרשת".decode("utf-8")

    def test_get_parasha_hebrew_short(self):
        parasha = random.randint(0, 61)
        parasha_string = hs.get_parashe(parasha, short=True, hebrew=True)
        assert parasha_string == ht.PARASHAOT[1][parasha]

    def test_get_parasha_english_long(self):
        parasha = random.randint(0, 61)
        parasha_string = hs.get_parashe(parasha, short=False, hebrew=False)
        assert parasha_string == "Parashat {}".format(ht.PARASHAOT[0][parasha])

    def test_get_parasha_english_short(self):
        parasha = random.randint(0, 61)
        parasha_string = hs.get_parashe(parasha, short=True, hebrew=False)
        assert parasha_string == ht.PARASHAOT[0][parasha]
