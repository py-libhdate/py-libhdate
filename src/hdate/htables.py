# -*- coding: utf-8 -*-
"""Constant lookup tables for hdate modules."""

from collections import namedtuple

READING = namedtuple("READING", "year_type, readings")

READINGS = (
    READING([1725], (
        0, 53, 0, range(29), 0, range(29, 35), 0, range(35, 39), 59, 41, 60,
        range(44, 51), 61)),
    READING([1703], (
        0, 53, 0, range(29), 0, range(29, 42), 60, range(44, 51), 61)),
    READING([1523, 523], (
        53, 0, range(30), 0, range(30, 51), 61)),
    READING([1501, 501], (
        53, 0, range(30), 0, range(30, 51))),
    READING([1317, 1227], (
        52, 53, range(29), 0, 0, range(29, 42), 60, range(44, 51))),
    READING([1205], (
        52, 53, range(29), 0, range(29, 35), 0, range(35, 39), 59, 41, 60,
        range(44, 51), 61)),
    READING([521, 1521], (
        53, 0, range(26), 0, 26, 56, 57, 31, 58, range(34, 42), 60,
        range(44, 54))),
    READING([1225, 1315], (
        52, 53, range(22), 55, 24, 25, 0, 26, 56, 57, 31, 58, 34, 0,
        range(35, 39), 59, 41, 60, range(44, 51), 61)),
    READING([1701], (
        0, 53, 0, range(22), 55, 24, 25, 0, 26, 56, 57, 31, 58, range(34, 42),
        60, range(44, 52))),
    READING([1723], (
        0, 53, 0, range(22), 55, 24, 25, 0, 26, 56, 57, 31, 58, range(34, 42),
        60, range(44, 51), 61)),
    READING([1517], (
        53, 0, range(22), 55, 24, 25, 0, 0, 26, 56, 57, 31, 58, range(34, 42),
        60, range(44, 51))),
    READING([703, 725], (
        0, 53, 0, 54, range(1, 29), 0, range(29, 42), 60, range(44, 51), 61)),
    READING([317, 227], (
        52, 53, range(29), 0, range(29, 51))),
    READING([205], (
        52, 53, range(29), 0, range(29, 42), 60, range(44, 51), 61)),
    READING([701], (
        0, 53, 0, 54, range(1, 22), 55, 24, 25, 0, 26, 56, 57, 31, 58,
        range(34, 42), 60, range(44, 52))),
    READING([315, 203, 225, 1203], (
        52, 53, range(22), 55, 24, 25, 0, 26, 56, 57, 31, 58, range(34, 42),
        60, range(44, 51), 61)),
    READING([723], (
        0, 53, 0, 54, range(1, 22), 55, 24, 25, 0, 26, 56, 57, 31, 58,
        range(34, 42), 60, range(44, 51), 61)),
    READING([517], (
        53, 0, range(22), 55, 24, 25, 0, 26, 56, 57, range(31, 42), 60,
        range(44, 51)))
    )

DIGITS = (
    (u" ", u"א", u"ב", u"ג", u"ד", u"ה", u"ו", u"ז", u"ח", u"ט"),
    (u"ט", u"י", u"כ", u"ל", u"מ", u"נ", u"ס", u"ע", u"פ", u"צ"),
    (u" ", u"ק", u"ר", u"ש", u"ת")
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
    LANG(DESC(u"Saturday", u"Sat"), DESC(u"שבת", u"ז"))
    )

