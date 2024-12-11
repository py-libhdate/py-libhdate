"""Translator base classes.

Classes using the translator base-classes will be able to pick up the correct string
based on the language specified.
"""

import json
import logging
from pathlib import Path
from typing import Any

TRANSLATIONS_PATH = Path(__file__).parent / "translations"
_LOGGER = logging.getLogger(__name__)


class TranslatorMixin:
    """Translator Mixin class.

    Provides the capability of loading the correct string based on the language
    specified and the class name.
    """

    _language: str = "english"
    _translations: dict[str, str] = {}

    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        self.load_translations()
        super().__init__(*args, **kwargs)

    def available_languages(self) -> list[str]:
        """Return a list of available languages."""
        return [
            file.stem for file in TRANSLATIONS_PATH.iterdir() if file.suffix == ".json"
        ]

    def load_translations(self) -> None:
        """Load the translations for the class."""
        translation_file = TRANSLATIONS_PATH / f"{self._language[:2]}.json"
        if not translation_file.exists():
            _LOGGER.warning(
                "Translation file for %s not found, falling back to english",
                self._language,
            )
            translation_file = TRANSLATIONS_PATH / "en.json"

        all_translations = json.loads(translation_file.read_text(encoding="utf-8"))
        self._translations = all_translations.get(self.__class__.__name__.lower(), {})

    def get_translation(self, key: str) -> str:
        """Return the translation for the given key."""
        value = self._translations.get(key.lower(), None)
        if value is None:
            _LOGGER.error("Translation for %s not found", key)
            value = key
        return value

    def set_language(self, language: str) -> None:
        """Set the language for the translator."""
        self._language = language
        self.load_translations()
