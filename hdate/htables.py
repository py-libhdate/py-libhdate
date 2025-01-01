"""Constant lookup tables for hdate modules."""

import datetime as dt
from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import Callable, TypeVar, Union

from hdate.translator import TranslatorMixin

HebrewDateT = TypeVar("HebrewDateT", bound="HebrewDate")  # type: ignore # noqa: F821


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


class Days(TranslatorMixin, IntEnum):
    """Enum class for the days of the week."""

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7


class Months(TranslatorMixin, IntEnum):
    """Enum class for the Hebrew months."""

    TISHREI = 1
    MARCHESHVAN = 2
    KISLEV = 3
    TEVET = 4
    SHVAT = 5
    ADAR = 6
    NISAN = 7
    IYYAR = 8
    SIVAN = 9
    TAMMUZ = 10
    AV = 11
    ELUL = 12
    ADAR_I = 13
    ADAR_II = 14


LONG_MONTHS = (
    Months.TISHREI,
    Months.SHVAT,
    Months.ADAR_I,
    Months.NISAN,
    Months.SIVAN,
    Months.AV,
)
SHORT_MONTHS = (
    Months.TEVET,
    Months.ADAR,
    Months.ADAR_II,
    Months.IYYAR,
    Months.TAMMUZ,
    Months.ELUL,
)
CHANGING_MONTHS = (Months.MARCHESHVAN, Months.KISLEV)


