"""Tests for the TranslatorMixin class."""

import typing

import pytest

from hdate.hebrew_date import Months
from hdate.translator import Language, TranslatorMixin, get_language, set_language


@pytest.mark.parametrize("language", typing.get_args(Language))
def test_available_languages(language: Language) -> None:
    """Test the available_languages method."""
    month = Months.TISHREI
    assert language[:2] in month.available_languages()


@pytest.mark.parametrize("language", typing.get_args(Language))
def test_set_language(language: Language) -> None:
    """Test the load_language method."""
    month = Months.TISHREI
    result = {"en": "Tishrei", "fr": "Tishri", "he": "תשרי"}
    set_language(language)
    assert str(month) == result[language]


def test_set_non_existing_language(caplog: pytest.LogCaptureFixture) -> None:
    """Test the load_language method."""
    set_language("non-existing-language")  # type: ignore
    assert (
        "Language non-existing-language not found, falling back to hebrew"
        in caplog.text
    )
    assert get_language() == "he"


def test_translation_not_found(caplog: pytest.LogCaptureFixture) -> None:
    """Test the get_translation method when no translation is available."""

    class Foo(TranslatorMixin):
        """Test class."""

    foo_class = Foo()
    assert foo_class.get_translation("non-existing-key") == "non-existing-key"
    assert "Translation for non-existing-key not found" in caplog.text
    with pytest.raises(NameError):
        str(foo_class)
