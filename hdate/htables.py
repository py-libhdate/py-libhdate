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
    [" ", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"],
    ["ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"],
    [" ", "ק", "ר", "ש", "ת"]
]

DAYS_TABLE = [
    [   # begin english long
        ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
         "Saturday"],
        # begin english short
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    ],
    [   # begin hebrew long
        ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"],
        # begin hebrew short
        ["א", "ב", "ג", "ד", "ה", "ו", "ש"]
    ]
]

PARASHAOT = [
    [  # begin english
        "none", "Bereshit", "Noach",
        "Lech-Lecha", "Vayera", "Chayei Sara",
        "Toldot", "Vayetzei", "Vayishlach",
        "Vayeshev", "Miketz", "Vayigash",     # 11
        "Vayechi", "Shemot", "Vaera",
        "Bo", "Beshalach", "Yitro",
        "Mishpatim", "Terumah", "Tetzaveh",     # 20
        "Ki Tisa", "Vayakhel", "Pekudei",
        "Vayikra", "Tzav", "Shmini",
        "Tazria", "Metzora", "Achrei Mot",
        "Kedoshim", "Emor", "Behar",        # 32
        "Bechukotai", "Bamidbar", "Nasso",
        "Beha'alotcha", "Sh'lach", "Korach",
        "Chukat", "Balak", "Pinchas",      # 41
        "Matot", "Masei", "Devarim",
        "Vaetchanan", "Eikev", "Re'eh",
        "Shoftim", "Ki Teitzei", "Ki Tavo",      # 50
        "Nitzavim", "Vayeilech", "Ha'Azinu",
        "Vezot Habracha",                             # 54
        "Vayakhel-Pekudei", "Tazria-Metzora", "Achrei Mot-Kedoshim",
        "Behar-Bechukotai", "Chukat-Balak", "Matot-Masei",
        "Nitzavim-Vayeilech"],
    [     # begin hebrew
        "none", "בראשית", "נח",
        "לך לך", "וירא", "חיי שרה",
        "תולדות", "ויצא", "וישלח",
        "וישב", "מקץ", "ויגש",  # 11
        "ויחי", "שמות", "וארא",
        "בא", "בשלח", "יתרו",
        "משפטים", "תרומה", "תצוה",  # 20
        "כי תשא", "ויקהל", "פקודי",
        "ויקרא", "צו", "שמיני",
        "תזריע", "מצורע", "אחרי מות",
        "קדושים", "אמור", "בהר",  # 32
        "בחוקתי", "במדבר", "נשא",
        "בהעלתך", "שלח", "קרח",
        "חקת", "בלק", "פנחס",  # 41
        "מטות", "מסעי", "דברים",
        "ואתחנן", "עקב", "ראה",
        "שופטים", "כי תצא", "כי תבוא",  # 50
        "נצבים", "וילך", "האזינו",
        "וזאת הברכה",  # 54
        "ויקהל-פקודי", "תזריע-מצורע", "אחרי מות-קדושים",
        "בהר-בחוקתי", "חוקת-בלק", "מטות מסעי",
        "נצבים-וילך"]
]

HEBREW_MONTHS = [
    [  # begin english
        "Tishrei", "Cheshvan", "Kislev", "Tevet",
        "Sh'vat", "Adar", "Nisan", "Iyyar",
        "Sivan", "Tammuz", "Av", "Elul", "Adar I",
        "Adar II"
    ],
    [  # begin hebrew
        "תשרי", "חשון", "כסלו", "טבת", "שבט", "אדר", "ניסן", "אייר",
        "סיון", "תמוז", "אב", "אלול", "אדר א", "אדר ב"
    ]
]

GREGORIAN_MONTHS = [  # NOT IN USE
    [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ],
    [
        "Jan", "Feb", "Mar", "Apr", "May",
        "Jun", "Jul", "Aug", "Sep", "Oct",
        "Nov", "Dec"
    ]
]

