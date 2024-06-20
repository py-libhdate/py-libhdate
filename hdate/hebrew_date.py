"""Pure Hebrew date class."""

from dataclasses import dataclass

from hdate.htables import Months


@dataclass
class HebrewDate:
    """Define a Hebrew date object."""

    year: int
    month: Months
    day: int

    def __post_init__(self):
        self.month = (
            self.month if isinstance(self.month, Months) else Months(self.month)
        )
