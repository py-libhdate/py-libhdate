"""Constant lookup tables for hdate modules."""

import datetime
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Callable, TypeVar, Union

from hdate.translator import TranslatorMixin

HDateT = TypeVar("HDateT", bound="HDate")  # type: ignore # noqa: F821

READING = namedtuple("READING", "year_type, readings")

_READINGS = (
    READING(
        [1725],
        (
            0,
            53,
            0,
            range(29),
            0,
            range(29, 35),
            0,
            range(35, 39),
            59,
            41,
            60,
            range(44, 51),
            61,
        ),
    ),
    READING([1703], (0, 53, 0, range(29), 0, range(29, 42), 60, range(44, 51), 61)),
    READING([1523, 523], (53, 0, range(30), 0, range(30, 51), 61)),
    READING([1501, 501], (53, 0, range(30), 0, range(30, 52))),
    READING([1317, 1227], (52, 53, range(29), 0, 0, range(29, 42), 60, range(44, 52))),
    READING(
        [1205],
        (
            52,
            53,
            range(29),
            0,
            range(29, 35),
            0,
            range(35, 39),
            59,
            41,
            60,
            range(44, 51),
            61,
        ),
    ),
    READING(
        [521, 1521],
        (53, 0, range(26), 0, 26, 56, 57, 31, 58, range(34, 42), 60, range(44, 52)),
    ),
    READING(
        [1225, 1315],
        (
            52,
            53,
            range(22),
            55,
            24,
            25,
            0,
            26,
            56,
            57,
            31,
            58,
            34,
            0,
            range(35, 39),
            59,
            41,
            60,
            range(44, 51),
            61,
        ),
    ),
    READING(
        [1701],
        (
            0,
            53,
            0,
            range(22),
            55,
            24,
            25,
            0,
            26,
            56,
            57,
            31,
            58,
            range(34, 42),
            60,
            range(44, 52),
        ),
    ),
    READING(
        [1723],
        (
            0,
            53,
            0,
            range(22),
            55,
            24,
            25,
            0,
            26,
            56,
            57,
            31,
            58,
            range(34, 42),
            60,
            range(44, 51),
            61,
        ),
    ),
    READING(
        [1517],
        (
            53,
            0,
            range(22),
            55,
            24,
            25,
            0,
            0,
            26,
            56,
            57,
            31,
            58,
            range(34, 42),
            60,
            range(44, 52),
        ),
    ),
    READING(
        [703, 725],
        (0, 53, 0, 54, range(1, 29), 0, range(29, 42), 60, range(44, 51), 61),
    ),
    READING([317, 227], (52, 53, range(29), 0, range(29, 52))),
    READING([205], (52, 53, range(29), 0, range(29, 42), 60, range(44, 51), 61)),
    READING(
        [701],
        (
            0,
            53,
            0,
            54,
            range(1, 22),
            55,
            24,
            25,
            0,
            26,
            56,
            57,
            31,
            58,
            range(34, 42),
            60,
            range(44, 52),
        ),
    ),
    READING(
        [315, 203, 225, 1203],
        (
            52,
            53,
            range(22),
            55,
            24,
            25,
            0,
            26,
            56,
            57,
            31,
            58,
            range(34, 42),
            60,
            range(44, 51),
            61,
        ),
    ),
    READING(
        [723],
        (
            0,
            53,
            0,
            54,
            range(1, 22),
            55,
            24,
            25,
            0,
            26,
            56,
            57,
            31,
            58,
            range(34, 42),
            60,
            range(44, 51),
            61,
        ),
    ),
    READING(
        [517],
        (53, 0, range(22), 55, 24, 25, 0, 26, 56, 57, range(31, 42), 60, range(44, 52)),
    ),
)

READINGS = dict((year_type, r.readings) for r in _READINGS for year_type in r.year_type)

