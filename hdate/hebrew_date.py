"""Pure Hebrew date class."""

from dataclasses import dataclass
from typing import Union

from hdate.htables import Months
from hdate.translator import TranslatorMixin


@dataclass
class HebrewDate(TranslatorMixin):
    """Define a Hebrew date object."""

    year: int
    month: Union[Months, int]
    day: int

    def __post_init__(self) -> None:
        if not 0 < date.day < 31:
            raise ValueError(f"day ({day}) legal values are 1-30")
        self.month = (
            self.month if isinstance(self.month, Months) else Months(self.month)
        )
