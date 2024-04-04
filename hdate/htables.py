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


def correct_adar():
    """
    Return a lambda function.

    Lambda checks that the value of the month returned is correct depending on whether
    it's a leap year.
    """
    return lambda x: (
        (x.hdate.month == Months.ADAR and not x.is_leap_year)
        or (x.hdate.month in [Months.ADAR_I, Months.ADAR_II] and x.is_leap_year)
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
    HOLIDAY(HolidayTypes.UNKNOWN, "", (), "", [], LANG("", "", DESC("", ""))),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_rosh_hashana",
        (29, Months.ELUL),
        "",
        [],
        LANG(
            "Veille de Rosh Hashana",
            "Erev Rosh Hashana",
            DESC("ערב ראש השנה", 'ערב ר"ה'),
        ),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "rosh_hashana_i",
        (1, Months.TISHREI),
        "",
        [],
        LANG("Rosh Hashana I", "Rosh Hashana I", DESC("א' ראש השנה", 'א ר"ה')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "rosh_hashana_ii",
        (2, Months.TISHREI),
        "",
        [],
        LANG("Rosh Hashana II", "Rosh Hashana II", DESC("ב' ראש השנה", "ב' ר\"ה")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        ([3, 4], Months.TISHREI),
        "",
        [move_if_not_on_dow(3, 4, 5, 6)],
        LANG("Jeûne de Guedalia", "Tzom Gedaliah", DESC("צום גדליה", "צום גדליה")),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_yom_kippur",
        (9, Months.TISHREI),
        "",
        [],
        LANG("Veille de Yom Kipour", "Erev Yom Kippur", DESC('עיוה"כ', 'עיוה"כ')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "yom_kippur",
        (10, Months.TISHREI),
        "",
        [],
        LANG("Yom Kipour", "Yom Kippur", DESC("יום הכפורים", 'יוה"כ')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_sukkot",
        (14, Months.TISHREI),
        "",
        [],
        LANG("Veille de Souccot", "Erev Sukkot", DESC("ערב סוכות", "ערב סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "sukkot",
        (15, Months.TISHREI),
        "",
        [],
        LANG("Souccot", "Sukkot", DESC("סוכות", "סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        (16, Months.TISHREI),
        "ISRAEL",
        "",
        LANG(
            "Hol hamoed Souccot",
            "Hol hamoed Sukkot",
            DESC("חול המועד סוכות", 'חוה"מ סוכות'),
        ),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_sukkot",
        ([17, 18, 19, 20], Months.TISHREI),
        "",
        "",
        LANG(
            "Hol hamoed Souccot",
            "Hol hamoed Sukkot",
            DESC("חול המועד סוכות", 'חוה"מ סוכות'),
        ),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "hoshana_raba",
        (21, Months.TISHREI),
        "",
        [],
        LANG("Hoshaâna Rabba", "Hoshana Raba", DESC("הושענא רבה", 'הוש"ר')),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "simchat_torah",
        (23, Months.TISHREI),
        "DIASPORA",
        [],
        LANG("Simhat Torah", "Simchat Torah", DESC("שמחת תורה", 'שמח"ת')),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        (list(range(25, 30)), Months.KISLEV),
        "",
        [],
        LANG("Hanouka", "Chanukah", DESC("חנוכה", "חנוכה")),
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
        LANG("Hanouka", "Chanukah", DESC("חנוכה", "חנוכה")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "asara_btevet",
        (10, Months.TEVET),
        "",
        [],
        LANG("10 Tevet", "Asara B'Tevet", DESC("צום עשרה בטבת", "י' בטבת")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "tu_bshvat",
        (15, Months.SHVAT),
        "",
        [],
        LANG("Tou Bi Shvat", "Tu B'Shvat", DESC('ט"ו בשבט', 'ט"ו בשבט')),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ([11, 13], [Months.ADAR, Months.ADAR_II]),
        "",
        [move_if_not_on_dow(13, 11, 5, 3), correct_adar()],
        LANG("Jeûne d'Esther", "Ta'anit Esther", DESC("תענית אסתר", "תענית אסתר")),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        (14, [Months.ADAR, Months.ADAR_II]),
        "",
        [correct_adar()],
        LANG("Pourim", "Purim", DESC("פורים", "פורים")),
    ),
    HOLIDAY(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        (15, [Months.ADAR, Months.ADAR_II]),
        "",
        [correct_adar()],
        LANG("Pourim Shoushan", "Shushan Purim", DESC("שושן פורים", "שושן פורים")),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_pesach",
        (14, Months.NISAN),
        "",
        [],
        LANG("Veille de Pessah", "Erev Pesach", DESC("ערב פסח", "ערב פסח")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach",
        (15, Months.NISAN),
        "",
        "",
        LANG("Pessah", "Pesach", DESC("פסח", "פסח")),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        (16, Months.NISAN),
        "ISRAEL",
        [],
        LANG(
            "Hol hamoed Pessah", "Hol hamoed Pesach", DESC("חול המועד פסח", 'חוה"מ פסח')
        ),
    ),
    HOLIDAY(
        HolidayTypes.HOL_HAMOED,
        "hol_hamoed_pesach",
        ([17, 18, 19], Months.NISAN),
        "",
        [],
        LANG(
            "Hol hamoed Pessah", "Hol hamoed Pesach", DESC("חול המועד פסח", 'חוה"מ פסח')
        ),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "hol_hamoed_pesach",
        (20, Months.NISAN),
        "",
        [],
        LANG(
            "Hol hamoed Pessah", "Hol hamoed Pesach", DESC("חול המועד פסח", 'חוה"מ פסח')
        ),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_vii",
        (21, Months.NISAN),
        "",
        [],
        LANG("Pessah VII", "Pesach VII", DESC("שביעי פסח", "ז' פסח")),
    ),
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ([3, 4, 5], Months.IYYAR),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(5, 4, 4, 3) or move_if_not_on_dow(5, 3, 5, 3),
        ],
        LANG("Yom HaAtsmaout", "Yom HaAtzma'ut", DESC("יום העצמאות", "יום העצמאות")),
    ),
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ([3, 4, 5, 6], Months.IYYAR),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(5, 4, 4, 3)
            or move_if_not_on_dow(5, 3, 5, 3)
            or move_if_not_on_dow(5, 6, 0, 1),
        ],
        LANG("Yom HaAtsmaout", "Yom HaAtzma'ut", DESC("יום העצמאות", "יום העצמאות")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "lag_bomer",
        (18, Months.IYYAR),
        "",
        [],
        LANG("Lag Ba Omer", "Lag B'Omer", DESC('ל"ג בעומר', 'ל"ג בעומר')),
    ),
    HOLIDAY(
        HolidayTypes.EREV_YOM_TOV,
        "erev_shavuot",
        (5, Months.SIVAN),
        "",
        [],
        LANG("Veille de Shavouot", "Erev Shavuot", DESC("ערב שבועות", "ערב שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shavuot",
        (6, Months.SIVAN),
        "",
        [],
        LANG("Shavouot", "Shavuot", DESC("שבועות", "שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        ([17, 18], Months.TAMMUZ),
        "",
        [move_if_not_on_dow(17, 18, 5, 6)],
        LANG(
            "Jeûne du 17 Tamouz", "Tzom Tammuz", DESC("צום שבעה עשר בתמוז", "צום תמוז")
        ),
    ),
    HOLIDAY(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        ([9, 10], Months.AV),
        "",
        [move_if_not_on_dow(9, 10, 5, 6)],
        LANG("Tisha Be'Av", "Tish'a B'Av", DESC("תשעה באב", "ט' באב")),
    ),
    HOLIDAY(
        HolidayTypes.MINOR_HOLIDAY,
        "tu_bav",
        (15, Months.AV),
        "",
        [],
        LANG("Tou be'Av", "Tu B'Av", DESC('ט"ו באב', 'ט"ו באב')),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hashoah",
        ([26, 27, 28], Months.NISAN),
        "",
        [
            move_if_not_on_dow(27, 28, 6, 0) or move_if_not_on_dow(27, 26, 4, 3),
            year_is_after(5718),
        ],
        LANG("Yom HaShoah", "Yom HaShoah", DESC("יום השואה", "יום השואה")),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ([2, 3, 4], Months.IYYAR),
        "",
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(4, 3, 3, 2) or move_if_not_on_dow(4, 2, 4, 2),
        ],
        LANG("Yom haZicaron", "Yom HaZikaron", DESC("יום הזכרון", "יום הזכרון")),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ([2, 3, 4, 5], Months.IYYAR),
        "",
        [
            year_is_after(5763),
            move_if_not_on_dow(4, 3, 3, 2)
            or move_if_not_on_dow(4, 2, 4, 2)
            or move_if_not_on_dow(4, 5, 6, 0),
        ],
        LANG("Yom haZicaron", "Yom HaZikaron", DESC("יום הזכרון", "יום הזכרון")),
    ),
    HOLIDAY(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_yerushalayim",
        (28, Months.IYYAR),
        "",
        [year_is_after(5727)],
        LANG("Yom Yeroushalaïm", "Yom Yerushalayim", DESC("יום ירושלים", "יום י-ם")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shmini_atzeret",
        (22, Months.TISHREI),
        "",
        [],
        LANG("Shemini Atseret", "Shmini Atzeret", DESC("שמיני עצרת", "שמיני עצרת")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_viii",
        (22, Months.NISAN),
        "DIASPORA",
        [],
        LANG("Pessah VIII", "Pesach VIII", DESC("אחרון של פסח", "אחרון של פסח")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "shavuot_ii",
        (7, Months.SIVAN),
        "DIASPORA",
        [],
        LANG("Shavouot II", "Shavuot II", DESC("שני של שבועות", "ב' שבועות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "sukkot_ii",
        (16, Months.TISHREI),
        "DIASPORA",
        [],
        LANG("Souccot II", "Sukkot II", DESC("שני של סוכות", "ב' סוכות")),
    ),
    HOLIDAY(
        HolidayTypes.YOM_TOV,
        "pesach_ii",
        (16, Months.NISAN),
        "DIASPORA",
        [],
        LANG("Pessah II", "Pesach II", DESC("שני של פסח", "ב' פסח")),
    ),
    HOLIDAY(
        HolidayTypes.ISRAEL_NATIONAL_HOLIDAY,
        "family_day",
        (30, Months.SHVAT),
        "ISRAEL",
        [year_is_after(5734)],
        LANG("Family Day", "Family Day", DESC("יום המשפחה", "יום המשפחה")),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "memorial_day_unknown",
        (7, [Months.ADAR, Months.ADAR_II]),
        "ISRAEL",
        [correct_adar()],
        LANG(
            "Jour du souvenir",
            "Memorial day for fallen whose place of burial is unknown",
            DESC("יום זכרון...", "יום זכרון..."),
        ),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        ([11, 12], Months.MARCHESHVAN),
        "ISRAEL",
        [move_if_not_on_dow(12, 11, 4, 3), year_is_after(5757)],
        LANG(
            "Yitzhak Rabin memorial day",
            "Yitzhak Rabin memorial day",
            DESC("יום הזכרון ליצחק רבין", "יום הזכרון ליצחק רבין"),
        ),
    ),
    HOLIDAY(
        HolidayTypes.MEMORIAL_DAY,
        "zeev_zhabotinsky_day",
        (29, Months.TAMMUZ),
        "ISRAEL",
        [year_is_after(5764)],
        LANG(
            "Zeev Zhabotinsky day",
            "Zeev Zhabotinsky day",
            DESC("יום ז'בוטינסקי", "יום ז'בוטינסקי"),
        ),
    ),
)

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
    ZMAN("small_mincha", LANG("Minha Qetana", "Small Mincha", "מנחה קטנה")),
    ZMAN("plag_mincha", LANG("Plag haMinha", "Plag Mincha", "פלג המנחה")),
    ZMAN("sunset", LANG("Shqiat", "Sunset", "שקיעה")),
    ZMAN("first_stars", LANG("Tzeit haCokhavim", "First stars", "צאת הכוכבים")),
    ZMAN("midnight", LANG("Hatsot laïla", "Midnight", "חצות הלילה")),
)

# The first few cycles were only 2702 blatt. After that it became 2711. Even with
# that, the math doesn't play nicely with the dates before the 11th cycle :(
# From cycle 11 onwards, it was simple and sequential
DAF_YOMI_CYCLE_11_START = datetime.date(1997, 9, 29)
MESECHTA = namedtuple("MESECHTA", ["name", "pages"])
DAF_YOMI_MESECHTOS = (
    MESECHTA(LANG("Berachos", "Berachos", "ברכות"), 63),
    MESECHTA(LANG("Shabbos", "Shabbos", "שבת"), 156),
    MESECHTA(LANG("Eruvin", "Eruvin", "עירובין"), 104),
    MESECHTA(LANG("Pesachim", "Pesachim", "פסחים"), 120),
    MESECHTA(LANG("Shekalim", "Shekalim", "שקלים"), 21),
    MESECHTA(LANG("Yoma", "Yoma", "יומא"), 87),
    MESECHTA(LANG("Succah", "Succah", "סוכה"), 55),
    MESECHTA(LANG("Beitzah", "Beitzah", "ביצה"), 39),
    MESECHTA(LANG("Rosh Hashanah", "Rosh Hashanah", "ראש השנה"), 34),
    MESECHTA(LANG("Taanis", "Taanis", "תענית"), 30),
    MESECHTA(LANG("Megillah", "Megillah", "מגילה"), 31),
    MESECHTA(LANG("Moed Katan", "Moed Katan", "מועד קטן"), 28),
    MESECHTA(LANG("Chagigah", "Chagigah", "חגיגה"), 26),
    MESECHTA(LANG("Yevamos", "Yevamos", "יבמות"), 121),
    MESECHTA(LANG("Kesubos", "Kesubos", "כתובות"), 111),
    MESECHTA(LANG("Nedarim", "Nedarim", "נדרים"), 90),
    MESECHTA(LANG("Nazir", "Nazir", "נזיר"), 65),
    MESECHTA(LANG("Sotah", "Sotah", "סוטה"), 48),
    MESECHTA(LANG("Gittin", "Gittin", "גיטין"), 89),
    MESECHTA(LANG("Kiddushin", "Kiddushin", "קידושין"), 81),
    MESECHTA(LANG("Bava Kamma", "Bava Kamma", "בבא קמא"), 118),
    MESECHTA(LANG("Bava Metzia", "Bava Metzia", "בבא מציעא"), 118),
    MESECHTA(LANG("Bava Basra", "Bava Basra", "בבא בתרא"), 175),
    MESECHTA(LANG("Sanhedrin", "Sanhedrin", "סנהדרין"), 112),
    MESECHTA(LANG("Makkos", "Makkos", "מכות"), 23),
    MESECHTA(LANG("Shevuos", "Shevuos", "שבועות"), 48),
    MESECHTA(LANG("Avodah Zarah", "Avodah Zarah", "עבודה זרה"), 75),
    MESECHTA(LANG("Horayos", "Horayos", "הוריות"), 13),
    MESECHTA(LANG("Zevachim", "Zevachim", "זבחים"), 119),
    MESECHTA(LANG("Menachos", "Menachos", "מנחות"), 109),
    MESECHTA(LANG("Chullin", "Chullin", "חולין"), 141),
    MESECHTA(LANG("Bechoros", "Bechoros", "בכורות"), 60),
    MESECHTA(LANG("Arachin", "Arachin", "ערכין"), 33),
    MESECHTA(LANG("Temurah", "Temurah", "תמורה"), 33),
    MESECHTA(LANG("Kereisos", "Kereisos", "כריתות"), 27),
    MESECHTA(LANG("Meilah", "Meilah", "מעילה"), 36),
    MESECHTA(LANG("Niddah", "Niddah", "נדה"), 72),
)

DAF_YOMI_TOTAL_PAGES = sum(mesechta.pages for mesechta in DAF_YOMI_MESECHTOS)
