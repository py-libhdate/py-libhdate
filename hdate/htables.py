# -*- coding: utf-8 -*-
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
    (u" ", u"א", u"ב", u"ג", u"ד", u"ה", u"ו", u"ז", u"ח", u"ט"),
    (u"ט", u"י", u"כ", u"ל", u"מ", u"נ", u"ס", u"ע", u"פ", u"צ"),
    (u" ", u"ק", u"ר", u"ש", u"ת"),
)

LANG = namedtuple("LANG", "english, hebrew")
DESC = namedtuple("DESC", "long, short")

DAYS = (
    LANG(DESC(u"Sunday", u"Sun"), DESC(u"ראשון", u"א")),
    LANG(DESC(u"Monday", u"Mon"), DESC(u"שני", u"ב")),
    LANG(DESC(u"Tuesday", u"Tue"), DESC(u"שלישי", u"ג")),
    LANG(DESC(u"Wednesday", u"Wed"), DESC(u"רביעי", u"ד")),
    LANG(DESC(u"Thursday", u"Thu"), DESC(u"חמישי", u"ה")),
    LANG(DESC(u"Friday", u"Fri"), DESC(u"שישי", u"ו")),
    LANG(DESC(u"Saturday", u"Sat"), DESC(u"שבת", u"ז")),
)

PARASHAOT = (
    LANG(u"none", u"none"),
    LANG(u"Bereshit", u"בראשית"),
    LANG(u"Noach", u"נח"),
    LANG(u"Lech-Lecha", u"לך לך"),
    LANG(u"Vayera", u"וירא"),
    LANG(u"Chayei Sara", u"חיי שרה"),
    LANG(u"Toldot", u"תולדות"),
    LANG(u"Vayetzei", u"ויצא"),
    LANG(u"Vayishlach", u"וישלח"),
    LANG(u"Vayeshev", u"וישב"),
    LANG(u"Miketz", u"מקץ"),
    LANG(u"Vayigash", u"ויגש"),
    LANG(u"Vayechi", u"ויחי"),
    LANG(u"Shemot", u"שמות"),
    LANG(u"Vaera", u"וארא"),
    LANG(u"Bo", u"בא"),
    LANG(u"Beshalach", u"בשלח"),
    LANG(u"Yitro", u"יתרו"),
    LANG(u"Mishpatim", u"משפטים"),
    LANG(u"Terumah", u"תרומה"),
    LANG(u"Tetzaveh", u"תצוה"),
    LANG(u"Ki Tisa", u"כי תשא"),
    LANG(u"Vayakhel", u"ויקהל"),
    LANG(u"Pekudei", u"פקודי"),
    LANG(u"Vayikra", u"ויקרא"),
    LANG(u"Tzav", u"צו"),
    LANG(u"Shmini", u"שמיני"),
    LANG(u"Tazria", u"תזריע"),
    LANG(u"Metzora", u"מצורע"),
    LANG(u"Achrei Mot", u"אחרי מות"),
    LANG(u"Kedoshim", u"קדושים"),
    LANG(u"Emor", u"אמור"),
    LANG(u"Behar", u"בהר"),
    LANG(u"Bechukotai", u"בחוקתי"),
    LANG(u"Bamidbar", u"במדבר"),
    LANG(u"Nasso", u"נשא"),
    LANG(u"Beha'alotcha", u"בהעלתך"),
    LANG(u"Sh'lach", u"שלח"),
    LANG(u"Korach", u"קרח"),
    LANG(u"Chukat", u"חקת"),
    LANG(u"Balak", u"בלק"),
    LANG(u"Pinchas", u"פנחס"),
    LANG(u"Matot", u"מטות"),
    LANG(u"Masei", u"מסעי"),
    LANG(u"Devarim", u"דברים"),
    LANG(u"Vaetchanan", u"ואתחנן"),
    LANG(u"Eikev", u"עקב"),
    LANG(u"Re'eh", u"ראה"),
    LANG(u"Shoftim", u"שופטים"),
    LANG(u"Ki Teitzei", u"כי תצא"),
    LANG(u"Ki Tavo", u"כי תבוא"),
    LANG(u"Nitzavim", u"נצבים"),
    LANG(u"Vayeilech", u"וילך"),
    LANG(u"Ha'Azinu", u"האזינו"),
    LANG(u"Vezot Habracha", u"וזאת הברכה"),
    LANG(u"Vayakhel-Pekudei", u"ויקהל-פקודי"),
    LANG(u"Tazria-Metzora", u"תזריע-מצורע"),
    LANG(u"Achrei Mot-Kedoshim", u"אחרי מות-קדושים"),
    LANG(u"Behar-Bechukotai", u"בהר-בחוקתי"),
    LANG(u"Chukat-Balak", u"חוקת-בלק"),
    LANG(u"Matot-Masei", u"מטות מסעי"),
    LANG(u"Nitzavim-Vayeilech", u"נצבים-וילך"),
)

