"""Pure Hebrew date class."""

from dataclasses import dataclass
from typing import Union

from hdate.htables import Months
from hdate.translator import TranslatorMixin


@dataclass
class HebrewDate(TranslatorMixin):
    """Define a Hebrew date object."""

    year: int = 0
    month: Union[Months, int] = Months.TISHREI
    day: int = 1

    def __post_init__(self) -> None:
        if not 0 < self.day < 31:
            raise ValueError(f"day ({self.day}) legal values are 1-30")
        self.month = (
            self.month if isinstance(self.month, Months) else Months(self.month)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HebrewDate):
            return NotImplemented
        if self.year == 0 or other.year == 0:
            return (self.month, self.day) == (other.month, other.day)
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, HebrewDate):
            return NotImplemented
        if self.year == 0 or other.year == 0:
            return (self.month, self.day) < (other.month, other.day)
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)