PARASHAOT = (
    LANG(u"none", u"none"), LANG(u"Bereshit", u"בראשית"),
    LANG(u"Noach", u"נח"), LANG(u"Lech-Lecha", u"לך לך"),
    LANG(u"Vayera", u"וירא"), LANG(u"Chayei Sara", u"חיי שרה"),
    LANG(u"Toldot", u"תולדות"), LANG(u"Vayetzei", u"ויצא"),
    LANG(u"Vayishlach", u"וישלח"), LANG(u"Vayeshev", u"וישב"),
    LANG(u"Miketz", u"מקץ"), LANG(u"Vayigash", u"ויגש"),
    LANG(u"Vayechi", u"ויחי"), LANG(u"Shemot", u"שמות"),
    LANG(u"Vaera", u"וארא"), LANG(u"Bo", u"בא"),
    LANG(u"Beshalach", u"בשלח"), LANG(u"Yitro", u"יתרו"),
    LANG(u"Mishpatim", u"משפטים"), LANG(u"Terumah", u"תרומה"),
    LANG(u"Tetzaveh", u"תצוה"), LANG(u"Ki Tisa", u"כי תשא"),
    LANG(u"Vayakhel", u"ויקהל"), LANG(u"Pekudei", u"פקודי"),
    LANG(u"Vayikra", u"ויקרא"), LANG(u"Tzav", u"צו"),
    LANG(u"Shmini", u"שמיני"), LANG(u"Tazria", u"תזריע"),
    LANG(u"Metzora", u"מצורע"), LANG(u"Achrei Mot", u"אחרי מות"),
    LANG(u"Kedoshim", u"קדושים"), LANG(u"Emor", u"אמור"),
    LANG(u"Behar", u"בהר"), LANG(u"Bechukotai", u"בחוקתי"),
    LANG(u"Bamidbar", u"במדבר"), LANG(u"Nasso", u"נשא"),
    LANG(u"Beha'alotcha", u"בהעלתך"), LANG(u"Sh'lach", u"שלח"),
    LANG(u"Korach", u"קרח"), LANG(u"Chukat", u"חקת"),
    LANG(u"Balak", u"בלק"), LANG(u"Pinchas", u"פנחס"),
    LANG(u"Matot", u"מטות"), LANG(u"Masei", u"מסעי"),
    LANG(u"Devarim", u"דברים"), LANG(u"Vaetchanan", u"ואתחנן"),
    LANG(u"Eikev", u"עקב"), LANG(u"Re'eh", u"ראה"),
    LANG(u"Shoftim", u"שופטים"), LANG(u"Ki Teitzei", u"כי תצא"),
    LANG(u"Ki Tavo", u"כי תבוא"), LANG(u"Nitzavim", u"נצבים"),
    LANG(u"Vayeilech", u"וילך"), LANG(u"Ha'Azinu", u"האזינו"),
    LANG(u"Vezot Habracha", u"וזאת הברכה"),
    LANG(u"Vayakhel-Pekudei", u"ויקהל-פקודי"),
    LANG(u"Tazria-Metzora", u"תזריע-מצורע"),
    LANG(u"Achrei Mot-Kedoshim", u"אחרי מות-קדושים"),
    LANG(u"Behar-Bechukotai", u"בהר-בחוקתי"),
    LANG(u"Chukat-Balak", u"חוקת-בלק"), LANG(u"Matot-Masei", u"מטות מסעי"),
    LANG(u"Nitzavim-Vayeilech", u"נצבים-וילך")
)

MONTHS = (
    LANG(u"Tishrei", u"תשרי"),
    LANG(u"Cheshvan", u"חשון"),
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
    LANG(u"Adar II", u"אדר ב")
    )


def year_is_after(year):
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is after the
    requested year.
    """
    return lambda x: x.h_year > year


def year_is_before(year):
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is before the
    requested year.
    """
    return lambda x: x.h_year < year


def move_if_not_on_dow(original, replacement, dow_not_orig, dow_replacement):
    """
    Return a lambda function.

    Lambda checks that either the original day does not fall on a given
    weekday, or that the replacement day does fall on the expected weekday.
    """
    return lambda x: (
        (x.h_day == original and x.gdate.weekday() != dow_not_orig) or
        (x.h_day == replacement and x.gdate.weekday() == dow_replacement))


HOLIDAY = namedtuple("HOLIDAY", [
    "index", "type", "name", "date", "israel_diaspora", "date_functions_list",
    "description"])