MONTHS = (
    LANG(u"Tishrei", u"תשרי"),
    LANG(u"Marcheshvan", u"מרחשוון"),
    LANG(u"Kislev", u"כסלו"),
    LANG(u"Tevet", u"טבת"),
    LANG(u"Sh'vat", u"שבט"),
    LANG(u"Adar", u"אדר"),
    LANG(u"Nisan", u"ניסן"),
    LANG(u"Iyyar", u"אייר"),
    LANG(u"Sivan", u"סיון"),
    LANG(u"Tammuz", u"תמוז"),
    LANG(u"Av", u"אב"),
    LANG(u"Elul", u"אלול"),
    LANG(u"Adar I", u"אדר א"),
    LANG(u"Adar II", u"אדר ב"),
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
    HOLIDAY(HolidayTypes.UNKNOWN, "", (), "", [], LANG(u"", DESC(u"", u""))),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_rosh_hashana",
        (29, Months.Elul),
        "",
        [],
        LANG(u"Erev Rosh Hashana", DESC(u"ערב ראש השנה", u'ערב ר"ה')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "rosh_hashana_i",
        (1, Months.Tishrei),
        "",
        [],
        LANG(u"Rosh Hashana I", DESC(u"א' ראש השנה", u'א ר"ה')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "rosh_hashana_ii",
        (2, Months.Tishrei),
        "",
        [],
        LANG(u"Rosh Hashana II", DESC(u"ב' ראש השנה", u"ב' ר\"ה")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        ([3, 4], Months.Tishrei),
        "",
        [move_if_not_on_dow(3, 4, 5, 6)],
        LANG(u"Tzom Gedaliah", DESC(u"צום גדליה", u"צום גדליה")),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_yom_kippur",
        (9, Months.Tishrei),
        "",
        [],
        LANG(u"Erev Yom Kippur", DESC(u'עיוה"כ', u'עיוה"כ')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "yom_kippur",
        (10, Months.Tishrei),
        "",
        [],
        LANG(u"Yom Kippur", DESC(u"יום הכפורים", u'יוה"כ')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_sukkot",
        (14, Months.Tishrei),
        "",
        [],
        LANG(u"Erev Sukkot", DESC(u"ערב סוכות", u"ערב סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "sukkot",
        (15, Months.Tishrei),
        "",
        [],
        LANG(u"Sukkot", DESC(u"סוכות", u"סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        (16, Months.Tishrei),
        "ISRAEL",
        "",
        LANG(u"Hol hamoed Sukkot", DESC(u"חול המועד סוכות", u'חוה"מ סוכות')),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        ([17, 18, 19, 20], Months.Tishrei),
        "",
        "",
        LANG(u"Hol hamoed Sukkot", DESC(u"חול המועד סוכות", u'חוה"מ סוכות')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "hoshana_raba",
        (21, Months.Tishrei),
        "",
        [],
        LANG(u"Hoshana Raba", DESC(u"הושענא רבה", u'הוש"ר')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "simchat_torah",
        (23, Months.Tishrei),
        "DIASPORA",
        [],
        LANG(u"Simchat Torah", DESC(u"שמחת תורה", u'שמח"ת')),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        (list(range(25, 30)), Months.Kislev),
        "",
        [],
        LANG(u"Chanukah", DESC(u"חנוכה", u"חנוכה")),
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
        LANG(u"Chanukah", DESC(u"חנוכה", u"חנוכה")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "asara_btevet",
        (10, Months.Tevet),
        "",
        [],
        LANG(u"Asara B'Tevet", DESC(u"צום עשרה בטבת", u"י' בטבת")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "tu_bshvat",
        (15, Months.Shvat),
        "",
        [],
        LANG(u"Tu B'Shvat", DESC(u'ט"ו בשבט', u'ט"ו בשבט')),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ([11, 13], [Months.Adar, Months.Adar_II]),
        "",
        [move_if_not_on_dow(13, 11, 5, 3)],
        LANG(u"Ta'anit Esther", DESC(u"תענית אסתר", u"תענית אסתר")),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        (14, [Months.Adar, Months.Adar_II]),
        "",
        [],
        LANG(u"Purim", DESC(u"פורים", u"פורים")),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        (15, [Months.Adar, Months.Adar_II]),
        "",
        [],
        LANG(u"Shushan Purim", DESC(u"שושן פורים", u"שושן פורים")),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_pesach",
        (14, Months.Nisan),
        "",
        [],
        LANG(u"Erev Pesach", DESC(u"ערב פסח", u"ערב פסח")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach",
        (15, Months.Nisan),
        "",
        "",
        LANG(u"Pesach", DESC(u"פסח", u"פסח")),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        (16, Months.Nisan),
        "ISRAEL",
        [],
        LANG(u"Hol hamoed Pesach", DESC(u"חול המועד פסח", u'חוה"מ פסח')),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        ([17, 18, 19], Months.Nisan),
        "",
        [],
        LANG(u"Hol hamoed Pesach", DESC(u"חול המועד פסח", u'חוה"מ פסח')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "hol_hamoed_pesach",
        (20, Months.Nisan),
        "",
        [],
        LANG(u"Hol hamoed Pesach", DESC(u"חול המועד פסח", u'חוה"מ פסח')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_vii",
        (21, Months.Nisan),
        "",
        [],
        LANG(u"Pesach VII", DESC(u"שביעי פסח", u"ז' פסח")),
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
        LANG(u"Yom HaAtzma'ut", DESC(u"יום העצמאות", u"יום העצמאות")),
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
        LANG(u"Yom HaAtzma'ut", DESC(u"יום העצמאות", u"יום העצמאות")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "lag_bomer",
        (18, Months.Iyyar),
        "",
        [],
        LANG(u"Lag B'Omer", DESC(u'ל"ג בעומר', u'ל"ג בעומר')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_shavuot",
        (5, Months.Sivan),
        "",
        [],
        LANG(u"Erev Shavuot", DESC(u"ערב שבועות", u"ערב שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shavuot",
        (6, Months.Sivan),
        "",
        [],
        LANG(u"Shavuot", DESC(u"שבועות", u"שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        ([17, 18], Months.Tammuz),
        "",
        [move_if_not_on_dow(17, 18, 5, 6)],
        LANG(u"Tzom Tammuz", DESC(u"צום שבעה עשר בתמוז", u"צום תמוז")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        ([9, 10], Months.Av),
        "",
        [move_if_not_on_dow(9, 10, 5, 6)],
        LANG(u"Tish'a B'Av", DESC(u"תשעה באב", u"ט' באב")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "tu_bav",
        (15, Months.Av),
        "",
        [],
        LANG(u"Tu B'Av", DESC(u'ט"ו באב', u'ט"ו באב')),
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
        LANG(u"Yom HaShoah", DESC(u"יום השואה", u"יום השואה")),
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
        LANG(u"Yom HaZikaron", DESC(u"יום הזכרון", u"יום הזכרון")),
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
        LANG(u"Yom HaZikaron", DESC(u"יום הזכרון", u"יום הזכרון")),
    ),
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_yerushalayim",
        (28, Months.Iyyar),
        "",
        [year_is_after(5727)],
        LANG(u"Yom Yerushalayim", DESC(u"יום ירושלים", u"יום י-ם")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shmini_atzeret",
        (22, Months.Tishrei),
        "",
        [],
        LANG(u"Shmini Atzeret", DESC(u"שמיני עצרת", u"שמיני עצרת")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_viii",
        (22, Months.Nisan),
        "DIASPORA",
        [],
        LANG(u"Pesach VIII", DESC(u"אחרון של פסח", u"אחרון של פסח")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shavuot_ii",
        (7, Months.Sivan),
        "DIASPORA",
        [],
        LANG(u"Shavuot II", DESC(u"שני של שבועות", u"ב' שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "sukkot_ii",
        (16, Months.Tishrei),
        "DIASPORA",
        [],
        LANG(u"Sukkot II", DESC(u"שני של סוכות", u"ב' סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_ii",
        (16, Months.Nisan),
        "DIASPORA",
        [],
        LANG(u"Pesach II", DESC(u"שני של פסח", u"ב' פסח")),
    ),
    HOLIDAY(
        HolidayTypes.ISRAEL_NATIONAL_HOLIDAY,
        "family_day",
        (30, Months.Shvat),
        "ISRAEL",
        [year_is_after(5734)],
        LANG(u"Family Day", DESC(u"יום המשפחה", u"יום המשפחה")),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "memorial_day_unknown",
        (7, [Months.Adar, Months.Adar_II]),
        "ISRAEL",
        [],
        LANG(
            u"Memorial day for fallen whose place of burial is unknown",
            DESC(u"יום זכרון...", u"יום זכרון..."),
        ),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        ([11, 12], Months.Marcheshvan),
        "ISRAEL",
        [move_if_not_on_dow(12, 11, 4, 3), year_is_after(5757)],
        LANG(
            u"Yitzhak Rabin memorial day",
            DESC(u"יום הזכרון ליצחק רבין", u"יום הזכרון ליצחק רבין"),
        ),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "zeev_zhabotinsky_day",
        (29, Months.Tammuz),
        "ISRAEL",
        [year_is_after(5764)],
        LANG(u"Zeev Zhabotinsky day", DESC(u"יום ז'בוטינסקי", u"יום ז'בוטינסקי")),
    ),
)

ZMAN = namedtuple("ZMAN", "zman, description")
ZMANIM = (
    ZMAN("first_light", LANG(u"Alot HaShachar", u"עלות השחר")),
    ZMAN("talit", LANG(u"Talit & Tefilin's time", u"זמן טלית ותפילין")),
    ZMAN("sunrise", LANG(u"Sunrise", u"הנץ החמה")),
    ZMAN("mga_end_shma", LANG(u'Shema EOT MG"A', u'סוף זמן ק"ש מג"א')),
    ZMAN("gra_end_shma", LANG(u'Shema EOT GR"A', u'סוף זמן ק"ש גר"א')),
    ZMAN("mga_end_tfila", LANG(u'Tefila EOT MG"A', u'סוף זמן תפילה מג"א')),
    ZMAN("gra_end_tfila", LANG(u'Tefila EOT GR"A', u'סוף זמן תפילה גר"א')),
    ZMAN("midday", LANG(u"Midday", u"חצות היום")),
    ZMAN("big_mincha", LANG(u"Big Mincha", u"מנחה גדולה")),
    ZMAN("small_mincha", LANG(u"Small Mincha", u"מנחה קטנה")),
    ZMAN("plag_mincha", LANG(u"Plag Mincha", u"פלג המנחה")),
    ZMAN("sunset", LANG(u"Sunset", u"שקיעה")),
    ZMAN("first_stars", LANG(u"First stars", u"צאת הכוכבים")),
    ZMAN("midnight", LANG(u"Midnight", u"חצות הלילה")),
)

# The first few cycles were only 2702 blatt. After that it became 2711. Even with
# that, the math doesn't play nicely with the dates before the 11th cycle :(
# From cycle 11 onwards, it was simple and sequential
DAF_YOMI_CYCLE_11_START = datetime.date(1997, 9, 29)
MESECHTA = namedtuple("MESECHTA", ["name", "pages"])
DAF_YOMI_MESECHTOS = (
    MESECHTA(LANG(u"Berachos", u"ברכות"), 63),
    MESECHTA(LANG(u"Shabbos", u"שבת"), 156),
    MESECHTA(LANG(u"Eruvin", u"עירובין"), 104),
    MESECHTA(LANG(u"Pesachim", u"פסחים"), 120),
    MESECHTA(LANG(u"Shekalim", u"שקלים"), 21),
    MESECHTA(LANG(u"Yoma", u"יומא"), 87),
    MESECHTA(LANG(u"Succah", u"סוכה"), 55),
    MESECHTA(LANG(u"Beitzah", u"ביצה"), 39),
    MESECHTA(LANG(u"Rosh Hashanah", u"ראש השנה"), 34),
    MESECHTA(LANG(u"Taanis", u"תענית"), 30),
    MESECHTA(LANG(u"Megillah", u"מגילה"), 31),
    MESECHTA(LANG(u"Moed Katan", u"מועד קטן"), 28),
    MESECHTA(LANG(u"Chagigah", u"חגיגה"), 26),
    MESECHTA(LANG(u"Yevamos", u"יבמות"), 121),
    MESECHTA(LANG(u"Kesubos", u"כתובות"), 111),
    MESECHTA(LANG(u"Nedarim", u"נדרים"), 90),
    MESECHTA(LANG(u"Nazir", u"נזיר"), 65),
    MESECHTA(LANG(u"Sotah", u"סוטה"), 48),
    MESECHTA(LANG(u"Gittin", u"גיטין"), 89),
    MESECHTA(LANG(u"Kiddushin", u"קידושין"), 81),
    MESECHTA(LANG(u"Bava Kamma", u"בבא קמא"), 118),
    MESECHTA(LANG(u"Bava Metzia", u"בבא מציעא"), 118),
    MESECHTA(LANG(u"Bava Basra", u"בבא בתרא"), 175),
    MESECHTA(LANG(u"Sanhedrin", u"סנהדרין"), 112),
    MESECHTA(LANG(u"Makkos", u"מכות"), 23),
    MESECHTA(LANG(u"Shevuos", u"שבועות"), 48),
    MESECHTA(LANG(u"Avodah Zarah", u"עבודה זרה"), 75),
    MESECHTA(LANG(u"Horayos", u"הוריות"), 13),
    MESECHTA(LANG(u"Zevachim", u"זבחים"), 119),
    MESECHTA(LANG(u"Menachos", u"מנחות"), 109),
    MESECHTA(LANG(u"Chullin", u"חולין"), 141),
    MESECHTA(LANG(u"Bechoros", u"בכורות"), 60),
    MESECHTA(LANG(u"Arachin", u"ערכין"), 33),
    MESECHTA(LANG(u"Temurah", u"תמורה"), 33),
    MESECHTA(LANG(u"Kereisos", u"כריתות"), 27),
    MESECHTA(LANG(u"Meilah", u"מעילה"), 36),
    MESECHTA(LANG(u"Niddah", u"נדה"), 72),
)

DAF_YOMI_TOTAL_PAGES = sum(mesechta.pages for mesechta in DAF_YOMI_MESECHTOS)
