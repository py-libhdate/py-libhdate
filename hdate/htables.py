"""Constant lookup tables for hdate modules."""

import datetime
from collections import namedtuple
from enum import Enum

READING = namedtuple("READING", "year_type, readings")

READINGS = (
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

READINGS = dict((year_type, r.readings) for r in READINGS for year_type in r.year_type)

DIGITS = (
    (" ", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"),
    ("ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"),
    (" ", "ק", "ר", "ש", "ת"),
)

LANG = namedtuple("LANG", "english, hebrew")
DESC = namedtuple("DESC", "long, short")

DAYS = (
    LANG(DESC("Sunday", "Sun"), DESC("ראשון", "א")),
    LANG(DESC("Monday", "Mon"), DESC("שני", "ב")),
    LANG(DESC("Tuesday", "Tue"), DESC("שלישי", "ג")),
    LANG(DESC("Wednesday", "Wed"), DESC("רביעי", "ד")),
    LANG(DESC("Thursday", "Thu"), DESC("חמישי", "ה")),
    LANG(DESC("Friday", "Fri"), DESC("שישי", "ו")),
    LANG(DESC("Saturday", "Sat"), DESC("שבת", "ז")),
)

PARASHAOT = (
    LANG("none", "none"),
    LANG("Bereshit", "בראשית"),
    LANG("Noach", "נח"),
    LANG("Lech-Lecha", "לך לך"),
    LANG("Vayera", "וירא"),
    LANG("Chayei Sara", "חיי שרה"),
    LANG("Toldot", "תולדות"),
    LANG("Vayetzei", "ויצא"),
    LANG("Vayishlach", "וישלח"),
    LANG("Vayeshev", "וישב"),
    LANG("Miketz", "מקץ"),
    LANG("Vayigash", "ויגש"),
    LANG("Vayechi", "ויחי"),
    LANG("Shemot", "שמות"),
    LANG("Vaera", "וארא"),
    LANG("Bo", "בא"),
    LANG("Beshalach", "בשלח"),
    LANG("Yitro", "יתרו"),
    LANG("Mishpatim", "משפטים"),
    LANG("Terumah", "תרומה"),
    LANG("Tetzaveh", "תצוה"),
    LANG("Ki Tisa", "כי תשא"),
    LANG("Vayakhel", "ויקהל"),
    LANG("Pekudei", "פקודי"),
    LANG("Vayikra", "ויקרא"),
    LANG("Tzav", "צו"),
    LANG("Shmini", "שמיני"),
    LANG("Tazria", "תזריע"),
    LANG("Metzora", "מצורע"),
    LANG("Achrei Mot", "אחרי מות"),
    LANG("Kedoshim", "קדושים"),
    LANG("Emor", "אמור"),
    LANG("Behar", "בהר"),
    LANG("Bechukotai", "בחוקתי"),
    LANG("Bamidbar", "במדבר"),
    LANG("Nasso", "נשא"),
    LANG("Beha'alotcha", "בהעלתך"),
    LANG("Sh'lach", "שלח"),
    LANG("Korach", "קרח"),
    LANG("Chukat", "חקת"),
    LANG("Balak", "בלק"),
    LANG("Pinchas", "פנחס"),
    LANG("Matot", "מטות"),
    LANG("Masei", "מסעי"),
    LANG("Devarim", "דברים"),
    LANG("Vaetchanan", "ואתחנן"),
    LANG("Eikev", "עקב"),
    LANG("Re'eh", "ראה"),
    LANG("Shoftim", "שופטים"),
    LANG("Ki Teitzei", "כי תצא"),
    LANG("Ki Tavo", "כי תבוא"),
    LANG("Nitzavim", "נצבים"),
    LANG("Vayeilech", "וילך"),
    LANG("Ha'Azinu", "האזינו"),
    LANG("Vezot Habracha", "וזאת הברכה"),
    LANG("Vayakhel-Pekudei", "ויקהל-פקודי"),
    LANG("Tazria-Metzora", "תזריע-מצורע"),
    LANG("Achrei Mot-Kedoshim", "אחרי מות-קדושים"),
    LANG("Behar-Bechukotai", "בהר-בחוקתי"),
    LANG("Chukat-Balak", "חוקת-בלק"),
    LANG("Matot-Masei", "מטות מסעי"),
    LANG("Nitzavim-Vayeilech", "נצבים-וילך"),
)

MONTHS = (
    LANG("Tishrei", "תשרי"),
    LANG("Marcheshvan", "מרחשוון"),
    LANG("Kislev", "כסלו"),
    LANG("Tevet", "טבת"),
    LANG("Sh'vat", "שבט"),
    LANG("Adar", "אדר"),
    LANG("Nisan", "ניסן"),
    LANG("Iyyar", "אייר"),
    LANG("Sivan", "סיון"),
    LANG("Tammuz", "תמוז"),
    LANG("Av", "אב"),
    LANG("Elul", "אלול"),
    LANG("Adar I", "אדר א"),
    LANG("Adar II", "אדר ב"),
)


class Months(Enum):
    """Enum class for the Hebrew months."""

    Tishrei = 1
    Marcheshvan = 2
    Kislev = 3
    Tevet = 4
    Shvat = 5
    Adar = 6
    Nisan = 7
    Iyyar = 8
    Sivan = 9
    Tammuz = 10
    Av = 11
    Elul = 12
    Adar_I = 13
    Adar_II = 14


def year_is_after(year):
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is after the
    requested year.
    """
    return lambda x: x.hdate.year > year


def year_is_before(year):
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is before the
    requested year.
    """
    return lambda x: x.hdate.year < year


def move_if_not_on_dow(original, replacement, dow_not_orig, dow_replacement):
    """
    Return a lambda function.

    Lambda checks that either the original day does not fall on a given
    weekday, or that the replacement day does fall on the expected weekday.
    """
    return lambda x: (
        (x.hdate.day == original and x.gdate.weekday() != dow_not_orig)
        or (x.hdate.day == replacement and x.gdate.weekday() == dow_replacement)
    )


HOLIDAY = namedtuple(
    "HOLIDAY",
    ["type", "name", "date", "israel_diaspora", "date_functions_list", "description"],
)


class HolidayTypes(Enum):
    """Container class for holiday type integer mappings."""

    UNKNOWN = 0
    YOM_TOV = 1
    EREV_YOM_TOV = 2
    HOL_HAMOED = 3
    MELACHA_PERMITTED_HOLIDAY = 4
    FAST_DAY = 5
    MODERN_HOLIDAY = 6
    MINOR_HOLIDAY = 7
    MEMORIAL_DAY = 8
    ISRAEL_NATIONAL_HOLIDAY = 9


HOLIDAYS = (
    HOLIDAY(HolidayTypes.UNKNOWN, "", (), "", [], LANG("", DESC("", ""))),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_rosh_hashana",
        (29, Months.Elul),
        "",
        [],
        LANG("Erev Rosh Hashana", DESC("ערב ראש השנה", 'ערב ר"ה')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "rosh_hashana_i",
        (1, Months.Tishrei),
        "",
        [],
        LANG("Rosh Hashana I", DESC("א' ראש השנה", 'א ר"ה')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "rosh_hashana_ii",
        (2, Months.Tishrei),
        "",
        [],
        LANG("Rosh Hashana II", DESC("ב' ראש השנה", "ב' ר\"ה")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        ([3, 4], Months.Tishrei),
        "",
        [move_if_not_on_dow(3, 4, 5, 6)],
        LANG("Tzom Gedaliah", DESC("צום גדליה", "צום גדליה")),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_yom_kippur",
        (9, Months.Tishrei),
        "",
        [],
        LANG("Erev Yom Kippur", DESC('עיוה"כ', 'עיוה"כ')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "yom_kippur",
        (10, Months.Tishrei),
        "",
        [],
        LANG("Yom Kippur", DESC("יום הכפורים", 'יוה"כ')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_sukkot",
        (14, Months.Tishrei),
        "",
        [],
        LANG("Erev Sukkot", DESC("ערב סוכות", "ערב סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "sukkot",
        (15, Months.Tishrei),
        "",
        [],
        LANG("Sukkot", DESC("סוכות", "סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        (16, Months.Tishrei),
        "ISRAEL",
        "",
        LANG("Hol hamoed Sukkot", DESC("חול המועד סוכות", 'חוה"מ סוכות')),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        ([17, 18, 19, 20], Months.Tishrei),
        "",
        "",
        LANG("Hol hamoed Sukkot", DESC("חול המועד סוכות", 'חוה"מ סוכות')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "hoshana_raba",
        (21, Months.Tishrei),
        "",
        [],
        LANG("Hoshana Raba", DESC("הושענא רבה", 'הוש"ר')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "simchat_torah",
        (23, Months.Tishrei),
        "DIASPORA",
        [],
        LANG("Simchat Torah", DESC("שמחת תורה", 'שמח"ת')),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        (list(range(25, 30)), Months.Kislev),
        "",
        [],
        LANG("Chanukah", DESC("חנוכה", "חנוכה")),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        ([1, 2, 3], Months.Tevet),
        "",
        [
            lambda x: (
                (x.short_kislev() and x.hdate.day == 3) or (x.hdate.day in [1, 2])
            )
        ],
        LANG("Chanukah", DESC("חנוכה", "חנוכה")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "asara_btevet",
        (10, Months.Tevet),
        "",
        [],
        LANG("Asara B'Tevet", DESC("צום עשרה בטבת", "י' בטבת")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "tu_bshvat",
        (15, Months.Shvat),
        "",
        [],
        LANG("Tu B'Shvat", DESC('ט"ו בשבט', 'ט"ו בשבט')),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ([11, 13], [Months.Adar, Months.Adar_II]),
        "",
        [move_if_not_on_dow(13, 11, 5, 3)],
        LANG("Ta'anit Esther", DESC("תענית אסתר", "תענית אסתר")),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        (14, [Months.Adar, Months.Adar_II]),
        "",
        [],
        LANG("Purim", DESC("פורים", "פורים")),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        (15, [Months.Adar, Months.Adar_II]),
        "",
        [],
        LANG("Shushan Purim", DESC("שושן פורים", "שושן פורים")),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_pesach",
        (14, Months.Nisan),
        "",
        [],
        LANG("Erev Pesach", DESC("ערב פסח", "ערב פסח")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach",
        (15, Months.Nisan),
        "",
        "",
        LANG("Pesach", DESC("פסח", "פסח")),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        (16, Months.Nisan),
        "ISRAEL",
        [],
        LANG("Hol hamoed Pesach", DESC("חול המועד פסח", 'חוה"מ פסח')),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        ([17, 18, 19], Months.Nisan),
        "",
        [],
        LANG("Hol hamoed Pesach", DESC("חול המועד פסח", 'חוה"מ פסח')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "hol_hamoed_pesach",
        (20, Months.Nisan),
        "",
        [],
        LANG("Hol hamoed Pesach", DESC("חול המועד פסח", 'חוה"מ פסח')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_vii",
        (21, Months.Nisan),
        "",
        [],
        LANG("Pesach VII", DESC("שביעי פסח", "ז' פסח")),
    ),
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ([3, 4, 5], Months.Iyyar),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(5, 4, 4, 3) or move_if_not_on_dow(5, 3, 5, 3),
        ],
        LANG("Yom HaAtzma'ut", DESC("יום העצמאות", "יום העצמאות")),
    ),
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ([3, 4, 5, 6], Months.Iyyar),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(5, 4, 4, 3)
            or move_if_not_on_dow(5, 3, 5, 3)
            or move_if_not_on_dow(5, 6, 0, 1),
        ],
        LANG("Yom HaAtzma'ut", DESC("יום העצמאות", "יום העצמאות")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "lag_bomer",
        (18, Months.Iyyar),
        "",
        [],
        LANG("Lag B'Omer", DESC('ל"ג בעומר', 'ל"ג בעומר')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_shavuot",
        (5, Months.Sivan),
        "",
        [],
        LANG("Erev Shavuot", DESC("ערב שבועות", "ערב שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shavuot",
        (6, Months.Sivan),
        "",
        [],
        LANG("Shavuot", DESC("שבועות", "שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        ([17, 18], Months.Tammuz),
        "",
        [move_if_not_on_dow(17, 18, 5, 6)],
        LANG("Tzom Tammuz", DESC("צום שבעה עשר בתמוז", "צום תמוז")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        ([9, 10], Months.Av),
        "",
        [move_if_not_on_dow(9, 10, 5, 6)],
        LANG("Tish'a B'Av", DESC("תשעה באב", "ט' באב")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "tu_bav",
        (15, Months.Av),
        "",
        [],
        LANG("Tu B'Av", DESC('ט"ו באב', 'ט"ו באב')),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hashoah",
        ([26, 27, 28], Months.Nisan),
        "",
        [
            move_if_not_on_dow(27, 28, 6, 0) or move_if_not_on_dow(27, 26, 4, 3),
            year_is_after(5718),
        ],
        LANG("Yom HaShoah", DESC("יום השואה", "יום השואה")),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ([2, 3, 4], Months.Iyyar),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(4, 3, 3, 2) or move_if_not_on_dow(4, 2, 4, 2),
        ],
        LANG("Yom HaZikaron", DESC("יום הזכרון", "יום הזכרון")),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ([2, 3, 4, 5], Months.Iyyar),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(4, 3, 3, 2)
            or move_if_not_on_dow(4, 2, 4, 2)
            or move_if_not_on_dow(4, 5, 6, 0),
        ],
        LANG("Yom HaZikaron", DESC("יום הזכרון", "יום הזכרון")),
    ),
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_yerushalayim",
        (28, Months.Iyyar),
        "",
        [year_is_after(5727)],
        LANG("Yom Yerushalayim", DESC("יום ירושלים", "יום י-ם")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shmini_atzeret",
        (22, Months.Tishrei),
        "",
        [],
        LANG("Shmini Atzeret", DESC("שמיני עצרת", "שמיני עצרת")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_viii",
        (22, Months.Nisan),
        "DIASPORA",
        [],
        LANG("Pesach VIII", DESC("אחרון של פסח", "אחרון של פסח")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shavuot_ii",
        (7, Months.Sivan),
        "DIASPORA",
        [],
        LANG("Shavuot II", DESC("שני של שבועות", "ב' שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "sukkot_ii",
        (16, Months.Tishrei),
        "DIASPORA",
        [],
        LANG("Sukkot II", DESC("שני של סוכות", "ב' סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_ii",
        (16, Months.Nisan),
        "DIASPORA",
        [],
        LANG("Pesach II", DESC("שני של פסח", "ב' פסח")),
    ),
    HOLIDAY(
        HolidayTypes.ISRAEL_NATIONAL_HOLIDAY,
        "family_day",
        (30, Months.Shvat),
        "ISRAEL",
        [year_is_after(5734)],
        LANG("Family Day", DESC("יום המשפחה", "יום המשפחה")),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "memorial_day_unknown",
        (7, [Months.Adar, Months.Adar_II]),
        "ISRAEL",
        [],
        LANG(
            "Memorial day for fallen whose place of burial is unknown",
            DESC("יום זכרון...", "יום זכרון..."),
        ),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        ([11, 12], Months.Marcheshvan),
        "ISRAEL",
        [move_if_not_on_dow(12, 11, 4, 3), year_is_after(5757)],
        LANG(
            "Yitzhak Rabin memorial day",
            DESC("יום הזכרון ליצחק רבין", "יום הזכרון ליצחק רבין"),
        ),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "zeev_zhabotinsky_day",
        (29, Months.Tammuz),
        "ISRAEL",
        [year_is_after(5764)],
        LANG("Zeev Zhabotinsky day", DESC("יום ז'בוטינסקי", "יום ז'בוטינסקי")),
    ),
)

ZMAN = namedtuple("ZMAN", "zman, description")
ZMANIM = (
    ZMAN("first_light", LANG("Alot HaShachar", "עלות השחר")),
    ZMAN("talit", LANG("Talit & Tefilin's time", "זמן טלית ותפילין")),
    ZMAN("sunrise", LANG("Sunrise", "הנץ החמה")),
    ZMAN("mga_end_shma", LANG('Shema EOT MG"A', 'סוף זמן ק"ש מג"א')),
    ZMAN("gra_end_shma", LANG('Shema EOT GR"A', 'סוף זמן ק"ש גר"א')),
    ZMAN("mga_end_tfila", LANG('Tefila EOT MG"A', 'סוף זמן תפילה מג"א')),
    ZMAN("gra_end_tfila", LANG('Tefila EOT GR"A', 'סוף זמן תפילה גר"א')),
    ZMAN("midday", LANG("Midday", "חצות היום")),
    ZMAN("big_mincha", LANG("Big Mincha", "מנחה גדולה")),
    ZMAN("small_mincha", LANG("Small Mincha", "מנחה קטנה")),
    ZMAN("plag_mincha", LANG("Plag Mincha", "פלג המנחה")),
    ZMAN("sunset", LANG("Sunset", "שקיעה")),
    ZMAN("first_stars", LANG("First stars", "צאת הכוכבים")),
    ZMAN("midnight", LANG("Midnight", "חצות הלילה")),
)

# The first few cycles were only 2702 blatt. After that it became 2711. Even with
# that, the math doesn't play nicely with the dates before the 11th cycle :(
# From cycle 11 onwards, it was simple and sequential
DAF_YOMI_CYCLE_11_START = datetime.date(1997, 9, 29)
MESECHTA = namedtuple("MESECHTA", ["name", "pages"])
DAF_YOMI_MESECHTOS = (
    MESECHTA(LANG("Berachos", "ברכות"), 63),
    MESECHTA(LANG("Shabbos", "שבת"), 156),
    MESECHTA(LANG("Eruvin", "עירובין"), 104),
    MESECHTA(LANG("Pesachim", "פסחים"), 120),
    MESECHTA(LANG("Shekalim", "שקלים"), 21),
    MESECHTA(LANG("Yoma", "יומא"), 87),
    MESECHTA(LANG("Succah", "סוכה"), 55),
    MESECHTA(LANG("Beitzah", "ביצה"), 39),
    MESECHTA(LANG("Rosh Hashanah", "ראש השנה"), 34),
    MESECHTA(LANG("Taanis", "תענית"), 30),
    MESECHTA(LANG("Megillah", "מגילה"), 31),
    MESECHTA(LANG("Moed Katan", "מועד קטן"), 28),
    MESECHTA(LANG("Chagigah", "חגיגה"), 26),
    MESECHTA(LANG("Yevamos", "יבמות"), 121),
    MESECHTA(LANG("Kesubos", "כתובות"), 111),
    MESECHTA(LANG("Nedarim", "נדרים"), 90),
    MESECHTA(LANG("Nazir", "נזיר"), 65),
    MESECHTA(LANG("Sotah", "סוטה"), 48),
    MESECHTA(LANG("Gittin", "גיטין"), 89),
    MESECHTA(LANG("Kiddushin", "קידושין"), 81),
    MESECHTA(LANG("Bava Kamma", "בבא קמא"), 118),
    MESECHTA(LANG("Bava Metzia", "בבא מציעא"), 118),
    MESECHTA(LANG("Bava Basra", "בבא בתרא"), 175),
    MESECHTA(LANG("Sanhedrin", "סנהדרין"), 112),
    MESECHTA(LANG("Makkos", "מכות"), 23),
    MESECHTA(LANG("Shevuos", "שבועות"), 48),
    MESECHTA(LANG("Avodah Zarah", "עבודה זרה"), 75),
    MESECHTA(LANG("Horayos", "הוריות"), 13),
    MESECHTA(LANG("Zevachim", "זבחים"), 119),
    MESECHTA(LANG("Menachos", "מנחות"), 109),
    MESECHTA(LANG("Chullin", "חולין"), 141),
    MESECHTA(LANG("Bechoros", "בכורות"), 60),
    MESECHTA(LANG("Arachin", "ערכין"), 33),
    MESECHTA(LANG("Temurah", "תמורה"), 33),
    MESECHTA(LANG("Kereisos", "כריתות"), 27),
    MESECHTA(LANG("Meilah", "מעילה"), 36),
    MESECHTA(LANG("Niddah", "נדה"), 72),
)

DAF_YOMI_TOTAL_PAGES = sum(mesechta.pages for mesechta in DAF_YOMI_MESECHTOS)