HOLIDAYS = (
    HOLIDAY(1, 1, "rosh_hashana_i", (1, 1), "", [],
            LANG(u"Rosh Hashana I", DESC(u"א' ראש השנה", u"א ר\"ה"))),
    HOLIDAY(2, 1, "rosh_hashana_ii", (2, 1), "", [],
            LANG(u"Rosh Hashana II", DESC(u"ב' ראש השנה", u"ב' ר\"ה"))),
    HOLIDAY(3, 5, "tzom_gedaliah", ([3, 4], 1), "",
            [move_if_not_on_dow(3, 4, 5, 6)],
            LANG(u"Tzom Gedaliah", DESC(u"צום גדליה", u"צום גדליה"))),
    HOLIDAY(4, 1, "yom_kippur", (10, 1), "", [],
            LANG(u"Yom Kippur", DESC(u"יום הכפורים", u"יוה\"כ"))),
    HOLIDAY(5, 1, "sukkot", (15, 1), "", [],
            LANG(u"Sukkot", DESC(u"סוכות", u"סוכות"))),
    HOLIDAY(6, 3, "hol_hamoed_sukkot", (16, 1), "ISRAEL", "",
            LANG(u"Hol hamoed Sukkot",
                 DESC(u"חול המועד סוכות", u"חוה\"מ סוכות"))),
    HOLIDAY(6, 3, "hol_hamoed_sukkot", ([17, 18, 19, 20], 1), "", "",
            LANG(u"Hol hamoed Sukkot",
                 DESC(u"חול המועד סוכות", u"חוה\"מ סוכות"))),
    HOLIDAY(7, 3, "hoshana_raba", (21, 1), "", [],
            LANG(u"Hoshana Raba", DESC(u"הושענא רבה", u"הוש\"ר"))),
    HOLIDAY(8, 1, "simchat_torah", (23, 1), "DIASPORA", [],
            LANG(u"Simchat Torah", DESC(u"שמחת תורה", u"שמח\"ת"))),
    HOLIDAY(9, 4, "chanukah", (list(range(25, 30)), 3), "", [],
            LANG(u"Chanukah", DESC(u"חנוכה", u"חנוכה"))),
    HOLIDAY(9, 4, "chanukah", ([1, 2, 3], 4), "",
            [lambda x: (
                (x.short_kislev() and x.h_day == 3) or
                (x.h_day in [1, 2]))],
            LANG(u"Chanukah", DESC(u"חנוכה", u"חנוכה"))),
    HOLIDAY(10, 5, "asara_btevet", (10, 4), "", [],
            LANG(u"Asara B'Tevet", DESC(u"צום עשרה בטבת", u"י' בטבת"))),
    HOLIDAY(11, 7, "tu_bshvat", (15, 5), "", [],
            LANG(u"Tu B'Shvat", DESC(u"ט\"ו בשבט", u"ט\"ו בשבט"))),
    HOLIDAY(12, 5, "taanit_esther", ([11, 13], [6, 14]), "",
            [move_if_not_on_dow(13, 11, 5, 3)],
            LANG(u"Ta'anit Esther", DESC(u"תענית אסתר", u"תענית אסתר"))),
    HOLIDAY(13, 4, "purim", (14, [6, 14]), "", [],
            LANG(u"Purim", DESC(u"פורים", u"פורים"))),
    HOLIDAY(14, 4, "shushan_purim", (15, [6, 14]), "", [],
            LANG(u"Shushan Purim", DESC(u"שושן פורים", u"שושן פורים"))),
    HOLIDAY(15, 1, "pesach", (15, 7), "", "",
            LANG(u"Pesach", DESC(u"פסח", u"פסח"))),
    HOLIDAY(16, 3, "hol_hamoed_pesach", (16, 7), "ISRAEL", [],
            LANG(u"Hol hamoed Pesach",
                 DESC(u"חול המועד פסח", u"חוה\"מ פסח"))),
    HOLIDAY(16, 3, "hol_hamoed_pesach", ([17, 18, 19, 20], 7), "", [],
            LANG(u"Hol hamoed Pesach",
                 DESC(u"חול המועד פסח", u"חוה\"מ פסח"))),
    HOLIDAY(17, 6, "yom haatzmaut", ([3, 4, 5], 8), "",
            [year_is_after(5708), year_is_before(5764),
             move_if_not_on_dow(5, 4, 4, 3) or
             move_if_not_on_dow(5, 3, 5, 3)],
            LANG(u"Yom HaAtzma'ut", DESC(u"יום העצמאות", u"יום העצמאות"))),
    HOLIDAY(17, 6, "yom haatzmaut", ([3, 4, 5, 6], 8), "",
            [year_is_after(5763),
             move_if_not_on_dow(5, 4, 4, 3) or
             move_if_not_on_dow(5, 3, 5, 3) or
             move_if_not_on_dow(5, 6, 0, 1)],
            LANG(u"Yom HaAtzma'ut", DESC(u"יום העצמאות", u"יום העצמאות"))),
    HOLIDAY(18, 7, "lag_bomer", (18, 8), "", [],
            LANG(u"Lag B'Omer", DESC(u"ל\"ג בעומר", u"ל\"ג בעומר"))),
    HOLIDAY(19, 9, "erev_shavuot", (5, 9), "", [],
            LANG(u"Erev Shavuot", DESC(u"ערב שבועות", u"ערב שבועות"))),
    HOLIDAY(20, 1, "shavuot", (6, 9), "", [],
            LANG(u"Shavuot", DESC(u"שבועות", u"שבועות"))),
    HOLIDAY(21, 5, "tzom_tammuz", ([17, 18], 10), "",
            [move_if_not_on_dow(17, 18, 5, 6)],
            LANG(u"Tzom Tammuz", DESC(u"צום שבעה עשר בתמוז", u"צום תמוז"))),
    HOLIDAY(22, 5, "tisha_bav", ([9, 10], 11), "",
            [move_if_not_on_dow(9, 10, 5, 6)],
            LANG(u"Tish'a B'Av", DESC(u"תשעה באב", u"ט' באב"))),
    HOLIDAY(23, 7, "tu_bav", (15, 11), "", [],
            LANG(u"Tu B'Av", DESC(u"ט\"ו באב", u"ט\"ו באב"))),
    HOLIDAY(24, 8, "yom_hashoah", ([26, 27, 28], 7), "",
            [move_if_not_on_dow(27, 28, 6, 0) or
             move_if_not_on_dow(27, 26, 4, 3),
             year_is_after(5718)],
            LANG(u"Yom HaShoah", DESC(u"יום השואה", u"יום השואה"))),
    HOLIDAY(25, 8, "yom_hazikaron", ([2, 3, 4], 8), "",
            [year_is_after(5708), year_is_before(5764),
             move_if_not_on_dow(4, 3, 3, 2) or
             move_if_not_on_dow(4, 2, 4, 2)],
            LANG(u"Yom HaZikaron", DESC(u"יום הזכרון", u"יום הזכרון"))),
    HOLIDAY(25, 8, "yom_hazikaron", ([2, 3, 4, 5], 8), "",
            [year_is_after(5763),
             move_if_not_on_dow(4, 3, 3, 2) or
             move_if_not_on_dow(4, 2, 4, 2) or
             move_if_not_on_dow(4, 5, 6, 0)],
            LANG(u"Yom HaZikaron", DESC(u"יום הזכרון", u"יום הזכרון"))),
    HOLIDAY(26, 6, "yom_yerushalayim", (28, 8), "", [year_is_after(5727)],
            LANG(u"Yom Yerushalayim", DESC(u"יום ירושלים", u"יום י-ם"))),
    HOLIDAY(27, 1, "shmini_atzeret", (22, 1), "", [],
            LANG(u"Shmini Atzeret", DESC(u"שמיני עצרת", u"שמיני עצרת"))),
    HOLIDAY(28, 1, "pesach_vii", (21, 7), "", [],
            LANG(u"Pesach VII", DESC(u"שביעי פסח", u"ז' פסח"))),
    HOLIDAY(29, 1, "pesach_viii", (22, 7), "DIASPORA", [],
            LANG(u"Pesach VIII", DESC(u"אחרון של פסח", u"אחרון של פסח"))),
    HOLIDAY(30, 1, "shavuot_ii", (7, 9), "DIASPORA", [],
            LANG(u"Shavuot II", DESC(u"שני של שבועות", u"ב' שבועות"))),
    HOLIDAY(31, 1, "sukkot_ii", (16, 1), "DIASPORA", [],
            LANG(u"Sukkot II", DESC(u"שני של סוכות", u"ב' סוכות"))),
    HOLIDAY(32, 1, "pesach_ii", (16, 7), "DIASPORA", [],
            LANG(u"Pesach II", DESC(u"שני של פסח", u"ב' פסח"))),
    HOLIDAY(33, 9, "family_day", (30, 5), "ISRAEL", [],
            LANG(u"Family Day", DESC(u"יום המשפחה", u"יום המשפחה"))),
    HOLIDAY(34, 9, "memorial_day_unknown", (7, [6, 14]), "ISRAEL", [],
            LANG(u"Memorial day for fallen whose place of burial is unknown",
                 DESC(u"יום זכרון...", u"יום זכרון..."))),
    HOLIDAY(35, 9, "rabin_memorial_day", ([11, 12], 2), "ISRAEL",
            [move_if_not_on_dow(12, 11, 4, 3), year_is_after(5757)],
            LANG(u"Yitzhak Rabin memorial day",
                 DESC(u"יום הזכרון ליצחק רבין", u"יום הזכרון ליצחק רבין"))),
    HOLIDAY(36, 9, "zeev_zhabotinsky_day", (29, 10), "ISRAEL",
            [year_is_after(5764)],
            LANG(u"Zeev Zhabotinsky day",
                 DESC(u"יום ז\'בוטינסקי", u"יום ז\'בוטינסקי"))),
    HOLIDAY(37, 2, "erev_yom_kippur", (9, 1), "", [],
            LANG(u"Erev Yom Kippur", DESC(u"עיוה\"כ", u"עיוה\"כ")))
    )

