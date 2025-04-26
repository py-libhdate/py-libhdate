"""Test hebrew_number"""

import pytest
from hypothesis import given, strategies

from hdate import gematria
from hdate.translator import set_language

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


@given(
    number=strategies.one_of(
        strategies.integers(max_value=-1), strategies.integers(min_value=10001)
    )
)
def test_illegal_value(number: int) -> None:
    """Test unsupported numbers."""
    with pytest.raises(ValueError):
        gematria.hebrew_number(number)


@given(number=strategies.integers(min_value=0, max_value=10000))
def test_hebrew_number_hebrew_false(number: int) -> None:
    """Test returning a non-hebrew number."""
    set_language("en")
    assert gematria.hebrew_number(number) == str(number)
    assert gematria.hebrew_number(number, short=True) == str(number)
