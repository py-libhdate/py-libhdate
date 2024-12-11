"""Tests for the TranslatorMixin class."""

import pytest

from hdate.translator import TranslatorMixin

# pylint: disable=redefined-outer-name


@pytest.fixture
def translator() -> type[TranslatorMixin]:
    """Return the TranslatorMixin class."""

    class Translator(TranslatorMixin):
        """Dummy Translator class."""

        TISHREI = 1

    return Translator


@pytest.fixture
def translator_instance(translator: type[TranslatorMixin]) -> TranslatorMixin:
    """Return an instance of the TranslatorMixin class."""
    return translator()


def test_available_languages(translator_instance: TranslatorMixin) -> None:
    """Test the available_languages method."""
    known_languages = ["english", "french", "hebrew"]
    for language in known_languages:
        assert language[:2] in translator_instance.available_languages()


def test_load_language(translator: type[TranslatorMixin]) -> None:
    """Test the load_language method."""
    translator.__name__ = "months"

    inst = translator()
    inst.load_translations()
    assert inst.get_translation("TISHREI") == "Tishrei"