ZMAN = namedtuple('ZMAN', 'zman, description')
ZMANIM = (
    ZMAN("first_light", LANG(u"Alot HaShachar", u"עלות השחר")),
    ZMAN("talit", LANG(u"Talit & Tefilin's time", u"זמן טלית ותפילין")),
    ZMAN("sunrise", LANG(u"Sunrise", u"הנץ החמה")),
    ZMAN("sunset", LANG(u"Sunset", u"שקיעה")),
    ZMAN("first_stars", LANG(u"First stars", u"צאת הככבים")),
    ZMAN("plag_mincha", LANG(u"Plag Mincha", u"פלג מנחה")),
    ZMAN("big_mincha", LANG(u"Big Mincha", u"מנחה גדולה")),
    ZMAN("small_mincha", LANG(u"Small Mincha", u"מנחה קטנה")),
    ZMAN("mga_end_shma", LANG(u"Shema EOT MG\"A", u"סוף זמן ק\"ש מג\"א")),
    ZMAN("gra_end_shma", LANG(u"Shema EOT GR\"A", u"סוף זמן ק\"ש הגר\"א")),
    ZMAN("mga_end_tfila", LANG(u"Tefila EOT MG\"A", u"סוף זמן תפילה מג\"א")),
    ZMAN("gra_end_tfila", LANG(u"Tefila EOT GR\"A", u"סוף זמן תפילה גר\"א")),
    ZMAN("midnight", LANG(u"Midnight", u"חצות הלילה")),
    ZMAN("midday", LANG(u"Midday", u"חצות היום"))
    )
