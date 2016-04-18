# holydays table
holydays_table = [
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
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
        0, 0, 0, 0, 0, 0, 0, 0, 36, 36],
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
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        12, 0, 12, 13, 14, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Joined Parash flags
join_flags = [
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

digits = [
    [" ", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"],
    ["ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"],
    [" ", "ק", "ר", "ש", "ת"]
]

days_table = [
    [   #begin english long
        ["Sunday",  "Monday",  "Tuesday",  "Wednesday", "Thursday",  "Friday",  "Saturday"],
		# begin english short
		["Sun",  "Mon",  "Tue",  "Wed",  "Thu", "Fri",  "Sat"],
    ],
	[   # begin hebrew long
        ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"],
		# begin hebrew short
		["א", "ב", "ג", "ד", "ה", "ו", "ש"]
    ]
]

parashaot = [
	[  # begin english
		[  # begin english long
		 "none",		"Bereshit",		"Noach",
		 "Lech-Lecha",	"Vayera",		"Chayei Sara",
		 "Toldot",		"Vayetzei",		"Vayishlach",
		 "Vayeshev",	"Miketz",		"Vayigash",		# 11
		 "Vayechi",		"Shemot",		"Vaera",
		 "Bo",		"Beshalach",	"Yitro",
		 "Mishpatim",	"Terumah",		"Tetzaveh",		# 20
		 "Ki Tisa",		"Vayakhel",		"Pekudei",
		 "Vayikra",		"Tzav",		"Shmini",
		 "Tazria",		"Metzora",		"Achrei Mot",
		 "Kedoshim",	"Emor",		"Behar",		# 32
		 "Bechukotai",	"Bamidbar",		"Nasso",
		 "Beha'alotcha",	"Sh'lach",		"Korach",
		 "Chukat",		"Balak",		"Pinchas",		# 41
		 "Matot",		"Masei",		"Devarim",
		 "Vaetchanan",	"Eikev",		"Re'eh",
		 "Shoftim",		"Ki Teitzei",	"Ki Tavo",		# 50
		 "Nitzavim",	"Vayeilech",	"Ha'Azinu",
		 "Vezot Habracha",	# 54
		 "Vayakhel-Pekudei","Tazria-Metzora",	"Achrei Mot-Kedoshim",
		 "Behar-Bechukotai","Chukat-Balak",	"Matot-Masei",
		 "Nitzavim-Vayeilech"],
		[ # begin english short
		 "none",		"Bereshit",		"Noach",
		 "Lech-Lecha",	"Vayera",		"Chayei Sara",
		 "Toldot",		"Vayetzei",		"Vayishlach",
		 "Vayeshev",	"Miketz",		"Vayigash",		# 11
		 "Vayechi",		"Shemot",		"Vaera",
		 "Bo",		"Beshalach",	"Yitro",
		 "Mishpatim",	"Terumah",		"Tetzaveh",		# 20
		 "Ki Tisa",		"Vayakhel",		"Pekudei",
		 "Vayikra",		"Tzav",		"Shmini",
		 "Tazria",		"Metzora",		"Achrei Mot",
		 "Kedoshim",	"Emor",		"Behar",		# 32
		 "Bechukotai",	"Bamidbar",		"Nasso",
		 "Beha'alotcha",	"Sh'lach",		"Korach",
		 "Chukat",		"Balak",		"Pinchas",		# 41
		 "Matot",		"Masei",		"Devarim",
		 "Vaetchanan",	"Eikev",		"Re'eh",
		 "Shoftim",		"Ki Teitzei",	"Ki Tavo",		# 50
		 "Nitzavim",	"Vayeilech",	"Ha'Azinu",
		 "Vezot Habracha",	# 54
		 "Vayakhel-Pekudei","Tazria-Metzora",	"Achrei Mot-Kedoshim",
		 "Behar-Bechukotai","Chukat-Balak",	"Matot-Masei",
		 "Nitzavim-Vayeilech"]
	],
	[ # begin hebrew
		[ # begin hebrew long
		 "none",		"בראשית",		"נח",
		 "לך לך",		"וירא",			"חיי שרה",
		 "תולדות",		"ויצא",			"וישלח",
		 "וישב",		"מקץ",			"ויגש",		# 11
		 "ויחי",		"שמות",			"וארא",
		 "בא",			"בשלח",			"יתרו",
		 "משפטים",		"תרומה",		"תצוה",		# 20
		 "כי תשא",		"ויקהל",		"פקודי",
		 "ויקרא",		"צו",			"שמיני",
		 "תזריע",		"מצורע",		"אחרי מות",
		 "קדושים",		"אמור",			"בהר",		# 32
		 "בחוקתי",		"במדבר",		"נשא",
		 "בהעלתך",		"שלח",			"קרח",
		 "חקת",			"בלק",			"פנחס",		# 41
		 "מטות",		"מסעי",			"דברים",
		 "ואתחנן",		"עקב",			"ראה",
		 "שופטים",		"כי תצא",		"כי תבוא",		# 50
		 "נצבים",		"וילך",			"האזינו",
		 "וזאת הברכה",	# 54
		 "ויקהל-פקודי",	"תזריע-מצורע",	"אחרי מות-קדושים",
		 "בהר-בחוקתי",	"חוקת-בלק",		"מטות מסעי",
		 "נצבים-וילך"],
		[ # begin hebrew short
		 "none",		"בראשית",		"נח",
		 "לך לך",		"וירא",			"חיי שרה",
		 "תולדות",		"ויצא",			"וישלח",
		 "וישב",		"מקץ",			"ויגש",		# 11
		 "ויחי",		"שמות",			"וארא",
		 "בא",			"בשלח",			"יתרו",
		 "משפטים",		"תרומה",		"תצוה",		# 20
		 "כי תשא",		"ויקהל",		"פקודי",
		 "ויקרא",		"צו",			"שמיני",
		 "תזריע",		"מצורע",		"אחרי מות",
		 "קדושים",		"אמור",			"בהר",		# 32
		 "בחוקתי",		"במדבר",		"נשא",
		 "בהעלתך",		"שלח",			"קרח",
		 "חקת",			"בלק",			"פנחס",		# 41
		 "מטות",		"מסעי",			"דברים",
		 "ואתחנן",		"עקב",			"ראה",
		 "שופטים",		"כי תצא",		"כי תבוא",		# 50
		 "נצבים",		"וילך",			"האזינו",
		 "וזאת הברכה",	# 54
		 "ויקהל-פקודי",	"תזריע-מצורע",	"אחרי מות-קדושים",
		 "בהר-בחוקתי",	"חוקת-בלק",		"מטות מסעי",
		 "נצבים-וילך"]
	]
]

hebrew_months = [
	[ # begin english
		[ # begin english long
		 "Tishrei", "Cheshvan", "Kislev", "Tevet",
		 "Sh'vat", "Adar", "Nisan", "Iyyar",
		 "Sivan", "Tammuz", "Av", "Elul", "Adar I",
		 "Adar II"],
		[ # begin english short
		 "Tishrei", "Cheshvan", "Kislev", "Tevet",
		 "Sh'vat", "Adar", "Nisan", "Iyyar",
		 "Sivan", "Tammuz", "Av", "Elul", "Adar I",
		 "Adar II"]
		],
	[ # begin hebrew
		[ # begin hebrew long
		 "תשרי", "חשון", "כסלו", "טבת", "שבט", "אדר", "ניסן", "אייר",
		  "סיון", "תמוז", "אב", "אלול", "אדר א", "אדר ב" ],
		[ # begin hebrew short
		 "תשרי", "חשון", "כסלו", "טבת", "שבט", "אדר", "ניסן", "אייר",
		  "סיון", "תמוז", "אב", "אלול", "אדר א", "אדר ב" ]
    ]
]

gregorian_months = [
		["January", "February", "March",
		 "April", "May", "June",
		 "July", "August", "September",
		 "October", "November", "December"],
		["Jan", "Feb", "Mar", "Apr", "May",
		 "Jun", "Jul", "Aug", "Sep", "Oct",
		 "Nov", "Dec"],
	]

holidays = [
	[ # begin english
		[ # begin english long
		 "Rosh Hashana I",	"Rosh Hashana II",
		 "Tzom Gedaliah",	"Yom Kippur",
		 "Sukkot",			"Hol hamoed Sukkot",
		 "Hoshana raba",	"Simchat Torah",
		 "Chanukah",		"Asara B'Tevet",
		 "Tu B'Shvat",		"Ta'anit Esther",
		 "Purim",			"Shushan Purim",
		 "Pesach",			"Hol hamoed Pesach",
		 "Yom HaAtzma'ut",	"Lag B'Omer",
		 "Erev Shavuot",	"Shavuot",
		 "Tzom Tammuz",		"Tish'a B'Av",
		 "Tu B'Av",			"Yom HaShoah",
		 "Yom HaZikaron",	"Yom Yerushalayim",
		 "Shmini Atzeret",	"Pesach VII",
		 "Pesach VIII",		"Shavuot II",
		 "Sukkot II",		"Pesach II",
		 "Family Day",		"Memorial day for fallen whose place of burial is unknown", 
		 "Yitzhak Rabin memorial day", "Zeev Zhabotinsky day",
		 "Rabin memorial day",	 "Zhabotinsky day",
		 "Erev Yom Kippur"],
		[ # begin english short
		 "Rosh Hashana I",	"Rosh Hashana II",
		 "Tzom Gedaliah",	"Yom Kippur",
		 "Sukkot",			"Hol hamoed Sukkot",
		 "Hoshana raba",	"Simchat Torah",
		 "Chanukah",		"Asara B'Tevet",	# 10
		 "Tu B'Shvat",		"Ta'anit Esther",
		 "Purim",			"Shushan Purim",
		 "Pesach",			"Hol hamoed Pesach",
		 "Yom HaAtzma'ut",	"Lag B'Omer",
		 "Erev Shavuot",	"Shavuot",			# 20
		 "Tzom Tammuz",		"Tish'a B'Av",
		 "Tu B'Av",			"Yom HaShoah",
		 "Yom HaZikaron",	"Yom Yerushalayim",
		 "Shmini Atzeret",	"Pesach VII",
		 "Pesach VIII",		"Shavuot II",   # 30
		 "Sukkot II",		"Pesach II",	 
		 "Family Day",		"Memorial day for fallen whose place of burial is unknown", 
		 "Rabin memorial day",	 "Zhabotinsky day",
		 "Erev Yom Kippur"]
	],
    [ # begin hebrew
		[ # begin hebrew long
		 "א ר\"ה",		 "ב' ר\"ה",
		 "צום גדליה",	 "יוה\"כ",
		 "סוכות",		 "חוה\"מ סוכות",
		 "הוש\"ר",		 "שמח\"ת",
		 "חנוכה",		 "י' בטבת",	# 10
		 "ט\"ו בשבט",	 "תענית אסתר",
		 "פורים",		 "שושן פורים",
		 "פסח",			 "חוה\"מ פסח",
		 "יום העצמאות",	 "ל\"ג בעומר",
		 "ערב שבועות",	 "שבועות",	# 20
		 "צום תמוז",	 "ט' באב",
		 "ט\"ו באב",	 "יום השואה",
		 "יום הזכרון",	 "יום י-ם",
		 "שמיני עצרת",	 "ז' פסח",
		 "אחרון של פסח", "ב' שבועות",   # 30
		 "ב' סוכות",	 "ב' פסח",	 
		 "יום המשפחה",	 "יום זכרון...", 
		 "יום הזכרון ליצחק רבין","יום ז\'בוטינסקי",
		 "עיוה\"כ"],
		[ # begin hebrew short
		 "א' ראש השנה",		"ב' ראש השנה",
		 "צום גדליה",		"יום הכפורים",
		 "סוכות",		    "חול המועד סוכות",
		 "הושענא רבה",		"שמחת תורה",
		 "חנוכה",		    "צום עשרה בטבת",# 10
		 "ט\"ו בשבט",		"תענית אסתר",
		 "פורים",		    "שושן פורים",
		 "פסח",			    "חול המועד פסח",
		 "יום העצמאות",		"ל\"ג בעומר",
		 "ערב שבועות",		"שבועות",	# 20
		 "צום שבעה עשר בתמוז",	"תשעה באב",
		 "ט\"ו באב",		"יום השואה",
		 "יום הזכרון",		"יום ירושלים",
		 "שמיני עצרת",		"שביעי פסח",
		 "אחרון של פסח",	"שני של שבועות",# 30
		 "שני של סוכות",	"שני של פסח",
		 "יום המשפחה",		"יום זכרון...", 
		 "יום הזכרון ליצחק רבין","יום ז\'בוטינסקי",
		 "עיוה\"כ"]	
    ]
]
