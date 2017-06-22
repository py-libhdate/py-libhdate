# -*- coding: utf-8 -*-

import pytest
import hdate.hdate_string as hs

import random


class TestOmer(object):
    """Test Omer strings"""

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
