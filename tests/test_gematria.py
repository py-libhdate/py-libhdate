"""Test hebrew_number"""

import random

import pytest

from hdate import gematria

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
def test_hebrew_number(number: int, expected_string: str, expected_short: str) -> None:
    """Test the calculating the hebrew string."""
    assert gematria.hebrew_number(number, short=True) == expected_short
    assert gematria.hebrew_number(number) == expected_string


def test_illegal_value() -> None:
    """Test unsupported numbers."""
    with pytest.raises(ValueError):
        gematria.hebrew_number(random.randint(10000, 20000))
    with pytest.raises(ValueError):
        gematria.hebrew_number(random.randint(-100, -1))


def test_hebrew_number_hebrew_false() -> None:
    """Test returning a non-hebrew number."""
    number = random.randint(0, 100000)
    assert gematria.hebrew_number(number, language="english") == str(number)
    assert gematria.hebrew_number(number, language="english", short=True) == str(number)