HOLIDAYS = [
    [  # begin english
        [  # begin english long
            "Rosh Hashana I", "Rosh Hashana II",
            "Tzom Gedaliah", "Yom Kippur",
            "Sukkot", "Hol hamoed Sukkot",
            "Hoshana raba", "Simchat Torah",
            "Chanukah", "Asara B'Tevet",
            "Tu B'Shvat", "Ta'anit Esther",
            "Purim", "Shushan Purim",
            "Pesach", "Hol hamoed Pesach",
            "Yom HaAtzma'ut", "Lag B'Omer",
            "Erev Shavuot", "Shavuot",
            "Tzom Tammuz", "Tish'a B'Av",
            "Tu B'Av", "Yom HaShoah",
            "Yom HaZikaron", "Yom Yerushalayim",
            "Shmini Atzeret", "Pesach VII",
            "Pesach VIII", "Shavuot II",
            "Sukkot II", "Pesach II",
            "Family Day",
            "Memorial day for fallen whose place of burial is unknown",
            "Yitzhak Rabin memorial day", "Zeev Zhabotinsky day",
            "Erev Yom Kippur"],
        [  # begin english short
            "Rosh Hashana I", "Rosh Hashana II",
            "Tzom Gedaliah", "Yom Kippur",
            "Sukkot", "Hol hamoed Sukkot",
            "Hoshana raba", "Simchat Torah",
            "Chanukah", "Asara B'Tevet",      # 10
            "Tu B'Shvat", "Ta'anit Esther",
            "Purim", "Shushan Purim",
            "Pesach", "Hol hamoed Pesach",
            "Yom HaAtzma'ut", "Lag B'Omer",
            "Erev Shavuot", "Shavuot",            # 20
            "Tzom Tammuz", "Tish'a B'Av",
            "Tu B'Av", "Yom HaShoah",
            "Yom HaZikaron", "Yom Yerushalayim",
            "Shmini Atzeret", "Pesach VII",
            "Pesach VIII", "Shavuot II",         # 30
            "Sukkot II", "Pesach II",
            "Family Day",
            "Memorial day for fallen whose place of burial is unknown",
            "Rabin memorial day", "Zhabotinsky day",
            "Erev Yom Kippur"]
    ],
    [  # begin hebrew
        [  # begin hebrew long
            "א' ראש השנה", "ב' ראש השנה",
            "צום גדליה", "יום הכפורים",
            "סוכות", "חול המועד סוכות",
            "הושענא רבה", "שמחת תורה",
            "חנוכה", "צום עשרה בטבת",  # 10
            "ט\"ו בשבט", "תענית אסתר",
            "פורים", "שושן פורים",
            "פסח", "חול המועד פסח",
            "יום העצמאות", "ל\"ג בעומר",
            "ערב שבועות", "שבועות",  # 20
            "צום שבעה עשר בתמוז", "תשעה באב",
            "ט\"ו באב", "יום השואה",
            "יום הזכרון", "יום ירושלים",
            "שמיני עצרת", "שביעי פסח",
            "אחרון של פסח", "שני של שבועות",  # 30
            "שני של סוכות", "שני של פסח",
            "יום המשפחה", "יום זכרון...",
            "יום הזכרון ליצחק רבין", "יום ז\'בוטינסקי",
            "עיוה\"כ"],
        [  # begin hebrew short
            "א ר\"ה", "ב' ר\"ה",
            "צום גדליה", "יוה\"כ",
            "סוכות", "חוה\"מ סוכות",
            "הוש\"ר", "שמח\"ת",
            "חנוכה", "י' בטבת",  # 10
            "ט\"ו בשבט", "תענית אסתר",
            "פורים", "שושן פורים",
            "פסח", "חוה\"מ פסח",
            "יום העצמאות", "ל\"ג בעומר",
            "ערב שבועות", "שבועות",  # 20
            "צום תמוז", "ט' באב",
            "ט\"ו באב", "יום השואה",
            "יום הזכרון", "יום י-ם",
            "שמיני עצרת", "ז' פסח",
            "אחרון של פסח", "ב' שבועות",  # 30
            "ב' סוכות", "ב' פסח",
            "יום המשפחה", "יום זכרון...",
            "יום הזכרון ליצחק רבין", "יום ז\'בוטינסקי",
            "עיוה\"כ"]
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
