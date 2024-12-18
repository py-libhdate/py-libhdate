"""
The class attempts to compute:
    - The tekufot (seasons) in the Hebrew calendar: Nissan, Tammuz, Tishrei, and Tevet.
    - Cheilat Geshamim start date, which differs between the diaspora and Israel.
    - Halachic prayer periods based on key Jewish holidays and seasonal changes.
    - Appropriate prayer phrases depending on the current date, tradition, and language.
"""

import datetime
from collections import namedtuple
from typing import Optional, Union

from hdate import converters as conv
from hdate.hebrew_date import HebrewDate
from hdate.location import Location
from hdate.zmanim import Zmanim

LANG = namedtuple("LANG", ["french", "english", "hebrew"])
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


class Tekufot:  # pylint: disable=too-many-instance-attributes
    """
    A class that calculates and manages Jewish seasonal times (Tekufot),
    periods for prayer insertions, and associated halachic dates such as
    the start of Cheilat Geshamim (requesting rain)."""

    def __init__(
        self,
        date: Union[datetime.date, str, datetime.datetime] = datetime.datetime.now(),
        diaspora: bool = True,
        location: Location = Location(),
    ):

        if isinstance(date, str):
            # If a string is given, parse it into a date/datetime if needed.
            # For now, assume YYYY-MM-DD format.
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        elif isinstance(date, datetime.datetime):
            date = date.date()

        self.date = date
        self.gregorian_year = date.year
        self.hebrew_year = self.gregorian_year + 3760
        self.diaspora = diaspora
        self.location = location

        # Convert current date to JDN and Hebrew Date
        self.jdn = conv.gdate_to_jdn(date)
        self.hebrew_date = conv.jdn_to_hdate(self.jdn)
        self.hebrew_year_p = self.hebrew_date.year
        self.gregorian_year_p = self.hebrew_year_p - 3760

        # Tekufot calculations
        self.get_tekufa()

        # Cheilat Geshamim calculation
        self.get_cheilat_geshamim()

        # Prayer periods
        self.set_prayer_periods()

    def get_tekufa(self) -> None:
        """
        Calculates the approximate dates and times of the Tekufot.
        This is a simplified approximation. Traditional calculations may differ.
        """

        interval_days = 91
        interval_hours = 7.5  # 7 hours and 30 minutes

        # Start with Tekufa Nissan:
        # Historically approximated at the spring equinox. For simplicity, assume:
        # If the Hebrew year corresponds to a Gregorian year before 2100
        # we take April 7 as a reference, otherwise April 8

        if self.gregorian_year_p < 2100:
            date_equinox_april = datetime.date(self.gregorian_year_p, 4, 7)
        else:
            date_equinox_april = datetime.date(self.gregorian_year_p, 4, 8)

        # Hours shift depends on leap year cycles
        hours_delta_nissan = (self.gregorian_year_p % 4) * 6

        # Tekufa Nissan: start at date_equinox_april at 12:00
        tekufa_nissan = datetime.datetime.combine(
            date_equinox_april, datetime.time(12, 0)
        ) + datetime.timedelta(hours=hours_delta_nissan)
        self.tekufa_nissan = tekufa_nissan

        # Tekufa intervals are about 91 days and 7.5 hours apart
        tekufa_delta = datetime.timedelta(
            days=interval_days,
            hours=int(interval_hours),
            minutes=int((interval_hours - int(interval_hours)) * 60),
        )

        # From Nissan to Tevet (minus interval)
        self.tekufa_tevet = self.tekufa_nissan - tekufa_delta
        self.tekufa_tishrei = self.tekufa_tevet - tekufa_delta
        self.tekufa_tammuz = self.tekufa_nissan + tekufa_delta

    def get_cheilat_geshamim(
        self,
    ):
        """
        Calculates the start date for the prayers for rain (Cheilat Geshamim).
        In the diaspora, it is 60 days (add 59 days) after Tekufat Tishrei.
        In Israel, it is fixed at the 7th of Cheshvan.
        """

        # Ensure we have Tekufa Tishrei
        # if not hasattr(self, "tekufa_tishrei") or self.tekufa_tishrei is None:
        #    self.cheilat_geshamim = None
        #    return

        if self.diaspora:
            # Cheilat Geshamim starts 60 days after Tekufat Tishrei.
            cheilat_geshamim = self.tekufa_tishrei + datetime.timedelta(days=59)
            self.cheilat_geshamim = cheilat_geshamim

            time_end_of_day = Zmanim(
                self.cheilat_geshamim, location=self.location
            ).zmanim["first_stars"]

            tz = time_end_of_day.tzinfo

            cheilat_geshamim_dt = datetime.datetime(
                cheilat_geshamim.year,
                cheilat_geshamim.month,
                cheilat_geshamim.day,
                cheilat_geshamim.hour,
                cheilat_geshamim.minute,
                tzinfo=tz,
            )

            if cheilat_geshamim_dt < time_end_of_day:
                # Normalize to date at midnight
                self.cheilat_geshamim = cheilat_geshamim_dt.date()
            else:
                self.cheilat_geshamim = cheilat_geshamim_dt.date() + datetime.timedelta(
                    days=1
                )
        else:
            # In Israel: 7th of Cheshvan
            hdate_7_cheshvan = HebrewDate(self.hebrew_year_p, 2, 7)
            jdn_7_cheshvan = conv.hdate_to_jdn(hdate_7_cheshvan)
            self.cheilat_geshamim = conv.jdn_to_gdate(jdn_7_cheshvan)

    def set_prayer_periods(self) -> None:
        """
        Defines the prayer periods based on the calculated dates.
        """

        # Shemini Atzeret of current Hebrew year
        hdate_shemini_atzeret = HebrewDate(self.hebrew_year_p, 1, 22)
        jdn_shemini_atzeret = conv.hdate_to_jdn(hdate_shemini_atzeret)
        self.shemini_atzeret = conv.jdn_to_gdate(jdn_shemini_atzeret)

        # Shemini Atzeret of next Hebrew year
        hdate_next_shemini_atzeret = HebrewDate(self.hebrew_year_p + 1, 1, 22)
        jdn_next_shemini_atzeret = conv.hdate_to_jdn(hdate_next_shemini_atzeret)
        self.next_shemini_atzeret = conv.jdn_to_gdate(jdn_next_shemini_atzeret)

        # 7th of Cheshvan current Hebrew year
        hdate_7_cheshvan = HebrewDate(self.hebrew_year_p, 2, 7)
        jdn_7_cheshvan = conv.hdate_to_jdn(hdate_7_cheshvan)
        self.seventh_cheshvan = conv.jdn_to_gdate(jdn_7_cheshvan)

        # Previous year's Pesach (15 Nissan)
        hdate_prev_pesach = HebrewDate(self.hebrew_year_p - 1, 7, 15)
        jdn_prev_pesach = conv.hdate_to_jdn(hdate_prev_pesach)
        self.prev_pesach = conv.jdn_to_gdate(jdn_prev_pesach)

        # Current year's Pesach
        hdate_pesach = HebrewDate(self.hebrew_year_p, 7, 15)
        jdn_pesach = conv.hdate_to_jdn(hdate_pesach)
        self.pesach = conv.jdn_to_gdate(jdn_pesach)

        # Define the prayer periods
        self.prayer_periods = [
            ("prev_pessah_to_shemini", self.prev_pesach, self.shemini_atzeret),
            ("shemini_to_cheshvan", self.shemini_atzeret, self.seventh_cheshvan),
            ("cheshvan_to_geshamim", self.seventh_cheshvan, self.cheilat_geshamim),
            ("geshamim_to_pessah", self.cheilat_geshamim, self.pesach),
            ("pessah_to_shemini_next", self.pesach, self.next_shemini_atzeret),
        ]

    def get_prayer_for_date(
        self,
        date: Union[datetime.date, str, datetime.datetime] = datetime.datetime.now(),
        tradition: str = "israel",
        language: str = "english",
    ) -> str:
        """
        Returns the appropriate prayer phrases for the given date, tradition,
        and language. The tradition can be
        'israel',
        'diaspora_ashkenazi',
        or 'diaspora_sephardi'.
        The language can be 'english', 'french', or 'hebrew'.
        """
        if isinstance(date, str):
            # If a string is given, parse it into a date/datetime if needed.
            # For now, assume YYYY-MM-DD format.
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        elif isinstance(date, datetime.datetime):
            date = date.date()

        if date is None:
            date = self.date

        for period_name, start_date, end_date in self.prayer_periods:
            if start_date and end_date:
                if start_date <= date < end_date:
                    tradition_data = PRAYER_DESCRIPTIONS.get(period_name)
                    if tradition_data:
                        lang_data = getattr(tradition_data, tradition, None)
                        if lang_data:
                            return getattr(
                                lang_data, language, "No phrase for this language."
                            )
        return "No prayer phrase found for this date, tradition, and language."

    def get_results(self) -> dict[str, object]:
        """
        Returns a dictionary containing all the calculated dates and times.
        """
        return {
            "date": self.date,
            "gregorian_year": self.gregorian_year,
            "hebrew_year": self.hebrew_year,
            "hebrew_year_p": self.hebrew_year_p,
            "diaspora": self.diaspora,
            "tekufa_tishrei": getattr(self, "tekufa_tishrei", None),
            "tekufa_tevet": getattr(self, "tekufa_tevet", None),
            "tekufa_nissan": self.tekufa_nissan,
            "tekufa_tammuz": getattr(self, "tekufa_tammuz", None),
            "cheilat_geshamim": getattr(self, "cheilat_geshamim", None),
            "seventh_cheshvan": getattr(self, "seventh_cheshvan", None),
            "prev_pesach": getattr(self, "prev_pesach", None),
            "shemini_atzeret": getattr(self, "shemini_atzeret", None),
            "pesach": getattr(self, "pesach", None),
            "next_shemini_atzeret": getattr(self, "next_shemini_atzeret", None),
        }
