"""Tests for the TranslatorMixin class."""

from hdate.htables import Months


def test_available_languages() -> None:
    """Test the available_languages method."""
    known_languages = ["english", "french", "hebrew"]
    month = Months.TISHREI
    for language in known_languages:
        assert language[:2] in month.available_languages()


def test_load_language() -> None:
    """Test the load_language method."""
    month = Months.TISHREI
    assert str(month) == "Tishrei"
