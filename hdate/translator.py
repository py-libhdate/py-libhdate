"""Translator base classes.

Classes using the translator base-classes will be able to pick up the correct string
based on the language specified.
"""

import logging
import sys
from enum import Enum
from typing import Any

from hdate.translations import TRANSLATIONS

_LOGGER = logging.getLogger(__name__)


class TranslatorMixin:
    """Translator Mixin class.

    Provides the capability of loading the correct string based on the language
    specified and the class name.
    """

    _language: str = "english"
    _translations: dict[str, str] = {}

    def __init__(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        if isinstance(self, Enum) and sys.version_info < (3, 11):
            super().__init__()
        else:
            super().__init__(*args, **kwargs)
        language = self._language
        if hasattr(self, "language"):
            language = getattr(self, "language")
        self.set_language(language)

    def __post_init__(self) -> None:
        language = self._language
        if hasattr(self, "language"):
            language = getattr(self, "language")
        self.set_language(language)

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

    def load_translations(self) -> None:
        """Load the translations for the class."""
        lang = self._language[:2]
        if lang not in TRANSLATIONS:
            _LOGGER.warning(
                "Language %s not found, falling back to english", self._language
            )
            lang = "en"
        object.__setattr__(
            self, "_translations", TRANSLATIONS[lang].get(self.__class__.__name__, {})
        )

    def get_translation(self, key: str) -> str:
        """Return the translation for the given key."""
        value = self._translations.get(key.lower(), None)
        if value is None:
            _LOGGER.error("Translation for %s not found", key)
            value = key
        return value

    def set_language(self, language: str) -> None:
        """Set the language for the translator."""
        object.__setattr__(self, "_language", language)
        self.load_translations()
        for _, attr in vars(self).items():
            if isinstance(attr, TranslatorMixin):
                attr.set_language(language)
