"""Translator base classes.

Classes using the translator base-classes will be able to pick up the correct string
based on the language specified.
"""

import logging
from contextvars import ContextVar
from typing import Literal

from hdate.translations import TRANSLATIONS

_LOGGER = logging.getLogger(__name__)

Language = Literal["en", "fr", "he"]
context_language: ContextVar[Language] = ContextVar("context_language", default="he")


def set_language(language: Language) -> None:
    """Set the current translation language (context-local)."""
    if language not in TRANSLATIONS:
        _LOGGER.warning("Language %s not found, falling back to hebrew", language)
        language = "he"
    _ = context_language.set(language)


def get_language() -> Language:
    """Get the current translation language (context-local)."""
    return context_language.get()


class TranslatorMixin:
    """Translator Mixin class.

    Provides the capability of loading the correct string based on the language
    specified and the class name.
    """

    def __str__(self) -> str:
        if name := getattr(self, "name", None):
            return self.get_translation(name)
        raise NameError(
            f"Unable to translate {self.__class__.__name__}. "
            "It is missing the name attribute"
        )

    def available_languages(self) -> list[str]:
        """Return a list of available languages."""
        return list(TRANSLATIONS.keys())

    @property
    def translations(self) -> dict[str, str]:
        """Load the translations for the class."""
        lang = get_language()[:2]
        # lang will always be valid if set_language is called
        return TRANSLATIONS[lang].get(self.__class__.__name__, {})

    def get_translation(self, key: str) -> str:
        """Return the translation for the given key."""
        value = self.translations.get(key.lower(), None)
        if value is None:
            _LOGGER.error("Translation for %s not found", key)
            value = key
        return value
