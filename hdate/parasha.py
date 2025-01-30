"""Constant lookup tables for hdate modules."""

import datetime as dt
from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import ClassVar, cast

from hdate.hebrew_date import HebrewDate, Months, Weekday
from hdate.translator import TranslatorMixin


def erange(start: Enum, end: Enum) -> list[Enum]:
    """Return a range of Enums between `start` and `end`, exclusive."""
    if start.__class__ != end.__class__:
        raise TypeError(
            f"The `erange` method can only operate on the same enum types. "
            f"Start type: {start.__class__.__name__}, "
            f"End type: {end.__class__.__name__}"
        )
    enum_list = list(start.__class__)
    start_idx = enum_list.index(start)
    end_idx = enum_list.index(end) + 1
    return enum_list[start_idx:end_idx]


class Parasha(TranslatorMixin, IntEnum):
    """Parasha enum."""

    NONE = 0
    BERESHIT = auto()
    NOACH = auto()
    LECH_LECHA = auto()
    VAYERA = auto()
    CHAYEI_SARA = auto()
    TOLDOT = auto()
    VAYETZEI = auto()
    VAYISHLACH = auto()
    VAYESHEV = auto()
    MIKETZ = auto()
    VAYIGASH = auto()
    VAYECHI = auto()
    SHEMOT = auto()
    VAERA = auto()
    BO = auto()
    BESHALACH = auto()
    YITRO = auto()
    MISHPATIM = auto()
    TERUMAH = auto()
    TETZAVEH = auto()
    KI_TISA = auto()
    VAYAKHEL = auto()
    PEKUDEI = auto()
    VAYIKRA = auto()
    TZAV = auto()
    SHMINI = auto()
    TAZRIA = auto()
    METZORA = auto()
    ACHREI_MOT = auto()
    KEDOSHIM = auto()
    EMOR = auto()
    BEHAR = auto()
    BECHUKOTAI = auto()
    BAMIDBAR = auto()
    NASSO = auto()
    BEHAALOTCHA = auto()
    SHLACH = auto()
    KORACH = auto()
    CHUKAT = auto()
    BALAK = auto()
    PINCHAS = auto()
    MATOT = auto()
    MASEI = auto()
    DEVARIM = auto()
    VAETCHANAN = auto()
    EIKEV = auto()
    REEH = auto()
    SHOFTIM = auto()
    KI_TEITZEI = auto()
    KI_TAVO = auto()
    NITZAVIM = auto()
    VAYEILECH = auto()
    HAAZINU = auto()
    VEZOT_HABRACHA = auto()
    VAYAKHEL_PEKUDEI = auto()
    TAZRIA_METZORA = auto()
    ACHREI_MOT_KEDOSHIM = auto()
    BEHAR_BECHUKOTAI = auto()
    CHUKAT_BALAK = auto()
    MATOT_MASEI = auto()
    NITZAVIM_VAYEILECH = auto()


@dataclass
class ParashaDatabase:
    """Container class for parasha information."""

    diaspora: bool

    _all_parashas: ClassVar[dict[tuple[int, ...], tuple[Enum, ...]]]

    @classmethod
    def register(cls, parashas: dict[tuple[int, ...], tuple[Enum, ...]]) -> None:
        """Register the different parasha sequences."""
        cls._all_parashas = parashas

    def lookup(self, date: HebrewDate) -> Parasha:
        """Lookup the parasha for a given date."""
        _year_type = (date.year_size(date.year) % 10) - 3
        rosh_hashana = HebrewDate(date.year, Months.TISHREI, 1)
        pesach = HebrewDate(date.year, Months.NISAN, 15)
        year_type = (
            self.diaspora * 1000
            + rosh_hashana.dow() * 100
            + _year_type * 10
            + pesach.dow()
        )

        # Number of days since rosh hashana
        days = (date - rosh_hashana).days
        # Number of weeks since rosh hashana
        weeks = (days + rosh_hashana.dow() - 1) // 7

        # If it's currently Simchat Torah, return VeZot Haberacha.
        if weeks == 3:
            if (
                days <= 22
                and self.diaspora
                and date.dow() != Weekday.SATURDAY
                or days <= 21
                and not self.diaspora
            ):
                return Parasha.VEZOT_HABRACHA

        # Special case for Simchat Torah in diaspora.
        if weeks == 4 and days == 22 and self.diaspora:
            return Parasha.VEZOT_HABRACHA

        readings = next(
            seq for types, seq in self._all_parashas.items() if year_type in types
        )
        # Maybe recompute the year type based on the upcoming shabbat.
        # This avoids an edge case where today is before Rosh Hashana but
        # Shabbat is in a new year afterwards.
        if (
            weeks >= len(readings)
            and date.year
            < (
                next_shabbat := (
                    date + dt.timedelta(days=Weekday.SATURDAY - date.dow())
                )
            ).year
        ):
            return self.lookup(next_shabbat)
        return cast(Parasha, readings[weeks])


