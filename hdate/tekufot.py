"""
The class attempts to compute:
    - The tekufot (seasons) in the Hebrew calendar: Nissan, Tammuz, Tishrei, and Tevet.
    - Cheilat Geshamim start date, which differs between the diaspora and Israel.
    - Halachic prayer periods based on key Jewish holidays and seasonal changes.
    - Appropriate prayer phrases depending on the current date, tradition, and language.
"""

import datetime
from collections import namedtuple
from enum import IntEnum
from typing import Union

from hdate import converters as conv
from hdate.hebrew_date import HebrewDate
from hdate.location import Location
from hdate.translator import TranslatorMixin
from hdate.zmanim import Zmanim

LANG = namedtuple("LANG", ["french", "english", "hebrew"])
TRADITION = namedtuple(
    "TRADITION", ["israel", "diaspora_ashkenazi", "diaspora_sephardi"]
)


class Gevurot(TranslatorMixin, IntEnum):
    """Enum class for the gevurot."""

    MORID = 0
    MASHIV = 1
    NEITHER = 2


class Geshamim(TranslatorMixin, IntEnum):
    """Enum class for the geshamim."""

    BARKHEINU = 0
    BARECH_ALEINU = 1


class Tekufot(TranslatorMixin):  # pylint: disable=too-many-instance-attributes
    """
    A class that calculates and manages Jewish seasonal times (Tekufot),
    periods for prayer insertions, and associated halachic dates such as
    the start of Cheilat Geshamim (requesting rain)."""

    # pylint: disable=R0913, R0917
    def __init__(
        self,
        date: Union[datetime.date, str, datetime.datetime] = datetime.datetime.now(),
        diaspora: bool = False,
        location: Location = Location(),
        tradition: str = "israel",
        language: str = "english",
    ):
        """Initialize the Tekufot object."""
        super().__init__()
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
        self.tradition = tradition
        self.language = language

        # Convert current date to JDN and Hebrew Date
        self.jdn = conv.gdate_to_jdn(date)
        self.hebrew_date = conv.jdn_to_hdate(self.jdn)
        self.hebrew_year_p = self.hebrew_date.year
        self.gregorian_year_p = self.hebrew_year_p - 3760

        # Tekufot calculations
        self.get_tekufa()

        # Cheilat Geshamim calculation
        self.get_cheilat_geshamim()

        # Key date (pessach, shemini)
        self.set_key_date()

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

    def get_cheilat_geshamim(self) -> datetime.date:
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
            _cheilat_geshamim = self.tekufa_tishrei + datetime.timedelta(days=59)

            time_end_of_day = Zmanim(
                _cheilat_geshamim.date(), location=self.location
            ).zmanim["first_stars"]

            tz = time_end_of_day.tzinfo

            cheilat_geshamim_dt = datetime.datetime(
                _cheilat_geshamim.year,
                _cheilat_geshamim.month,
                _cheilat_geshamim.day,
                _cheilat_geshamim.hour,
                _cheilat_geshamim.minute,
                tzinfo=tz,
            )

            if cheilat_geshamim_dt < time_end_of_day:
                # Normalize to date at midnight
                cheilat_geshamim = cheilat_geshamim_dt.date()
            else:
                cheilat_geshamim = cheilat_geshamim_dt.date() + datetime.timedelta(
                    days=1
                )
        else:
            # In Israel: 7th of Cheshvan
            hdate_7_cheshvan = HebrewDate(self.hebrew_year_p, 2, 7)
            jdn_7_cheshvan = conv.hdate_to_jdn(hdate_7_cheshvan)
            cheilat_geshamim = conv.jdn_to_gdate(jdn_7_cheshvan)

        return cheilat_geshamim

    def set_key_date(self) -> None:
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

        # Previous year's Pesach (15 Nissan)
        hdate_prev_pesach = HebrewDate(self.hebrew_year_p - 1, 7, 15)
        jdn_prev_pesach = conv.hdate_to_jdn(hdate_prev_pesach)
        self.prev_pesach = conv.jdn_to_gdate(jdn_prev_pesach)

        # Current year's Pesach
        hdate_pesach = HebrewDate(self.hebrew_year_p, 7, 15)
        jdn_pesach = conv.hdate_to_jdn(hdate_pesach)
        self.pesach = conv.jdn_to_gdate(jdn_pesach)

    def get_gevurot(self) -> Gevurot:
        """
        From Pesach to Shemini Atzeret:
          Israel & Sephardi: Morid (0)
          Ashkenazi: neither (2)
        From Shemini Atzeret to Next Pesach:
          All: Mashiv (1)
        """
        # Prev Pesach to Shemini Atzeret
        if self.prev_pesach <= self.date < self.shemini_atzeret:
            if self.tradition in ["israel", "diaspora_sephardi"]:
                return Gevurot.MORID  # Morid = 0

            # diaspora_ashkenazi
            return Gevurot.NEITHER  # neither = 2

        # Shemini Atzeret to Pesach
        if self.shemini_atzeret <= self.date < self.pesach:
            return Gevurot.MASHIV  # mashiv = 1

        # Pesach to Next Shemini Atzeret
        if self.pesach <= self.date < self.next_shemini_atzeret:
            if self.tradition in ["israel", "diaspora_sephardi"]:
                return Gevurot.MORID  # Morid = 0

            # diaspora_ashkenazi
            return Gevurot.NEITHER  # neither = 2

        # Par défaut (si rien ne correspond, ex. date hors de la plage) :
        return Gevurot.NEITHER

    def get_geshamim(self) -> Geshamim:
        """
        Periods:
        From Pesach I (Musaf) to Cheilat geshamim: All = barkheinu (0)
        Cheilat geshamim to Pesach I (Shacharit): All = barech_aleinu (1)
        At Pesach I (Shacharit): All = barkheinu (0)
        """

        # From Pesach to Cheilat geshamim: All barkheinu (0)
        if self.prev_pesach <= self.date < self.get_cheilat_geshamim():
            return Geshamim.BARKHEINU  # barkheinu = 0

        # From Cheilat geshamim to Pesach: All = barech_aleinu (1)
        if self.get_cheilat_geshamim() <= self.date < self.pesach:
            return Geshamim.BARECH_ALEINU  # barech_aleinu = 1

        # At Pesach (Shacharit): All barkheinu (0)
        if self.date == self.pesach:
            return Geshamim.BARKHEINU

        # Par défaut
        return Geshamim.BARKHEINU

    def get_prayer_for_date(self) -> str:
        """
        Returns the appropriate prayer phrases for the given date, tradition,
        and language. The tradition can be
        'israel',
        'diaspora_ashkenazi',
        or 'diaspora_sephardi'.
        The language can be 'english', 'french', or 'hebrew'.
        """
        self.set_language(self.language)
        geshamim = self.get_geshamim()
        gevurot = self.get_gevurot()
        geshamim.set_language(self.language)
        gevurot.set_language(self.language)

        return f"{gevurot} - {geshamim}"
