import datetime
from collections import namedtuple
from typing import Union

import hdate
from hdate import converters as conv
from hdate.hebrew_date import HebrewDate

LANG = namedtuple("LANG", ["french", "english", "hebrew"])
TRADITION = namedtuple(
    "TRADITION", ["israel", "diaspora_ashkenazi", "diaspora_sephardi"]
)


class Tekufot:
    def __init__(
        self,
        date: Union[datetime.date, str, datetime.datetime] = datetime.datetime.now(),
        diaspora: bool = True,
    ):
        # Convert date to datetime.date object
        if isinstance(date, str):
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("The date string must be in 'YYYY-MM-DD' format")
        elif isinstance(date, datetime.datetime):
            date = date.date()
        elif not isinstance(date, datetime.date):
            raise TypeError(
                "The date must be a datetime.date, datetime.datetime object, or a string in 'YYYY-MM-DD' format"
            )

        self.date = date
        self.diaspora = diaspora
        self.gregorian_year = date.year
        self.hebrew_year = self.gregorian_year + 3760
        self.jdn = conv.gdate_to_jdn(date)
        self.hebrew_date = conv.jdn_to_hdate(self.jdn)
        self.hebrew_year_p = self.hebrew_date.year
        self.gregorian_year_p = self.hebrew_year_p - 3760
        self.weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Initial calculations
        self.get_days_shift()
        self.get_tekufa_dates()
        self.get_cheilat_geshamim()
        self.set_prayer_periods()  # Correction here

    @property
    def is_leap_year(self) -> bool:
        """Return True if this date's year is a leap year."""
        return self.hdate.year % 19 in [0, 3, 6, 8, 11, 14, 17]

    def get_days_shift(self):
        """
        Calculates the day shift for the Tekufa.
        """

        years_elapsed = self.hebrew_year_p - 1
        self.days_shift = (years_elapsed * 1.25 + 1.75) % 7
        self.days_shift_int = int(self.days_shift)
        self.days_shift_decimal = self.days_shift - self.days_shift_int
        self.tekufa_hour = self.days_shift_decimal * 24

    def get_tekufa_dates(self):
        """
        Calculates the dates and times of the Tekufot of Nissan, Tammuz, Tishrei, and Tevet.
        """
        INTERVAL_DAYS = 91
        INTERVAL_HOURS = 7.5  # 7 hours and 30 minutes

        # Start with Tekufa Nissan
        date_april_7 = datetime.date(self.gregorian_year_p, 4, 7)
        date_april_8 = datetime.date(self.gregorian_year_p, 4, 8)
        date_april_9 = datetime.date(self.gregorian_year_p, 4, 9)

        weekday_april_7 = date_april_7.weekday()
        weekday_april_8 = date_april_8.weekday()
        weekday_april_9 = date_april_9.weekday()

        if self.hebrew_year_p <= 5861 or self.gregorian_year <= 2100:
            if weekday_april_8 == self.days_shift_int:
                tekufa_nissan_date = date_april_8
            elif weekday_april_7 == self.days_shift_int:
                tekufa_nissan_date = date_april_7
            else:
                tekufa_nissan_date = None
        else:
            if weekday_april_8 == self.days_shift_int:
                tekufa_nissan_date = date_april_8
            elif weekday_april_9 == self.days_shift_int:
                tekufa_nissan_date = date_april_9
            else:
                tekufa_nissan_date = None

        # print(tekufa_nissan_date.strftime('%d/%m/%Y at %H:%M'))

        if tekufa_nissan_date:
            tekufa_nissan = datetime.datetime.combine(
                tekufa_nissan_date, datetime.time(0, 0)
            ) + datetime.timedelta(hours=self.tekufa_hour)
            self.tekufa_nissan = tekufa_nissan

            # Calculation of subsequent Tekufot
            tekufa_delta = datetime.timedelta(
                days=INTERVAL_DAYS,
                hours=int(INTERVAL_HOURS),
                minutes=(INTERVAL_HOURS - int(INTERVAL_HOURS)) * 60,
            )
            self.tekufa_tevet = self.tekufa_nissan - tekufa_delta
            self.tekufa_tishrei = self.tekufa_tevet - tekufa_delta
            self.tekufa_tammuz = self.tekufa_nissan + tekufa_delta

    def get_cheilat_geshamim(self):
        """
        Calculates the start date for the prayers for rain (Cheilat Geshamim).
        In the diaspora, it is 59 days after Tekufat Tishrei, adjusted for time.
        In Israel, it is fixed at the 7th of Cheshvan.
        The resulting date is normalized to midnight (00:00).
        """
        if not self.tekufa_tishrei:
            self.cheilat_geshamim = None
            return

        if self.diaspora:
            cheilat_geshamim = self.tekufa_tishrei + datetime.timedelta(days=59)
            # Adjust for time (after 16:00)
            if (
                isinstance(cheilat_geshamim, datetime.datetime)
                and cheilat_geshamim.hour >= 16
            ):
                cheilat_geshamim += datetime.timedelta(days=1)
            # Normalize to date at midnight
            self.cheilat_geshamim = datetime.date(
                cheilat_geshamim.year, cheilat_geshamim.month, cheilat_geshamim.day
            )
        else:
            # Convert 7th of Cheshvan (Hebrew date) to Gregorian
            hdate_7_cheshvan = HebrewDate(self.hebrew_year_p, 2, 7)
            jdn_7_cheshvan = conv.hdate_to_jdn(hdate_7_cheshvan)
            gdate_7_cheshvan = conv.jdn_to_gdate(jdn_7_cheshvan)
            # Normalize to date at midnight
            self.cheilat_geshamim = datetime.date(
                gdate_7_cheshvan.year, gdate_7_cheshvan.month, gdate_7_cheshvan.day
            )

    def set_prayer_periods(self):
        """
        Defines the prayer periods based on the calculated dates.
        """
        # Key dates
        # Define the namedtuples

        hdate_shemini_atzeret = HebrewDate(self.hebrew_year_p, 1, 22)
        jdn_shemini_atzeret = conv.hdate_to_jdn(hdate_shemini_atzeret)
        self.shemini_atzeret = conv.jdn_to_gdate(jdn_shemini_atzeret)

        hdate_next_shemini_atzeret = HebrewDate(self.hebrew_year_p + 1, 1, 22)
        jdn_next_shemini_atzeret = conv.hdate_to_jdn(hdate_next_shemini_atzeret)
        self.next_shemini_atzeret = conv.jdn_to_gdate(jdn_next_shemini_atzeret)

        hdate_7_cheshvan = HebrewDate(self.hebrew_year_p, 2, 7)
        jdn_7_cheshvan = conv.hdate_to_jdn(hdate_7_cheshvan)
        self.seventh_cheshvan = conv.jdn_to_gdate(jdn_7_cheshvan)

        hdate_prev_pesach = HebrewDate(self.hebrew_year_p - 1, 7, 15)
        jdn_prev_pesach = conv.hdate_to_jdn(hdate_prev_pesach)
        self.prev_pesach = conv.jdn_to_gdate(jdn_prev_pesach)

        hdate_pesach = HebrewDate(self.hebrew_year_p, 7, 15)
        jdn_pesach = conv.hdate_to_jdn(hdate_pesach)
        self.pesach = conv.jdn_to_gdate(jdn_pesach)

        if self.cheilat_geshamim:
            self.tekufa_tishrei_plus_60 = self.cheilat_geshamim.date()
        else:
            self.tekufa_tishrei_plus_60 = None

        # Definition of prayer periods
        self.prayer_periods = [
            ("prev_pessah_to_shemini", self.prev_pesach, self.shemini_atzeret),
            ("shemini_to_cheshvan", self.shemini_atzeret, self.seventh_cheshvan),
            (
                "cheshvan_to_geshamim",
                self.seventh_cheshvan,
                self.tekufa_tishrei_plus_60,
            ),
            ("geshamim_to_pessah", self.tekufa_tishrei_plus_60, self.pesach),
            ("pessah_to_shemini_next", self.pesach, self.next_shemini_atzeret),
        ]
        # Define the prayer descriptions without parameter names

    def get_prayer_for_date(
        self,
        date: datetime.date = None,
        tradition: str = "israel",
        language: str = "english",
    ) -> str:
        """
        Returns the appropriate prayer phrases for the given date, tradition, and language.
        The tradition can be 'israel', 'diaspora_ashkenazi', or 'diaspora_sephardi'.
        The language can be 'english', 'french', or 'hebrew'.
        """
        if date is None:
            date = self.date

        for period_name, start_date, end_date in self.prayer_periods:
            if start_date and end_date:
                if start_date <= date < end_date:
                    tradition_data = PRAYER_DESCRIPTIONS.get(period_name)
                    if tradition_data:
                        lang_data = getattr(tradition_data, tradition)
                        if lang_data:
                            return getattr(lang_data, language)
        return "No prayer phrase found for this date, tradition, and language."

    def get_results(self):
        """
        Returns a dictionary containing all the calculated dates and times.
        """
        return {
            "date": self.date,
            "gregorian_year": self.gregorian_year,
            "hebrew_year": self.hebrew_year,
            "hebrew_year_p": self.hebrew_year_p,
            "diaspora": self.diaspora,
            "tekufa_nissan": self.tekufa_nissan,
            "tekufa_tammuz": self.tekufa_tammuz,
            "tekufa_tishrei": self.tekufa_tishrei,
            "tekufa_tevet": self.tekufa_tevet,
            "cheilat_geshamim": self.cheilat_geshamim,
            "pesach": self.pesach,
            "shemini_atzeret": self.shemini_atzeret,
            "seventh_cheshvan": self.seventh_cheshvan,
            "tekufa_tishrei_plus_60": self.tekufa_tishrei_plus_60,
            "next_shemini_atzeret": self.next_shemini_atzeret,
            "prev_pesach": self.prev_pesach,
        }


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
