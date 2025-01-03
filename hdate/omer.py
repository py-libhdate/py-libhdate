"""Omer module."""

from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, auto
from typing import Union

from hdate.gematria import hebrew_number
from hdate.hebrew_date import HebrewDate
from hdate.htables import Months
from hdate.translator import TranslatorMixin


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
    language: str = "hebrew"

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.date is None and self.total_days == self.day == self.week == 0:
            return
        first_omer_day = HebrewDate(month=Months.NISAN, day=16)
        last_omer_day = HebrewDate(month=Months.SIVAN, day=5)
        if self.date:
            if not first_omer_day <= self.date <= last_omer_day:
                self.total_days = 0
                self.day = 0
                self.week = 0
            else:
                first_omer_day.year = self.date.year
                self.total_days = (self.date - first_omer_day).days + 1
                self.week, self.day = divmod(self.total_days, 7)
        elif self.total_days > 0:
            self.date = first_omer_day + timedelta(days=self.total_days + 1)
            self.week, self.day = divmod(self.total_days, 7)
        else:
            self.total_days = self.week * 7 + self.day
            self.date = first_omer_day + timedelta(days=self.total_days + 1)

    def __str__(self) -> str:
        if self.total_days == 0:
            return ""
        if self.nusach == Nusach.ASHKENAZ:
            suffix = self.get_translation(f"in_omer_{self.nusach}")
        else:
            suffix = self.get_translation("in_omer")
        return f"{hebrew_number(self.total_days)} {suffix}"

    def count_str(self) -> str:
        """Return the text to be said when counting the omer."""
        if self.total_days == 0:
            return ""
        today = self.get_translation("today")
        _is = self.get_translation("is")
        total_days = hebrew_number(self.total_days, language=self.language)
        which_are = days = weeks = _and = ""
        if self.total_days > 1:
            which_are = self.get_translation("which_are")
            if self.day > 0:
                days = (
                    f"{hebrew_number(self.day, language=self.language)} "
                    f"{self.get_translation('days')}"
                )
                _and = self.get_translation("and")
            if self.week > 0:
                weeks = (
                    f"{hebrew_number(self.week, language=self.language)}"
                    f"{self.get_translation('weeks')}"
                )
        suffix = self.get_translation("in_omer")
        return f"{today} {_is} {total_days} {which_are} {days} {_and} {weeks} {suffix}"
