"""Constant lookup tables for hdate modules."""

import datetime as dt
from dataclasses import dataclass
from enum import Enum, IntEnum, auto

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


# The first few cycles were only 2702 blatt. After that it became 2711. Even with
# that, the math doesn't play nicely with the dates before the 11th cycle :(
# From cycle 11 onwards, it was simple and sequential
DAF_YOMI_CYCLE_11_START = dt.date(1997, 9, 29)


@dataclass
class Masechta(TranslatorMixin):
    """Masechta object."""

    name: str
    pages: int


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

DAF_YOMI_TOTAL_PAGES = sum(mesechta.pages for mesechta in DAF_YOMI_MESECHTOS)
