"""Daf Yomi module."""

import datetime as dt
from dataclasses import dataclass
from typing import ClassVar

from hdate.gematria import hebrew_number
from hdate.translator import TranslatorMixin


@dataclass(frozen=True)
class Masechta(TranslatorMixin):
    """Masechta object."""

    name: str
    pages: int

    def __str__(self) -> str:
        name = self.get_translation(self.name)
        daf = hebrew_number(self.pages, short=True)
        return f"{name} {daf}"


@dataclass
class DafYomiDatabase:
    """Database of Masechtos."""

    # The first few cycles were only 2702 blatt. After that it became 2711. Even with
    # that, the math doesn't play nicely with the dates before the 11th cycle :(
    # From cycle 11 onwards, it was simple and sequential
    _start_date: ClassVar[dt.date] = dt.date(1997, 9, 29)
    _masechtot: ClassVar[list[Masechta]]

    @classmethod
    def register(cls, masechtot: list[Masechta]) -> None:
        """Regisetr a list of masechtos."""
        cls._masechtot = masechtot

    @classmethod
    def cycle_length(cls) -> int:
        """Return the length of a full cycle."""
        return sum(masechta.pages for masechta in cls._masechtot)

    def lookup(self, date: dt.date) -> Masechta:
        """Return the start date of a full cycle."""
        days_since_start = (date - self._start_date).days
        page_number = days_since_start % self.cycle_length()

        masechta_index = 0
        for masechta in self._masechtot:
            if page_number < masechta.pages:
                break
            page_number -= masechta.pages
            masechta_index += 1

        return Masechta(self._masechtot[masechta_index].name, page_number + 2)


DAF_YOMI_MESECHTOS = (
    Masechta("berachos", 63),
    Masechta("shabbos", 156),
    Masechta("eruvin", 104),
    Masechta("pesachim", 120),
    Masechta("shekalim", 21),
    Masechta("yoma", 87),
    Masechta("succah", 55),
    Masechta("beitzah", 39),
    Masechta("rosh_hashanah", 34),
    Masechta("taanis", 30),
    Masechta("megillah", 31),
    Masechta("moed_katan", 28),
    Masechta("chagigah", 26),
    Masechta("yevamos", 121),
    Masechta("kesubos", 111),
    Masechta("nedarim", 90),
    Masechta("nazir", 65),
    Masechta("sotah", 48),
    Masechta("gittin", 89),
    Masechta("kiddushin", 81),
    Masechta("bava_kamma", 118),
    Masechta("bava_metzia", 118),
    Masechta("bava_basra", 175),
    Masechta("sanhedrin", 112),
    Masechta("makkos", 23),
    Masechta("shevuos", 48),
    Masechta("avodah_zarah", 75),
    Masechta("horayos", 13),
    Masechta("zevachim", 119),
    Masechta("menachos", 109),
    Masechta("chullin", 141),
    Masechta("bechoros", 60),
    Masechta("arachin", 33),
    Masechta("temurah", 33),
    Masechta("kereisos", 27),
    Masechta("meilah", 36),
    Masechta("niddah", 72),
)

DafYomiDatabase.register(list(DAF_YOMI_MESECHTOS))
