"""Tests for the TranslatorMixin class."""

import pytest

from hdate.hebrew_date import Months
from hdate.translator import TranslatorMixin

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


def test_non_existing_language(caplog: pytest.LogCaptureFixture) -> None:
    """Test the load_language method."""
    month = Months.TISHREI
    month.set_language("non-existing-language")
    assert (
        "Language non-existing-language not found, falling back to english"
        in caplog.text
    )


def test_str_without_name() -> None:
    """Test the __str__ method."""

    class Foo(TranslatorMixin):
        """Test class."""

    foo_class = Foo()
    with pytest.raises(NameError):
        str(foo_class)