PARASHA_SEQUENCES: dict[tuple[int, ...], tuple[Enum, ...]] = {
    (1725,): (
        Parasha.NONE,
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.METZORA),
        Parasha.NONE,
        *erange(Parasha.ACHREI_MOT, Parasha.BAMIDBAR),
        Parasha.NONE,
        *erange(Parasha.NASSO, Parasha.KORACH),
        Parasha.CHUKAT_BALAK,
        Parasha.PINCHAS,
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (1703,): (
        Parasha.NONE,
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.METZORA),
        Parasha.NONE,
        *erange(Parasha.ACHREI_MOT, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (1523, 523): (
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.ACHREI_MOT),
        Parasha.NONE,
        *erange(Parasha.KEDOSHIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (1501, 501): (
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.ACHREI_MOT),
        Parasha.NONE,
        *erange(Parasha.KEDOSHIM, Parasha.NITZAVIM),
    ),
    (1317, 1227): (
        Parasha.VAYEILECH,
        Parasha.HAAZINU,
        *erange(Parasha.NONE, Parasha.METZORA),
        Parasha.NONE,
        Parasha.NONE,
        *erange(Parasha.ACHREI_MOT, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.NITZAVIM),
    ),
    (1205,): (
        Parasha.VAYEILECH,
        Parasha.HAAZINU,
        *erange(Parasha.NONE, Parasha.METZORA),
        Parasha.NONE,
        *erange(Parasha.ACHREI_MOT, Parasha.BAMIDBAR),
        Parasha.NONE,
        *erange(Parasha.NASSO, Parasha.KORACH),
        Parasha.CHUKAT_BALAK,
        Parasha.PINCHAS,
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (521, 1521): (
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.TZAV),
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        *erange(Parasha.BAMIDBAR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.NITZAVIM),
    ),
    (1225, 1315): (
        Parasha.VAYEILECH,
        Parasha.HAAZINU,
        *erange(Parasha.NONE, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        Parasha.BAMIDBAR,
        Parasha.NONE,
        *erange(Parasha.NASSO, Parasha.KORACH),
        Parasha.CHUKAT_BALAK,
        Parasha.PINCHAS,
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (1701,): (
        Parasha.NONE,
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        *erange(Parasha.BAMIDBAR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.NITZAVIM),
    ),
    (1723,): (
        Parasha.NONE,
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        *erange(Parasha.BAMIDBAR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (1517,): (
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        *erange(Parasha.BAMIDBAR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.NITZAVIM),
    ),
    (703, 725): (
        Parasha.NONE,
        Parasha.HAAZINU,
        Parasha.NONE,
        Parasha.VEZOT_HABRACHA,
        *erange(Parasha.BERESHIT, Parasha.METZORA),
        Parasha.NONE,
        *erange(Parasha.ACHREI_MOT, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (317, 227): (
        Parasha.VAYEILECH,
        Parasha.HAAZINU,
        *erange(Parasha.NONE, Parasha.METZORA),
        Parasha.NONE,
        *erange(Parasha.ACHREI_MOT, Parasha.NITZAVIM),
    ),
    (205,): (
        Parasha.VAYEILECH,
        Parasha.HAAZINU,
        *erange(Parasha.NONE, Parasha.METZORA),
        Parasha.NONE,
        *erange(Parasha.ACHREI_MOT, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (701,): (
        Parasha.NONE,
        Parasha.HAAZINU,
        Parasha.NONE,
        Parasha.VEZOT_HABRACHA,
        *erange(Parasha.BERESHIT, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        *erange(Parasha.BAMIDBAR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.NITZAVIM),
    ),
    (315, 203, 225, 1203): (
        Parasha.VAYEILECH,
        Parasha.HAAZINU,
        *erange(Parasha.NONE, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        *erange(Parasha.BAMIDBAR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (723,): (
        Parasha.NONE,
        Parasha.HAAZINU,
        Parasha.NONE,
        Parasha.VEZOT_HABRACHA,
        *erange(Parasha.BERESHIT, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        Parasha.EMOR,
        Parasha.BEHAR_BECHUKOTAI,
        *erange(Parasha.BAMIDBAR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.KI_TAVO),
        Parasha.NITZAVIM_VAYEILECH,
    ),
    (517,): (
        Parasha.HAAZINU,
        Parasha.NONE,
        *erange(Parasha.NONE, Parasha.KI_TISA),
        Parasha.VAYAKHEL_PEKUDEI,
        Parasha.VAYIKRA,
        Parasha.TZAV,
        Parasha.NONE,
        Parasha.SHMINI,
        Parasha.TAZRIA_METZORA,
        Parasha.ACHREI_MOT_KEDOSHIM,
        *erange(Parasha.EMOR, Parasha.PINCHAS),
        Parasha.MATOT_MASEI,
        *erange(Parasha.DEVARIM, Parasha.NITZAVIM),
    ),
}

ParashaDatabase.register(PARASHA_SEQUENCES)
