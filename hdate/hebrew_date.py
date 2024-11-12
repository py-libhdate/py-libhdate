"""Pure Hebrew date class."""

from dataclasses import dataclass
from typing import Union

from hdate.htables import Months


@dataclass
class HebrewDate:
    """Define a Hebrew date object."""

    year: int
    month: Union[Months, int]
    day: int

    def __post_init__(self) -> None:
        self.month = (
            self.month if isinstance(self.month, Months) else Months(self.month)
        )