DIGITS = (
    (" ", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"),
    ("ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"),
    (" ", "ק", "ר", "ש", "ת"),
)

LANG = namedtuple("LANG", "french, english, hebrew")
DESC = namedtuple("DESC", "long, short")

DAYS = (
    LANG(DESC("Dimanche", "Dim"), DESC("Sunday", "Sun"), DESC("ראשון", "א")),
    LANG(DESC("Lundi", "Lun"), DESC("Monday", "Mon"), DESC("שני", "ב")),
    LANG(DESC("Mardi", "Mar"), DESC("Tuesday", "Tue"), DESC("שלישי", "ג")),
    LANG(DESC("Mercredi", "Mer"), DESC("Wednesday", "Wed"), DESC("רביעי", "ד")),
    LANG(DESC("Jeudi", "Jeu"), DESC("Thursday", "Thu"), DESC("חמישי", "ה")),
    LANG(DESC("Vendredi", "Ven"), DESC("Friday", "Fri"), DESC("שישי", "ו")),
    LANG(DESC("Samedi", "Sam"), DESC("Saturday", "Sat"), DESC("שבת", "ז")),
)

PARASHAOT = (
    LANG("none", "none", "none"),
    LANG("Bereshit", "Bereshit", "בראשית"),
    LANG("Noa'h", "Noach", "נח"),
    LANG("Lekh Lekha", "Lech-Lecha", "לך לך"),
    LANG("Vayera", "Vayera", "וירא"),
    LANG("Haye Sarah", "Chayei Sara", "חיי שרה"),
    LANG("Toledot", "Toldot", "תולדות"),
    LANG("Vayetze", "Vayetzei", "ויצא"),
    LANG("Vayishla'h", "Vayishlach", "וישלח"),
    LANG("Vayeshev", "Vayeshev", "וישב"),
    LANG("Miketz", "Miketz", "מקץ"),
    LANG("Vayigash", "Vayigash", "ויגש"),
    LANG("Vaye'hi", "Vayechi", "ויחי"),
    LANG("Shemot", "Shemot", "שמות"),
    LANG("Va'era", "Vaera", "וארא"),
    LANG("Bo", "Bo", "בא"),
    LANG("Beshalakh", "Beshalach", "בשלח"),
    LANG("Yitro", "Yitro", "יתרו"),
    LANG("Mishpatim", "Mishpatim", "משפטים"),
    LANG("Teroumah", "Terumah", "תרומה"),
    LANG("Tetzave", "Tetzaveh", "תצוה"),
    LANG("Ki Tissa", "Ki Tisa", "כי תשא"),
    LANG("Vayaqhel", "Vayakhel", "ויקהל"),
    LANG("Peqoudei", "Pekudei", "פקודי"),
    LANG("Vayikra", "Vayikra", "ויקרא"),
    LANG("Tzav", "Tzav", "צו"),
    LANG("Shemini", "Shmini", "שמיני"),
    LANG("Tazria", "Tazria", "תזריע"),
    LANG("Metzora", "Metzora", "מצורע"),
    LANG("A'harei Mot", "Achrei Mot", "אחרי מות"),
    LANG("Kedoshim", "Kedoshim", "קדושים"),
    LANG("Emor", "Emor", "אמור"),
    LANG("Behar", "Behar", "בהר"),
    LANG("Be'houkotai", "Bechukotai", "בחוקתי"),
    LANG("Bamidbar", "Bamidbar", "במדבר"),
    LANG("Nasso", "Nasso", "נשא"),
    LANG("Beha'alotkha", "Beha'alotcha", "בהעלתך"),
    LANG("Shla'h lekha", "Sh'lach", "שלח"),
    LANG("Kora'h", "Korach", "קרח"),
    LANG("Houkat", "Chukat", "חקת"),
    LANG("Balak", "Balak", "בלק"),
    LANG("Pin'has", "Pinchas", "פנחס"),
    LANG("Matot", "Matot", "מטות"),
    LANG("Massei", "Masei", "מסעי"),
    LANG("Devarim", "Devarim", "דברים"),
    LANG("Va'et'hanan", "Vaetchanan", "ואתחנן"),
    LANG("Eikev", "Eikev", "עקב"),
    LANG("Re'eh", "Re'eh", "ראה"),
    LANG("Shoftim", "Shoftim", "שופטים"),
    LANG("Ki Tetze", "Ki Teitzei", "כי תצא"),
    LANG("Ki Tavo", "Ki Tavo", "כי תבוא"),
    LANG("Nitzavim", "Nitzavim", "נצבים"),
    LANG("Vayelekh", "Vayeilech", "וילך"),
    LANG("Haazinou", "Ha'Azinu", "האזינו"),
    LANG("Vezot Haberakha", "Vezot Habracha", "וזאת הברכה"),
    LANG("Vayaqhel-Peqoudei", "Vayakhel-Pekudei", "ויקהל-פקודי"),
    LANG("Tazria-Metzora", "Tazria-Metzora", "תזריע-מצורע"),
    LANG("A'harei Mot-Kedoshim", "Achrei Mot-Kedoshim", "אחרי מות-קדושים"),
    LANG("Behar-Be'houkotai", "Behar-Bechukotai", "בהר-בחוקתי"),
    LANG("Houkat-Balak", "Chukat-Balak", "חוקת-בלק"),
    LANG("Matot-Massei", "Matot-Masei", "מטות מסעי"),
    LANG("Nitzavim-Vayelekh", "Nitzavim-Vayeilech", "נצבים-וילך"),
)


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

    def __str__(self) -> str:
        return self.get_translation(self.name)


def year_is_after(year: int) -> Callable[[HDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is after the
    requested year.
    """
    return lambda x: x.hdate.year > year


def year_is_before(year: int) -> Callable[[HDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is before the
    requested year.
    """
    return lambda x: x.hdate.year < year


def move_if_not_on_dow(
    original: int, replacement: int, dow_not_orig: int, dow_replacement: int
) -> Callable[[HDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that either the original day does not fall on a given
    weekday, or that the replacement day does fall on the expected weekday.
    """
    return lambda x: (
        (x.hdate.day == original and x.gdate.weekday() != dow_not_orig)
        or (x.hdate.day == replacement and x.gdate.weekday() == dow_replacement)
    )


def correct_adar() -> Callable[[HDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that the value of the month returned is correct depending on whether
    it's a leap year.
    """
    return lambda x: (
        (x.hdate.month not in [Months.ADAR, Months.ADAR_I, Months.ADAR_II])
        or (x.hdate.month == Months.ADAR and not x.is_leap_year)
        or (x.hdate.month in [Months.ADAR_I, Months.ADAR_II] and x.is_leap_year)
    )


def not_rosh_chodesh() -> Callable[[HDateT], bool]:
    """The 1st of Tishrei is not Rosh Chodesh."""
    return lambda x: not (x.hdate.month == Months.TISHREI and x.hdate.day == 1)


def legal_month_length() -> Callable[[HDateT], bool]:
    """
    Return a lambda function.

    Lambda checks that the length for the provided month is legal
    """
    return lambda x: (
        x.hdate.day == 29  # 29 is always legal
        or x.hdate.day == 30
        and x.hdate.month
        in [
            Months.TISHREI,
            Months.SHVAT,
            Months.ADAR_I,
            Months.NISAN,
            Months.SIVAN,
            Months.AV,
        ]
        or x.hdate.day == 30
        and x.long_cheshvan()
        and x.hdate.month == Months.MARCHESHVAN
        or x.hdate.day == 30
        and not x.short_kislev()
        and x.hdate.month == Months.KISLEV
    )


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
    date: Union[tuple[Union[int, list[int]], Union[Months, list[Months]]], tuple[()]]
    israel_diaspora: str
    date_functions_list: list[Callable[[HDateT], bool]]

    def __str__(self) -> str:
        return self.get_translation(self.name)


HOLIDAYS = (
    Holiday(HolidayTypes.NONE, "", (), "", []),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_rosh_hashana", (29, Months.ELUL), "", []),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_i", (1, Months.TISHREI), "", []),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_ii", (2, Months.TISHREI), "", []),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        ([3, 4], Months.TISHREI),
        "",
        [move_if_not_on_dow(3, 4, 5, 6)],
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
        ([17, 18, 19, 20], Months.TISHREI),
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
        (list(range(25, 31)), Months.KISLEV),
        "",
        [],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        ([1, 2, 3], Months.TEVET),
        "",
        [
            lambda x: (
                (x.short_kislev() and x.hdate.day == 3) or (x.hdate.day in [1, 2])
            )
        ],
    ),
    Holiday(HolidayTypes.FAST_DAY, "asara_btevet", (10, Months.TEVET), "", []),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bshvat", (15, Months.SHVAT), "", []),
    Holiday(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ([11, 13], [Months.ADAR, Months.ADAR_II]),
        "",
        [move_if_not_on_dow(13, 11, 5, 3), correct_adar()],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        (14, [Months.ADAR, Months.ADAR_II]),
        "",
        [correct_adar()],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        (15, [Months.ADAR, Months.ADAR_II]),
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
        ([17, 18, 19], Months.NISAN),
        "",
        [],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "hol_hamoed_pesach", (20, Months.NISAN), "", []),
    Holiday(HolidayTypes.YOM_TOV, "pesach_vii", (21, Months.NISAN), "", []),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ([3, 4, 5], Months.IYYAR),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(5, 4, 4, 3)  # type: ignore
            or move_if_not_on_dow(5, 3, 5, 3),
        ],
    ),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ([3, 4, 5, 6], Months.IYYAR),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(5, 4, 4, 3)  # type: ignore
            or move_if_not_on_dow(5, 3, 5, 3)
            or move_if_not_on_dow(5, 6, 0, 1),
        ],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "lag_bomer", (18, Months.IYYAR), "", []),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_shavuot", (5, Months.SIVAN), "", []),
    Holiday(HolidayTypes.YOM_TOV, "shavuot", (6, Months.SIVAN), "", []),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        ([17, 18], Months.TAMMUZ),
        "",
        [move_if_not_on_dow(17, 18, 5, 6)],
    ),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        ([9, 10], Months.AV),
        "",
        [move_if_not_on_dow(9, 10, 5, 6)],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bav", (15, Months.AV), "", []),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hashoah",
        ([26, 27, 28], Months.NISAN),
        "",
        [
            move_if_not_on_dow(27, 28, 6, 0)  # type: ignore
            or move_if_not_on_dow(27, 26, 4, 3),
            year_is_after(5718),
        ],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ([2, 3, 4], Months.IYYAR),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(4, 3, 3, 2)  # type: ignore
            or move_if_not_on_dow(4, 2, 4, 2),
        ],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ([2, 3, 4, 5], Months.IYYAR),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(4, 3, 3, 2)  # type: ignore
            or move_if_not_on_dow(4, 2, 4, 2)
            or move_if_not_on_dow(4, 5, 6, 0),
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
        (7, [Months.ADAR, Months.ADAR_II]),
        "ISRAEL",
        [correct_adar()],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        ([11, 12], Months.MARCHESHVAN),
        "ISRAEL",
        [move_if_not_on_dow(12, 11, 4, 3), year_is_after(5757)],
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
        ([1, 30], list(Months)),
        "",
        [correct_adar(), legal_month_length(), not_rosh_chodesh()],
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


