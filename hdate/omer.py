"""Omer module."""

from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, auto
from typing import Union

from num2words import lang_HE, num2words

from hdate.gematria import hebrew_number
from hdate.hebrew_date import HebrewDate, Months
from hdate.translator import TranslatorMixin, get_language


class Nusach(Enum):
    """Nusach enum."""

    ASHKENAZ = auto()
    SFARAD = auto()
    ADOT_MIZRAH = auto()
    ITALIAN = auto()


@dataclass
class Omer(TranslatorMixin):
    """Hold information about the Omer count."""

    date: Union[HebrewDate, None] = None
    total_days: int = 0
    day: int = 0
    week: int = 0

    nusach: Nusach = Nusach.SFARAD

    def __post_init__(self) -> None:
        if self.date is None and self.total_days == self.day == self.week == 0:
            return
        if self.total_days not in range(50):
            raise ValueError("Invalid Omer day (if not counting, set to 0)")
        if self.week not in range(7) or self.day not in range(8):
            raise ValueError(f"Invalid Omer day ({self.day}) or week ({self.week})")
        first_omer_day = HebrewDate(month=Months.NISAN, day=16)
        last_omer_day = HebrewDate(month=Months.SIVAN, day=5)
        if self.date:
            if not first_omer_day <= self.date <= last_omer_day:
                self.total_days = 0
                self.day = 0
                self.week = 0
            else:
                first_omer_day = first_omer_day.replace(year=self.date.year)
                self.total_days = (self.date - first_omer_day).days + 1
                self.week, self.day = divmod(self.total_days, 7)
        elif self.total_days > 0:
            self.date = first_omer_day + timedelta(days=self.total_days - 1)
            self.week, self.day = divmod(self.total_days, 7)
        else:
            self.total_days = self.week * 7 + self.day
            self.date = first_omer_day + timedelta(days=self.total_days - 1)

    def __str__(self) -> str:
        if self.total_days == 0:
            return ""
        if self.nusach == Nusach.ASHKENAZ:
            suffix = self.get_translation(f"in_omer_{self.nusach.name}")
        else:
            suffix = self.get_translation("in_omer")
        return f"{hebrew_number(self.total_days)} {suffix}"

    def count_str(self) -> str:
        """Return the text to be said when counting the omer."""
        if self.total_days == 0:
            return ""

        language = get_language()

        def num2words_omer(number: int, _type: str = "total") -> str:
            """Wrapper for num2words."""
            if _type == "total":
                to = "ordinal"
                type_name = "day"
                if language == "he" and number in range(2, 11):
                    type_name = "days"
            else:
                to = "cardinal"
                type_name = _type if number == 1 else f"{_type}s"

            if language == "he":
                conv = lang_HE.Num2Word_HE()
                construct = number == 2
                if number > 20 and number % 10 != 0:
                    count_ones = conv.to_cardinal(number % 10, gender="m")
                    count_tens = conv.to_cardinal((number // 10) * 10, gender="m")
                    count = f"{count_ones} ו{count_tens}"
                else:
                    count = conv.to_cardinal(number, gender="m", construct=construct)
                _obj = self.get_translation(type_name)
                return f"{count} {_obj}" if number > 1 else f"{_obj} {count}"
            _obj = self.get_translation(type_name)
            count = num2words(number, lang=language[:2], to=to)
            if language == "en" and _type == "total":
                count = f"the {count}"
            if language == "fr" and number == 1 and type_name == "week":
                count = f"{count}e"
            return f"{count} {_obj}"

        total_days = num2words_omer(self.total_days, _type="total")
        in_omer = (
            self.get_translation("in_omer")
            if self.nusach != Nusach.ASHKENAZ
            else self.get_translation("in_omer_ashkenaz")
        )
        _is = self.get_translation("is")
        prefix = (
            f"{self.get_translation('today')} {_is}".strip()
            if self.nusach != Nusach.ITALIAN
            else f"{self.get_translation('today')} {in_omer} {_is}".strip()
        )
        detail = ""
        if self.week > 0:
            which_are = self.get_translation("which_are")
            weeks = num2words_omer(self.week, _type="week")
            detail = f" {which_are} {weeks}"
            detail = f",{detail}" if language != "he" else detail
            if self.day > 0:
                _and = self.get_translation("and")
                _and = f"{_and} " if language != "he" else _and
                days = num2words_omer(self.day, _type="day")
                detail = f"{detail} {_and}{days}"
        if self.nusach == Nusach.ITALIAN:
            return f"{prefix} {total_days}{detail}"
        if self.nusach == Nusach.ADOT_MIZRAH:
            return f"{prefix} {total_days} {in_omer}{detail}"
        return f"{prefix} {total_days}{detail} {in_omer}"
