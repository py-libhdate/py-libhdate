"""Tests relating to hebrew numbering with letters."""

import random

import pytest

import hdate.date as dt


class TestOmer:
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
        (49, "היום תשעה וארבעים יום שהם שבעה שבועות לעומר"),
    ]

    @pytest.mark.parametrize("omer_day,hebrew_string", OMER_STRINGS)
    def test_get_omer_string(self, omer_day, hebrew_string):
        """Test the value returned by calculating the Omer string."""
        assert dt.get_omer_string(omer_day) == hebrew_string

    def test_illegal_value(self):
        """Test passing illegal values to Omer."""
        with pytest.raises(ValueError):
            dt.get_omer_string(random.randint(50, 100))
        with pytest.raises(ValueError):
            dt.get_omer_string(random.randint(-100, 0))


class TestHebrewNumbers:
    """Test hebrew_number"""

    NUMBERS = [
        (1, "א'", "א"),
        (9, "ט'", "ט"),
        (10, "י'", "י"),
        (11, 'י"א', "יא"),
        (15, 'ט"ו', "טו"),
        (127, 'קכ"ז', "קכז"),
        (435, 'תל"ה', "תלה"),
        (770, 'תש"ע', "תשע"),
        (969, 'תתקס"ט', "תתקסט"),
        (1015, "א' ט\"ו", "א' טו"),
    ]

    @pytest.mark.parametrize("number,expected_string,expected_short", NUMBERS)
    def test_hebrew_number(self, number, expected_string, expected_short):
        """Test the calculating the hebrew string."""
        assert dt.hebrew_number(number, short=True) == expected_short
        assert dt.hebrew_number(number) == expected_string

    def test_illegal_value(self):
        """Test unsupported numbers."""
        with pytest.raises(ValueError):
            dt.hebrew_number(random.randint(10000, 20000))
        with pytest.raises(ValueError):
            dt.hebrew_number(random.randint(-100, -1))

    def test_hebrew_number_hebrew_false(self):
        """Test returning a non-hebrew number."""
        number = random.randint(0, 100000)
        assert dt.hebrew_number(number, hebrew=False) == str(number)
        assert dt.hebrew_number(number, hebrew=False, short=True) == str(number)