ZMAN = namedtuple("ZMAN", "zman, description")
ZMANIM = (
    ZMAN("first_light", LANG("Alot HaShahar", "Alot HaShachar", "עלות השחר")),
    ZMAN(
        "talit",
        LANG("Début Talit & Tefilin ", "Talit & Tefilin's time", "זמן טלית ותפילין"),
    ),
    ZMAN("sunrise", LANG("Lever du jour", "Sunrise", "הנץ החמה")),
    ZMAN("mga_end_shma", LANG('Shema MG"A', 'Shema EOT MG"A', 'סוף זמן ק"ש מג"א')),
    ZMAN("gra_end_shma", LANG('Shema GR"A', 'Shema EOT GR"A', 'סוף זמן ק"ש גר"א')),
    ZMAN("mga_end_tfila", LANG('Tefila MG"A', 'Tefila EOT MG"A', 'סוף זמן תפילה מג"א')),
    ZMAN("gra_end_tfila", LANG('Tefila GR"A', 'Tefila EOT GR"A', 'סוף זמן תפילה גר"א')),
    ZMAN("midday", LANG("Hatsot", "Midday", "חצות היום")),
    ZMAN("big_mincha", LANG("Minha Guedola", "Big Mincha", "מנחה גדולה")),
    ZMAN(
        "big_mincha_30",
        LANG("Minha Guedola 30 min", "Big Mincha 30 min", "מנחה גדולה 30 דק"),
    ),
    ZMAN("small_mincha", LANG("Minha Qetana", "Small Mincha", "מנחה קטנה")),
    ZMAN("plag_mincha", LANG("Plag haMinha", "Plag Mincha", "פלג המנחה")),
    ZMAN("sunset", LANG("Shqiat", "Sunset", "שקיעה")),
    ZMAN("first_stars", LANG("Tzeit haCokhavim", "First stars", "צאת הכוכבים")),
    ZMAN(
        "rabbeinu_tam",
        LANG("Nuit selon Rabbénou Tam", "Night by Rabbeinu Tam", "לילה לרבנו תם"),
    ),
    ZMAN("midnight", LANG("Hatsot laïla", "Midnight", "חצות הלילה")),
)

