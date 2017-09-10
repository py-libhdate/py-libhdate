# -*- coding: utf-8 -*-
"""Constant lookup tables for hdate modules."""

# holydays table
HOLYDAYS_TABLE = [
    [  # Tishrey
        1, 2, 3, 3, 0, 0, 0, 0, 37, 4,
        0, 0, 0, 0, 5, 31, 6, 6, 6, 6,
        7, 27, 8, 0, 0, 0, 0, 0, 0, 0],
    [  # Heshvan
        0, 0, 0, 0, 0, 0, 0, 0, 0, 35,
        35, 35, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # Kislev
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 9, 9, 9, 9, 9, 9],
    [  # Tevet
        9, 9, 9, 0, 0, 0, 0, 0, 0, 10,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # Shvat
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 11, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 33],
    [  # Adar
        0, 0, 0, 0, 0, 0, 34, 0, 0, 0,
        12, 0, 12, 13, 14, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # Nisan
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 15, 32, 16, 16, 16, 16,
        28, 29, 0, 0, 0, 24, 24, 24, 0, 0],
    [  # Iyar
        0, 17, 17, 17, 17, 17, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 18, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 26, 0, 0],
    [  # Sivan
        0, 0, 0, 0, 19, 20, 30, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # Tamuz
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 21, 21, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 36, 0],
    [  # Av
        0, 0, 0, 0, 0, 0, 0, 0, 22, 22,
        0, 0, 0, 0, 23, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # Elul
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # Adar 1
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # Adar 2
        0, 0, 0, 0, 0, 0, 34, 0, 0, 0,
        12, 0, 12, 13, 14, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Joined Parash flags
JOIN_FLAGS = [
    [
        [1, 1, 1, 1, 0, 1, 1],  # 1 be erez israel
        [1, 1, 1, 1, 0, 1, 0],  # 2
        [1, 1, 1, 1, 0, 1, 1],  # 3
        [1, 1, 1, 0, 0, 1, 0],  # 4
        [1, 1, 1, 1, 0, 1, 1],  # 5
        [0, 1, 1, 1, 0, 1, 0],  # 6
        [1, 1, 1, 1, 0, 1, 1],  # 7
        [0, 0, 0, 0, 0, 1, 1],  # 8
        [0, 0, 0, 0, 0, 0, 0],  # 9
        [0, 0, 0, 0, 0, 1, 1],  # 10
        [0, 0, 0, 0, 0, 0, 0],  # 11
        [0, 0, 0, 0, 0, 0, 0],  # 12
        [0, 0, 0, 0, 0, 0, 1],  # 13
        [0, 0, 0, 0, 0, 1, 1]   # 14
    ],
    [
        [1, 1, 1, 1, 0, 1, 1],  # 1 in diaspora
        [1, 1, 1, 1, 0, 1, 0],  # 2
        [1, 1, 1, 1, 1, 1, 1],  # 3
        [1, 1, 1, 1, 0, 1, 0],  # 4
        [1, 1, 1, 1, 1, 1, 1],  # 5
        [0, 1, 1, 1, 0, 1, 0],  # 6
        [1, 1, 1, 1, 0, 1, 1],  # 7
        [0, 0, 0, 0, 1, 1, 1],  # 8
        [0, 0, 0, 0, 0, 0, 0],  # 9
        [0, 0, 0, 0, 0, 1, 1],  # 10
        [0, 0, 0, 0, 0, 1, 0],  # 11
        [0, 0, 0, 0, 0, 1, 0],  # 12
        [0, 0, 0, 0, 0, 0, 1],  # 13
        [0, 0, 0, 0, 1, 1, 1]   # 14
    ]
]

DIGITS = [
    [u" ", u"א", u"ב", u"ג", u"ד", u"ה", u"ו", u"ז", u"ח", u"ט"],
    [u"ט", u"י", u"כ", u"ל", u"מ", u"נ", u"ס", u"ע", u"פ", u"צ"],
    [u" ", u"ק", u"ר", u"ש", u"ת"]
]

DAYS_TABLE = [
    [   # begin english long
        [u"Sunday", u"Monday", u"Tuesday", u"Wednesday", u"Thursday",
         u"Friday", u"Saturday"],
        # begin english short
        [u"Sun", u"Mon", u"Tue", u"Wed", u"Thu", u"Fri", u"Sat"],
    ],
    [   # begin hebrew long
        [u"ראשון", u"שני", u"שלישי", u"רביעי", u"חמישי", u"שישי", u"שבת"],
        # begin hebrew short
        [u"א", u"ב", u"ג", u"ד", u"ה", u"ו", u"ש"]
    ]
]

PARASHAOT = [
    [  # begin english
        u"none", u"Bereshit", u"Noach",
        u"Lech-Lecha", u"Vayera", u"Chayei Sara",
        u"Toldot", u"Vayetzei", u"Vayishlach",
        u"Vayeshev", u"Miketz", u"Vayigash",     # 11
        u"Vayechi", u"Shemot", u"Vaera",
        u"Bo", u"Beshalach", u"Yitro",
        u"Mishpatim", u"Terumah", u"Tetzaveh",     # 20
        u"Ki Tisa", u"Vayakhel", u"Pekudei",
        u"Vayikra", u"Tzav", u"Shmini",
        u"Tazria", u"Metzora", u"Achrei Mot",
        u"Kedoshim", u"Emor", u"Behar",        # 32
        u"Bechukotai", u"Bamidbar", u"Nasso",
        u"Beha'alotcha", u"Sh'lach", u"Korach",
        u"Chukat", u"Balak", u"Pinchas",      # 41
        u"Matot", u"Masei", u"Devarim",
        u"Vaetchanan", u"Eikev", u"Re'eh",
        u"Shoftim", u"Ki Teitzei", u"Ki Tavo",      # 50
        u"Nitzavim", u"Vayeilech", u"Ha'Azinu",
        u"Vezot Habracha",                             # 54
        u"Vayakhel-Pekudei", u"Tazria-Metzora", u"Achrei Mot-Kedoshim",
        u"Behar-Bechukotai", u"Chukat-Balak", u"Matot-Masei",
        u"Nitzavim-Vayeilech"],
    [     # begin hebrew
        u"none", u"בראשית", u"נח",
        u"לך לך", u"וירא", u"חיי שרה",
        u"תולדות", u"ויצא", u"וישלח",
        u"וישב", u"מקץ", u"ויגש",  # 11
        u"ויחי", u"שמות", u"וארא",
        u"בא", u"בשלח", u"יתרו",
        u"משפטים", u"תרומה", u"תצוה",  # 20
        u"כי תשא", u"ויקהל", u"פקודי",
        u"ויקרא", u"צו", u"שמיני",
        u"תזריע", u"מצורע", u"אחרי מות",
        u"קדושים", u"אמור", u"בהר",  # 32
        u"בחוקתי", u"במדבר", u"נשא",
        u"בהעלתך", u"שלח", u"קרח",
        u"חקת", u"בלק", u"פנחס",  # 41
        u"מטות", u"מסעי", u"דברים",
        u"ואתחנן", u"עקב", u"ראה",
        u"שופטים", u"כי תצא", u"כי תבוא",  # 50
        u"נצבים", u"וילך", u"האזינו",
        u"וזאת הברכה",  # 54
        u"ויקהל-פקודי", u"תזריע-מצורע", u"אחרי מות-קדושים",
        u"בהר-בחוקתי", u"חוקת-בלק", u"מטות מסעי",
        u"נצבים-וילך"]
]

HEBREW_MONTHS = [
    [  # begin english
        u"Tishrei", u"Cheshvan", u"Kislev", u"Tevet",
        u"Sh'vat", u"Adar", u"Nisan", u"Iyyar",
        u"Sivan", u"Tammuz", u"Av", u"Elul", u"Adar I",
        u"Adar II"
    ],
    [  # begin hebrew
        u"תשרי", u"חשון", u"כסלו", u"טבת", u"שבט", u"אדר", u"ניסן", u"אייר",
        u"סיון", u"תמוז", u"אב", u"אלול", u"אדר א", u"אדר ב"
    ]
]

GREGORIAN_MONTHS = [  # NOT IN USE
    [
        u"January", u"February", u"March",
        u"April", u"May", u"June",
        u"July", u"August", u"September",
        u"October", u"November", u"December"
    ],
    [
        u"Jan", u"Feb", u"Mar", u"Apr", u"May",
        u"Jun", u"Jul", u"Aug", u"Sep", u"Oct",
        u"Nov", u"Dec"
    ]
]

HOLIDAYS = [
    [  # begin english
        [  # begin english long
            u"Rosh Hashana I", u"Rosh Hashana II",
            u"Tzom Gedaliah", u"Yom Kippur",
            u"Sukkot", u"Hol hamoed Sukkot",
            u"Hoshana raba", u"Simchat Torah",
            u"Chanukah", u"Asara B'Tevet",
            u"Tu B'Shvat", u"Ta'anit Esther",
            u"Purim", u"Shushan Purim",
            u"Pesach", u"Hol hamoed Pesach",
            u"Yom HaAtzma'ut", u"Lag B'Omer",
            u"Erev Shavuot", u"Shavuot",
            u"Tzom Tammuz", u"Tish'a B'Av",
            u"Tu B'Av", u"Yom HaShoah",
            u"Yom HaZikaron", u"Yom Yerushalayim",
            u"Shmini Atzeret", u"Pesach VII",
            u"Pesach VIII", u"Shavuot II",
            u"Sukkot II", u"Pesach II",
            u"Family Day",
            u"Memorial day for fallen whose place of burial is unknown",
            u"Yitzhak Rabin memorial day", u"Zeev Zhabotinsky day",
            u"Erev Yom Kippur"],
        [  # begin english short
            u"Rosh Hashana I", u"Rosh Hashana II",
            u"Tzom Gedaliah", u"Yom Kippur",
            u"Sukkot", u"Hol hamoed Sukkot",
            u"Hoshana raba", u"Simchat Torah",
            u"Chanukah", u"Asara B'Tevet",      # 10
            u"Tu B'Shvat", u"Ta'anit Esther",
            u"Purim", u"Shushan Purim",
            u"Pesach", u"Hol hamoed Pesach",
            u"Yom HaAtzma'ut", u"Lag B'Omer",
            u"Erev Shavuot", u"Shavuot",            # 20
            u"Tzom Tammuz", u"Tish'a B'Av",
            u"Tu B'Av", u"Yom HaShoah",
            u"Yom HaZikaron", u"Yom Yerushalayim",
            u"Shmini Atzeret", u"Pesach VII",
            u"Pesach VIII", u"Shavuot II",         # 30
            u"Sukkot II", u"Pesach II",
            u"Family Day",
            u"Memorial day for fallen whose place of burial is unknown",
            u"Rabin memorial day", u"Zhabotinsky day",
            u"Erev Yom Kippur"]
    ],
    [  # begin hebrew
        [  # begin hebrew long
            u"א' ראש השנה", u"ב' ראש השנה",
            u"צום גדליה", u"יום הכפורים",
            u"סוכות", u"חול המועד סוכות",
            u"הושענא רבה", u"שמחת תורה",
            u"חנוכה", u"צום עשרה בטבת",  # 10
            u"ט\"ו בשבט", u"תענית אסתר",
            u"פורים", u"שושן פורים",
            u"פסח", u"חול המועד פסח",
            u"יום העצמאות", u"ל\"ג בעומר",
            u"ערב שבועות", u"שבועות",  # 20
            u"צום שבעה עשר בתמוז", u"תשעה באב",
            u"ט\"ו באב", u"יום השואה",
            u"יום הזכרון", u"יום ירושלים",
            u"שמיני עצרת", u"שביעי פסח",
            u"אחרון של פסח", u"שני של שבועות",  # 30
            u"שני של סוכות", u"שני של פסח",
            u"יום המשפחה", u"יום זכרון...",
            u"יום הזכרון ליצחק רבין", u"יום ז\'בוטינסקי",
            u"עיוה\"כ"],
        [  # begin hebrew short
            u"א ר\"ה", u"ב' ר\"ה",
            u"צום גדליה", u"יוה\"כ",
            u"סוכות", u"חוה\"מ סוכות",
            u"הוש\"ר", u"שמח\"ת",
            u"חנוכה", u"י' בטבת",  # 10
            u"ט\"ו בשבט", u"תענית אסתר",
            u"פורים", u"שושן פורים",
            u"פסח", u"חוה\"מ פסח",
            u"יום העצמאות", u"ל\"ג בעומר",
            u"ערב שבועות", u"שבועות",  # 20
            u"צום תמוז", u"ט' באב",
            u"ט\"ו באב", u"יום השואה",
            u"יום הזכרון", u"יום י-ם",
            u"שמיני עצרת", u"ז' פסח",
            u"אחרון של פסח", u"ב' שבועות",  # 30
            u"ב' סוכות", u"ב' פסח",
            u"יום המשפחה", u"יום זכרון...",
            u"יום הזכרון ליצחק רבין", u"יום ז\'בוטינסקי",
            u"עיוה\"כ"]
    ]
]

ZMANIM_TYPES = ['first_light', 'talit', 'sunrise',
                'mga_end_shma', 'gra_end_shma', 'mga_end_tfila',
                'gra_end_tfila', 'midday', 'big_mincha', 'small_mincha',
                'plag_mincha', 'sunset', 'first_stars', 'midnight']

ZMANIM_STRING = {
    'heb':
        {
            'first_light':   'עלות השחר',
            'talit':         'זמן טלית ותפילין',
            'sunrise':       'הנץ החמה',
            'sunset':        'שקיעה',
            'first_stars':   'צאת הככבים',
            'plag_mincha':   'פלג מנחה',
            'big_mincha':    'מנחה גדולה',
            'small_mincha':  'מנחה קטנה',
            'mga_end_shma':  'סוף זמן ק"ש מג"א',
            'gra_end_shma':  'סוף זמן ק"ש הגר"א',
            'mga_end_tfila': 'סוף זמן תפילה מג"א',
            'gra_end_tfila': 'סוף זמן תפילה גר"א',
            'midnight':      'חצות הלילה',
            'midday':        'חצות היום',
        },
    'eng':
        {
            'first_light':   'Alot HaShachar',
            'talit':         'Talit & Tefilin\'s time',
            'sunrise':       'sunrise',
            'sunset':        'sunset',
            'first_stars':   'first starts',
            'plag_mincha':   'Plag Mincha',
            'big_mincha':    'Big Mincha',
            'small_mincha':  'Small Mincha',
            'mga_end_shma':  'Shema EOT MG"A',
            'gra_end_shma':  'Shema EOT GR"A',
            'mga_end_tfila': 'Tefila EOT MG"A',
            'gra_end_tfila': 'Tefila EOT GR"A',
            'midnight':      'midnight',
            'midday':        'midday',
        }
}
