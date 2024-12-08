"""Constant lookup tables for hdate modules."""

import datetime
from collections import namedtuple
from enum import Enum
from typing import Callable, TypeVar

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

MONTHS = (
    LANG("Tishri", "Tishrei", "תשרי"),
    LANG("Heshvan", "Marcheshvan", "מרחשוון"),
    LANG("Kislev", "Kislev", "כסלו"),
    LANG("Tevet", "Tevet", "טבת"),
    LANG("Shvat", "Sh'vat", "שבט"),
    LANG("Adar", "Adar", "אדר"),
    LANG("Nissan", "Nisan", "ניסן"),
    LANG("Iyar", "Iyyar", "אייר"),
    LANG("Sivan", "Sivan", "סיון"),
    LANG("Tamouz", "Tammuz", "תמוז"),
    LANG("Av", "Av", "אב"),
    LANG("Eloul", "Elul", "אלול"),
    LANG("Adar I", "Adar I", "אדר א"),
    LANG("Adar II", "Adar II", "אדר ב"),
)


class Months(Enum):
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


HOLIDAY = namedtuple(
    "HOLIDAY",
    ["type", "name", "date", "israel_diaspora", "date_functions_list"],
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


HOLIDAYS = (
    HOLIDAY(HolidayTypes.NONE, "", (), "", []),
    HOLIDAY(HolidayTypes.EREV_YOM_TOV, "erev_rosh_hashana", (29, Months.ELUL), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "rosh_hashana_i", (1, Months.TISHREI), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "rosh_hashana_ii", (2, Months.TISHREI), "", []),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        ([3, 4], Months.TISHREI),
        "",
        [move_if_not_on_dow(3, 4, 5, 6)],
    ),
    HOLIDAY(HolidayTypes.EREV_YOM_TOV, "erev_yom_kippur", (9, Months.TISHREI), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "yom_kippur", (10, Months.TISHREI), "", []),
    HOLIDAY(HolidayTypes.EREV_YOM_TOV, "erev_sukkot", (14, Months.TISHREI), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "sukkot", (15, Months.TISHREI), "", []),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_sukkot", (16, Months.TISHREI), "ISRAEL", ""
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        ([17, 18, 19, 20], Months.TISHREI),
        "",
        "",
    ),
    HOLIDAY(HolidayTypes.EREV_YOM_TOV, "hoshana_raba", (21, Months.TISHREI), "", []),
    HOLIDAY(
        HolidayTypes.YOM_TOV, "simchat_torah", (23, Months.TISHREI), "DIASPORA", []
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        (list(range(25, 31)), Months.KISLEV),
        "",
        [],
    ),
    HOLIDAY(
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
    HOLIDAY(HolidayTypes.FAST_DAY, "asara_btevet", (10, Months.TEVET), "", []),
    HOLIDAY(HolidayTypes.MINOR_HOLIDAY, "tu_bshvat", (15, Months.SHVAT), "", []),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ([11, 13], [Months.ADAR, Months.ADAR_II]),
        "",
        [move_if_not_on_dow(13, 11, 5, 3), correct_adar()],
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        (14, [Months.ADAR, Months.ADAR_II]),
        "",
        [correct_adar()],
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        (15, [Months.ADAR, Months.ADAR_II]),
        "",
        [correct_adar()],
    ),
    HOLIDAY(HolidayTypes.EREV_YOM_TOV, "erev_pesach", (14, Months.NISAN), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "pesach", (15, Months.NISAN), "", ""),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_pesach", (16, Months.NISAN), "ISRAEL", []
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        ([17, 18, 19], Months.NISAN),
        "",
        [],
    ),
    HOLIDAY(HolidayTypes.EREV_YOM_TOV, "hol_hamoed_pesach", (20, Months.NISAN), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "pesach_vii", (21, Months.NISAN), "", []),
    HOLIDAY(
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
    HOLIDAY(
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
    HOLIDAY(HolidayTypes.MINOR_HOLIDAY, "lag_bomer", (18, Months.IYYAR), "", []),
    HOLIDAY(HolidayTypes.EREV_YOM_TOV, "erev_shavuot", (5, Months.SIVAN), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "shavuot", (6, Months.SIVAN), "", []),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        ([17, 18], Months.TAMMUZ),
        "",
        [move_if_not_on_dow(17, 18, 5, 6)],
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        ([9, 10], Months.AV),
        "",
        [move_if_not_on_dow(9, 10, 5, 6)],
    ),
    HOLIDAY(HolidayTypes.MINOR_HOLIDAY, "tu_bav", (15, Months.AV), "", []),
    HOLIDAY(
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
    HOLIDAY(
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
    HOLIDAY(
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
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_yerushalayim",
        (28, Months.IYYAR),
        "",
        [year_is_after(5727)],
    ),
    HOLIDAY(HolidayTypes.YOM_TOV, "shmini_atzeret", (22, Months.TISHREI), "", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "pesach_viii", (22, Months.NISAN), "DIASPORA", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "shavuot_ii", (7, Months.SIVAN), "DIASPORA", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "sukkot_ii", (16, Months.TISHREI), "DIASPORA", []),
    HOLIDAY(HolidayTypes.YOM_TOV, "pesach_ii", (16, Months.NISAN), "DIASPORA", []),
    HOLIDAY(
        HolidayTypes.ISRAEL_NATIONAL_HOLIDAY,
        "family_day",
        (30, Months.SHVAT),
        "ISRAEL",
        [year_is_after(5734)],
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "memorial_day_unknown",
        (7, [Months.ADAR, Months.ADAR_II]),
        "ISRAEL",
        [correct_adar()],
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        ([11, 12], Months.MARCHESHVAN),
        "ISRAEL",
        [move_if_not_on_dow(12, 11, 4, 3), year_is_after(5757)],
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "zeev_zhabotinsky_day",
        (29, Months.TAMMUZ),
        "ISRAEL",
        [year_is_after(5764)],
    ),
    HOLIDAY(
        HolidayTypes.ROSH_CHODESH,
        "rosh_chodesh",
        ([1, 30], list(Months)),
        "",
        [correct_adar(), legal_month_length(), not_rosh_chodesh()],
    ),
)

HOLIDAY_DESCRIPTIONS = {
    "none": LANG("", "", DESC("", "")),
    "erev_rosh_hashana": LANG(
        "Veille de Rosh Hashana", "Erev Rosh Hashana", DESC("ערב ראש השנה", 'ערב ר"ה')
    ),
    "rosh_hashana_i": LANG(
        "Rosh Hashana I", "Rosh Hashana I", DESC("א' ראש השנה", 'א ר"ה')
    ),
    "rosh_hashana_ii": LANG(
        "Rosh Hashana II", "Rosh Hashana II", DESC("ב' ראש השנה", "ב' ר\"ה")
    ),
    "tzom_gedaliah": LANG(
        "Jeûne de Guedalia", "Tzom Gedaliah", DESC("צום גדליה", "צום גדליה")
    ),
    "erev_yom_kippur": LANG(
        "Veille de Yom Kippour", "Erev Yom Kippur", DESC('עיוה"כ', 'עיוה"כ')
    ),
    "yom_kippur": LANG("Yom Kippour", "Yom Kippur", DESC("יום הכפורים", 'יוה"כ')),
    "erev_sukkot": LANG(
        "Veille de Souccot", "Erev Sukkot", DESC("ערב סוכות", "ערב סוכות")
    ),
    "sukkot": LANG("Souccot", "Sukkot", DESC("סוכות", "סוכות")),
    "hol_hamoed_sukkot": LANG(
        "Hol hamoed Souccot",
        "Hol hamoed Sukkot",
        DESC("חול המועד סוכות", 'חוה"מ סוכות'),
    ),
    "hoshana_raba": LANG("Hoshaâna Rabba", "Hoshana Raba", DESC("הושענא רבה", 'הוש"ר')),
    "simchat_torah": LANG("Simhat Torah", "Simchat Torah", DESC("שמחת תורה", 'שמח"ת')),
    "chanukah": LANG("Hanoukka", "Chanukah", DESC("חנוכה", "חנוכה")),
    "asara_btevet": LANG("10 Tevet", "Asara B'Tevet", DESC("צום עשרה בטבת", "י' בטבת")),
    "tu_bshvat": LANG("Tou Bichvat", "Tu B'Shvat", DESC('ט"ו בשבט', 'ט"ו בשבט')),
    "taanit_esther": LANG(
        "Jeûne d'Esther", "Ta'anit Esther", DESC("תענית אסתר", "תענית אסתר")
    ),
    "purim": LANG("Pourim", "Purim", DESC("פורים", "פורים")),
    "shushan_purim": LANG(
        "Pourim Shoushan", "Shushan Purim", DESC("שושן פורים", "שושן פורים")
    ),
    "erev_pesach": LANG("Veille de Pessah", "Erev Pesach", DESC("ערב פסח", "ערב פסח")),
    "pesach": LANG("Pessah", "Pesach", DESC("פסח", "פסח")),
    "hol_hamoed_pesach": LANG(
        "Hol hamoed Pessah", "Hol hamoed Pesach", DESC("חול המועד פסח", 'חוה"מ פסח')
    ),
    "pesach_vii": LANG("Pessah VII", "Pesach VII", DESC("שביעי פסח", "ז' פסח")),
    "yom_haatzmaut": LANG(
        "Yom HaAtsmaout", "Yom HaAtzma'ut", DESC("יום העצמאות", "יום העצמאות")
    ),
    "lag_bomer": LANG("Lag Ba Omer", "Lag B'Omer", DESC('ל"ג בעומר', 'ל"ג בעומר')),
    "erev_shavuot": LANG(
        "Veille de Shavouot", "Erev Shavuot", DESC("ערב שבועות", "ערב שבועות")
    ),
    "shavuot": LANG("Shavouot", "Shavuot", DESC("שבועות", "שבועות")),
    "tzom_tammuz": LANG(
        "Jeûne du 17 Tamouz", "Tzom Tammuz", DESC("צום שבעה עשר בתמוז", "צום תמוז")
    ),
    "tisha_bav": LANG("Tisha Be'Av", "Tish'a B'Av", DESC("תשעה באב", "ט' באב")),
    "tu_bav": LANG("Tou be'Av", "Tu B'Av", DESC('ט"ו באב', 'ט"ו באב')),
    "yom_hashoah": LANG("Yom HaShoah", "Yom HaShoah", DESC("יום השואה", "יום השואה")),
    "yom_hazikaron": LANG(
        "Yom haZicaron", "Yom HaZikaron", DESC("יום הזכרון", "יום הזכרון")
    ),
    "yom_yerushalayim": LANG(
        "Yom Yeroushalaïm", "Yom Yerushalayim", DESC("יום ירושלים", "יום י-ם")
    ),
    "shmini_atzeret": LANG(
        "Shemini Atseret", "Shmini Atzeret", DESC("שמיני עצרת", "שמיני עצרת")
    ),
    "pesach_viii": LANG(
        "Pessah VIII", "Pesach VIII", DESC("אחרון של פסח", "אחרון של פסח")
    ),
    "shavuot_ii": LANG("Shavouot II", "Shavuot II", DESC("שני של שבועות", "ב' שבועות")),
    "sukkot_ii": LANG("Souccot II", "Sukkot II", DESC("שני של סוכות", "ב' סוכות")),
    "pesach_ii": LANG("Pessah II", "Pesach II", DESC("שני של פסח", "ב' פסח")),
    "family_day": LANG(
        "Fête de la Famille", "Family Day", DESC("יום המשפחה", "יום המשפחה")
    ),
    "memorial_day_unknown": LANG(
        "Jour du souvenir",
        "Memorial day for fallen whose place of burial is unknown",
        DESC("יום זכרון...", "יום זכרון..."),
    ),
    "rabin_memorial_day": LANG(
        "Jour commémoratif Yitzhak Rabin",
        "Yitzhak Rabin memorial day",
        DESC("יום הזכרון ליצחק רבין", "יום הזכרון ליצחק רבין"),
    ),
    "zeev_zhabotinsky_day": LANG(
        "Jour de Zeev Zhabotinsky",
        "Zeev Zhabotinsky day",
        DESC("יום ז'בוטינסקי", "יום ז'בוטינסקי"),
    ),
    "rosh_chodesh": LANG("Rosh Hodesh", "Rosh Chodesh", DESC("ראש חודש", "ראש חודש")),
}


def holiday_name(entry: HOLIDAY, language: str) -> str:
    """Return the description of a holiday in the specified language."""
    # Assume each `entry` has a `name` attribute that corresponds to a key in list.
    description_entry = HOLIDAY_DESCRIPTIONS.get(entry.name)

    if not description_entry:
        return "Unknown Holiday"

    # Try to get the requested language description
    entry_language = getattr(description_entry, language, None)
    if entry_language:
        return (
            entry_language.long if isinstance(entry_language, DESC) else entry_language
        )

    # If the requested language is not available, fallback to English
    return description_entry.english


def get_all_holidays(language: str) -> list[str]:
    """Helper method to get all the holiday descriptions in the specified language."""

    holidays_list = [holiday_name(h, language) for h in HOLIDAYS]

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
MESECHTA = namedtuple("MESECHTA", ["name", "pages"])
DAF_YOMI_MESECHTOS = (
    MESECHTA(LANG("Berakhot", "Berachos", "ברכות"), 63),
    MESECHTA(LANG("Shabbat", "Shabbos", "שבת"), 156),
    MESECHTA(LANG("Erouvin", "Eruvin", "עירובין"), 104),
    MESECHTA(LANG("Pessa'him", "Pesachim", "פסחים"), 120),
    MESECHTA(LANG("Chekalim", "Shekalim", "שקלים"), 21),
    MESECHTA(LANG("Yoma", "Yoma", "יומא"), 87),
    MESECHTA(LANG("Soucca", "Succah", "סוכה"), 55),
    MESECHTA(LANG("Beitsa", "Beitzah", "ביצה"), 39),
    MESECHTA(LANG("Roch Hachana", "Rosh Hashanah", "ראש השנה"), 34),
    MESECHTA(LANG("Ta'anit", "Taanis", "תענית"), 30),
    MESECHTA(LANG("Meguila", "Megillah", "מגילה"), 31),
    MESECHTA(LANG("Moëd Katan", "Moed Katan", "מועד קטן"), 28),
    MESECHTA(LANG("Haguiga", "Chagigah", "חגיגה"), 26),
    MESECHTA(LANG("Yevamot", "Yevamos", "יבמות"), 121),
    MESECHTA(LANG("Ketouvot", "Kesubos", "כתובות"), 111),
    MESECHTA(LANG("Nédarim", "Nedarim", "נדרים"), 90),
    MESECHTA(LANG("Nazir", "Nazir", "נזיר"), 65),
    MESECHTA(LANG("Sota", "Sotah", "סוטה"), 48),
    MESECHTA(LANG("Guittin", "Gittin", "גיטין"), 89),
    MESECHTA(LANG("Kidouchin", "Kiddushin", "קידושין"), 81),
    MESECHTA(LANG("Baba Kama", "Bava Kamma", "בבא קמא"), 118),
    MESECHTA(LANG("Baba Metsia", "Bava Metzia", "בבא מציעא"), 118),
    MESECHTA(LANG("Baba Batra", "Bava Basra", "בבא בתרא"), 175),
    MESECHTA(LANG("Sanhedrin", "Sanhedrin", "סנהדרין"), 112),
    MESECHTA(LANG("Makot", "Makkos", "מכות"), 23),
    MESECHTA(LANG("Chevouot", "Shevuos", "שבועות"), 48),
    MESECHTA(LANG("Avoda Zara", "Avodah Zarah", "עבודה זרה"), 75),
    MESECHTA(LANG("Horayot", "Horayos", "הוריות"), 13),
    MESECHTA(LANG("Zevahim", "Zevachim", "זבחים"), 119),
    MESECHTA(LANG("Menahot", "Menachos", "מנחות"), 109),
    MESECHTA(LANG("Houlin", "Chullin", "חולין"), 141),
    MESECHTA(LANG("Bekhorot", "Bechoros", "בכורות"), 60),
    MESECHTA(LANG("Arakhin", "Arachin", "ערכין"), 33),
    MESECHTA(LANG("Temoura", "Temurah", "תמורה"), 33),
    MESECHTA(LANG("Keritot", "Kereisos", "כריתות"), 27),
    MESECHTA(LANG("Me'ila", "Meilah", "מעילה"), 36),
    MESECHTA(LANG("Nida", "Niddah", "נדה"), 72),
)

DAF_YOMI_TOTAL_PAGES = sum(mesechta.pages for mesechta in DAF_YOMI_MESECHTOS)