# The first few cycles were only 2702 blatt. After that it became 2711. Even with
# that, the math doesn't play nicely with the dates before the 11th cycle :(
# From cycle 11 onwards, it was simple and sequential
DAF_YOMI_CYCLE_11_START = datetime.date(1997, 9, 29)


@dataclass
class Masechta(TranslatorMixin):
    """Masechta object."""

    name: str
    pages: int

    def __str__(self) -> str:
        return self.get_translation(self.name)


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

TRADITION = namedtuple(
    "TRADITION", ["israel", "diaspora_ashkenazi", "diaspora_sephardi"]
)

PRAYER_DESCRIPTIONS = {
    "prev_pessah_to_shemini": TRADITION(
        LANG(
            "Moride ha-tal - barkhénou",
            "Morid ha-tal - Barkheinu",
            "מוֹרִיד הַטַּל - בָּרְכֵנוּ",
        ),
        LANG(
            "(Silence) - barkhénou",
            "(Silence) - Barkheinu",
            "(שתיקה) - בָּרְכֵנוּ",
        ),
        LANG(
            "Moride ha-tal - barkhénou",
            "Morid ha-tal - Barkheinu",
            "מוֹרִיד הַטַּל - בָּרְכֵנוּ",
        ),
    ),
    "shemini_to_cheshvan": TRADITION(
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barkheinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ",
        ),
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barkheinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ",
        ),
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barkheinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ",
        ),
    ),
    "cheshvan_to_geshamim": TRADITION(
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barech aleinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ",
        ),
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barkheinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ",
        ),
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barkheinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ",
        ),
    ),
    "geshamim_to_pessah": TRADITION(
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barech aleinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ",
        ),
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barech aleinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ",
        ),
        LANG(
            "Machiv ha-roua'h oumoride ha-guéchem - barkhénou",
            "Mashiv ha-ruach u-morid ha-geshem - Barech aleinu",
            "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ",
        ),
    ),
    "pessah_to_shemini_next": TRADITION(
        LANG(
            "Moride ha-tal - barkhénou",
            "Morid ha-tal - Barkheinu",
            "מוֹרִיד הַטַּל - בָּרְכֵנוּ",
        ),
        LANG(
            "(Silence) - barkhénou",
            "(Silence) - Barkheinu",
            "(שתיקה) - בָּרְכֵנוּ",
        ),
        LANG(
            "Moride ha-tal - barkhénou",
            "Morid ha-tal - Barkheinu",
            "מוֹרִיד הַטַּל - בָּרְכֵנוּ",
        ),
    ),
}
