"""Tests for the TranslatorMixin class."""

import pytest

from hdate.hebrew_date import Months

LANGUAGES = ["english", "french", "hebrew"]


@pytest.mark.parametrize("language", LANGUAGES)
def test_available_languages(language: str) -> None:
    """Test the available_languages method."""
    month = Months.TISHREI
    assert language[:2] in month.available_languages()


@pytest.mark.parametrize("language", LANGUAGES)
def test_set_language(language: str) -> None:
    """Test the load_language method."""
    month = Months.TISHREI
    result = {
        "english": "Tishrei",
        "french": "Tishri",
        "hebrew": "תשרי",
    }
    month.set_language(language)
    assert str(month) == result[language]