def year_is_after(year: int) -> Callable[[HebrewDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is after the
    requested year.
    """
    return lambda x: x.year > year


def year_is_before(year: int) -> Callable[[HebrewDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is before the
    requested year.
    """
    return lambda x: x.year < year


def move_if_not_on_dow(
    original: int, replacement: int, dow_not_orig: Days, dow_replacement: Days
) -> Callable[[HebrewDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that either the original day does not fall on a given
    weekday, or that the replacement day does fall on the expected weekday.
    """
    return lambda x: (
        (x.day == original and x.dow() != dow_not_orig)
        or (x.day == replacement and x.dow() == dow_replacement)
    )


def correct_adar() -> Callable[[HebrewDateT], Union[bool, Callable[[], bool]]]:
    """
    Return a lambda function.

    Lambda checks that the value of the month returned is correct depending on whether
    it's a leap year.
    """
    return lambda x: (
        (x.month not in [Months.ADAR, Months.ADAR_I, Months.ADAR_II])
        or (x.month == Months.ADAR and not x.is_leap_year())
        or (x.month in (Months.ADAR_I, Months.ADAR_II) and x.is_leap_year())
    )


def not_rosh_chodesh() -> Callable[[HebrewDateT], bool]:
    """The 1st of Tishrei is not Rosh Chodesh."""
    return lambda x: not (x.month == Months.TISHREI and x.day == 1)


class HolidayTypes(Enum):
    """Container class for holiday type integer mappings."""

    NONE = 0
    YOM_TOV = 1
    EREV_YOM_TOV = 2
    HOL_HAMOED = 3
    MELACHA_PERMITTED_HOLIDAY = 4
    FAST_DAY = 5
    MODERN_HOLIDAY = 6
    MINOR_HOLIDAY = 7
    MEMORIAL_DAY = 8
    ISRAEL_NATIONAL_HOLIDAY = 9
    ROSH_CHODESH = 10


@dataclass
class Holiday(TranslatorMixin):
    """Container class for holiday information."""

    type: HolidayTypes
    name: str
    date: Union[
        tuple[Union[int, tuple[int, ...]], Union[Months, tuple[Months, ...]]], tuple[()]
    ]
    israel_diaspora: str
    date_functions_list: list[Callable[[HebrewDateT], Union[bool, Callable[[], bool]]]]


HOLIDAYS = (
    Holiday(HolidayTypes.NONE, "", (), "", []),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_rosh_hashana", (29, Months.ELUL), "", []),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_i", (1, Months.TISHREI), "", []),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_ii", (2, Months.TISHREI), "", []),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        ((3, 4), Months.TISHREI),
        "",
        [move_if_not_on_dow(3, 4, Days.SATURDAY, Days.SUNDAY)],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_yom_kippur", (9, Months.TISHREI), "", []),
    Holiday(HolidayTypes.YOM_TOV, "yom_kippur", (10, Months.TISHREI), "", []),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_sukkot", (14, Months.TISHREI), "", []),
    Holiday(HolidayTypes.YOM_TOV, "sukkot", (15, Months.TISHREI), "", []),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_sukkot", (16, Months.TISHREI), "ISRAEL", []
    ),
    Holiday(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        ((17, 18, 19, 20), Months.TISHREI),
        "",
        [],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "hoshana_raba", (21, Months.TISHREI), "", []),
    Holiday(
        HolidayTypes.YOM_TOV, "simchat_torah", (23, Months.TISHREI), "DIASPORA", []
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        ((25, 26, 27, 28, 29, 30), Months.KISLEV),
        "",
        [],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        ((1, 2, 3), Months.TEVET),
        "",
        [lambda x: ((x.short_kislev() and x.day == 3) or (x.day in [1, 2]))],
    ),
    Holiday(HolidayTypes.FAST_DAY, "asara_btevet", (10, Months.TEVET), "", []),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bshvat", (15, Months.SHVAT), "", []),
    Holiday(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ((11, 13), (Months.ADAR, Months.ADAR_II)),
        "",
        [move_if_not_on_dow(13, 11, Days.SATURDAY, Days.THURSDAY), correct_adar()],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        (14, (Months.ADAR, Months.ADAR_II)),
        "",
        [correct_adar()],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        (15, (Months.ADAR, Months.ADAR_II)),
        "",
        [correct_adar()],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_pesach", (14, Months.NISAN), "", []),
    Holiday(HolidayTypes.YOM_TOV, "pesach", (15, Months.NISAN), "", []),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_pesach", (16, Months.NISAN), "ISRAEL", []
    ),
    Holiday(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        ((17, 18, 19), Months.NISAN),
        "",
        [],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "hol_hamoed_pesach", (20, Months.NISAN), "", []),
    Holiday(HolidayTypes.YOM_TOV, "pesach_vii", (21, Months.NISAN), "", []),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ((3, 4, 5), Months.IYYAR),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(5, 4, Days.FRIDAY, Days.THURSDAY)  # type: ignore
            or move_if_not_on_dow(5, 3, Days.SATURDAY, Days.THURSDAY),
        ],
    ),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ((3, 4, 5, 6), Months.IYYAR),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(5, 4, Days.FRIDAY, Days.THURSDAY)  # type: ignore
            or move_if_not_on_dow(5, 3, Days.SATURDAY, Days.THURSDAY)
            or move_if_not_on_dow(5, 6, Days.MONDAY, Days.TUESDAY),
        ],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "lag_bomer", (18, Months.IYYAR), "", []),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_shavuot", (5, Months.SIVAN), "", []),
    Holiday(HolidayTypes.YOM_TOV, "shavuot", (6, Months.SIVAN), "", []),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        ((17, 18), Months.TAMMUZ),
        "",
        [move_if_not_on_dow(17, 18, Days.SATURDAY, Days.SUNDAY)],
    ),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        ((9, 10), Months.AV),
        "",
        [move_if_not_on_dow(9, 10, Days.SATURDAY, Days.SUNDAY)],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bav", (15, Months.AV), "", []),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hashoah",
        ((26, 27, 28), Months.NISAN),
        "",
        [
            move_if_not_on_dow(27, 28, Days.SUNDAY, Days.MONDAY)  # type: ignore
            or move_if_not_on_dow(27, 26, Days.FRIDAY, Days.THURSDAY),
            year_is_after(5718),
        ],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ((2, 3, 4), Months.IYYAR),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(4, 3, Days.THURSDAY, Days.TUESDAY)  # type: ignore
            or move_if_not_on_dow(4, 2, Days.FRIDAY, Days.WEDNESDAY),
        ],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ((2, 3, 4, 5), Months.IYYAR),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(4, 3, Days.THURSDAY, Days.WEDNESDAY)  # type: ignore
            or move_if_not_on_dow(4, 2, Days.FRIDAY, Days.WEDNESDAY)
            or move_if_not_on_dow(4, 5, Days.SUNDAY, Days.MONDAY),
        ],
    ),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_yerushalayim",
        (28, Months.IYYAR),
        "",
        [year_is_after(5727)],
    ),
    Holiday(HolidayTypes.YOM_TOV, "shmini_atzeret", (22, Months.TISHREI), "", []),
    Holiday(HolidayTypes.YOM_TOV, "pesach_viii", (22, Months.NISAN), "DIASPORA", []),
    Holiday(HolidayTypes.YOM_TOV, "shavuot_ii", (7, Months.SIVAN), "DIASPORA", []),
    Holiday(HolidayTypes.YOM_TOV, "sukkot_ii", (16, Months.TISHREI), "DIASPORA", []),
    Holiday(HolidayTypes.YOM_TOV, "pesach_ii", (16, Months.NISAN), "DIASPORA", []),
    Holiday(
        HolidayTypes.ISRAEL_NATIONAL_HOLIDAY,
        "family_day",
        (30, Months.SHVAT),
        "ISRAEL",
        [year_is_after(5734)],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "memorial_day_unknown",
        (7, (Months.ADAR, Months.ADAR_II)),
        "ISRAEL",
        [correct_adar()],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        ((11, 12), Months.MARCHESHVAN),
        "ISRAEL",
        [move_if_not_on_dow(12, 11, Days.FRIDAY, Days.THURSDAY), year_is_after(5757)],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "zeev_zhabotinsky_day",
        (29, Months.TAMMUZ),
        "ISRAEL",
        [year_is_after(5764)],
    ),
    Holiday(
        HolidayTypes.ROSH_CHODESH,
        "rosh_chodesh",
        (1, tuple(Months)),
        "",
        [correct_adar(), not_rosh_chodesh()],
    ),
    Holiday(
        HolidayTypes.ROSH_CHODESH,
        "rosh_chodesh",
        (30, LONG_MONTHS + CHANGING_MONTHS),
        "",
        [correct_adar()],
    ),
)


def get_all_holidays(language: str) -> list[str]:
    """Helper method to get all the holiday descriptions in the specified language."""

    def holiday_name(holiday: Holiday, language: str) -> str:
        holiday.set_language(language)
        return str(holiday.name)

    doubles = {
        "french": "Rosh Hodesh, Hanoukka",
        "hebrew": "ראש חודש, חנוכה",
        "english": "Rosh Chodesh, Chanukah",
    }
    holidays_list = [holiday_name(h, language) for h in HOLIDAYS] + [
        doubles.get(language, doubles["english"])
    ]

    return holidays_list


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
