"""
The class attempts to compute:
    - The tekufot (seasons) in the Hebrew calendar: Nissan, Tammuz, Tishrei, and Tevet.
    - Calculaltion are based on Shmuel calendar (Talmud Bavli, Eruvin 56a)
    - Rav Ada’s Tekufah: Closer to the astronomical solar year,
      shorter by 5min than Schmuel (365 days, 5 hours, 997 parts/chalakim) is not used
    - Cheilat Geshamim start date, which differs between the diaspora and Israel.
    - Halachic prayer periods based on key Jewish holidays and seasonal changes.
    - Appropriate prayer phrases depending on the current date, tradition, and language.
"""

import datetime as dt
from datetime import tzinfo
from enum import Enum
from typing import Union

from hdate.hebrew_date import HebrewDate, Months
from hdate.location import Location
from hdate.translator import TranslatorMixin
from hdate.zmanim import Zmanim


class Gevurot(TranslatorMixin, Enum):
    """Enum class for the gevurot."""

    MORID_HATAL = 0
    MASHIV_HARUACH = 1
    NEITHER = 2


class Geshamim(TranslatorMixin, Enum):
    """Enum class for the geshamim."""

    BARKHEINU = 0
    BARECH_ALEINU = 1
    VETEN_TAL = 2
    VETEN_BERACHA = 3


# pylint: disable=too-many-instance-attributes
class Tekufot(TranslatorMixin):
    """
    A class that calculates and manages Jewish seasonal times (Tekufot),
    periods for prayer insertions, and associated halachic dates such as
    the start of Cheilat Geshamim (requesting rain)."""

    def __init__(
        self,
        date: dt.date = dt.datetime.today(),
        location: Location = Location(),
        tradition: str = "sephardi",
        language: str = "english",
    ):
        """Initialize the Tekufot object."""
        super().__init__()

        self.date = date
        self.location = location
        self.tradition = tradition
        self.language = language

        # Convert current date Hebrew Date
        self.hebrew_date = HebrewDate.from_gdate(date)
        self.hebrew_year_p = self.hebrew_date.year
        self.gregorian_year_p = self.hebrew_year_p - 3760

        # Tekufot calculations
        self.get_tekufot()

        # Cheilat Geshamim calculation
        self.get_cheilat_geshamim()

    def get_tekufot(self) -> dict[str, dt.datetime]:
        """
        Calculates the approximate dates and times of the Tekufot.
        This is a simplified approximation. Traditional calculations may differ.
        """

        # Start with Tekufa Nissan:
        # Historically approximated at the spring equinox. For simplicity, assume:
        # If the Hebrew year corresponds to a Gregorian year before 2100
        # we take April 7 as a reference, otherwise April 8

        if self.gregorian_year_p < 2100:
            date_equinox_april = dt.date(self.gregorian_year_p, 4, 7)
        else:
            date_equinox_april = dt.date(self.gregorian_year_p, 4, 8)

        # Hours shift depends on leap year cycles
        hours_delta_nissan = (self.gregorian_year_p % 4) * 6

        # Tekufa Nissan: start at date_equinox_april at 12:00
        tz = self.location.timezone
        if not isinstance(tz, tzinfo):
            raise TypeError("Timezone must be of type tzinfo.")
        tekufa_nissan = dt.datetime.combine(date_equinox_april, dt.time(12, 0)).replace(
            tzinfo=tz
        ) + dt.timedelta(hours=hours_delta_nissan)
        self.tekufa_nissan = tekufa_nissan

        # Tekufa intervals are about 91 days and 7.5 hours apart
        tekufa_interval = dt.timedelta(
            days=91,
            hours=7,
            minutes=30,
        )

        # From Nissan to Tevet (minus interval)
        tekufa_tevet = self.tekufa_nissan - tekufa_interval
        tekufa_tishrei = tekufa_tevet - tekufa_interval
        tekufa_tammuz = self.tekufa_nissan + tekufa_interval

        # Return as dictionary
        return {
            "Tishrei": tekufa_tishrei,
            "Tevet": tekufa_tevet,
            "Nissan": tekufa_nissan,
            "Tammuz": tekufa_tammuz,
        }

    def get_cheilat_geshamim(self) -> dt.date:
        """
        Calculates the start date for the prayers for rain (Cheilat Geshamim).
        In the diaspora, it is 60 days (add 59 days) after Tekufat Tishrei.
        In Israel, it is fixed at the 7th of Cheshvan.
        """

        if self.location.diaspora:
            # Cheilat Geshamim starts 60 days after Tekufat Tishrei.
            cheilat_geshamim_dt = self.get_tekufot()["Tishrei"] + dt.timedelta(days=59)
            time_end_of_day = Zmanim(
                cheilat_geshamim_dt.date(), location=self.location
            ).first_stars.local
            if cheilat_geshamim_dt < time_end_of_day:
                # Normalize to date at midnight
                cheilat_geshamim = cheilat_geshamim_dt.date()
            else:
                cheilat_geshamim = cheilat_geshamim_dt.date() + dt.timedelta(days=1)
        else:
            # In Israel: 7th of Cheshvan
            hdate_7_cheshvan = HebrewDate(self.hebrew_year_p, Months.MARCHESHVAN, 7)
            cheilat_geshamim = HebrewDate.to_gdate(hdate_7_cheshvan)

        return cheilat_geshamim

    def get_cheilat_geshamim_hdate(self) -> HebrewDate:
        """
        Convert Cheilat Geshamim in Hebrew date.
        """
        cheilat_geshamim_hdate = HebrewDate.from_gdate(self.get_cheilat_geshamim())

        return cheilat_geshamim_hdate

    def get_gevurot(self) -> Union[Gevurot, None]:
        """
        From Pesach to Shemini Atzeret:
          Sephardi: Morid (0)
          Ashkenazi: neither (2)
        From Shemini Atzeret to Next Pesach:
          All: Mashiv (1)
        """
        # Prev Pesach to Shemini Atzeret
        if (
            HebrewDate(self.hebrew_year_p - 1, Months.NISAN, 15)
            < self.hebrew_date
            < HebrewDate(self.hebrew_year_p, Months.TISHREI, 22)
        ):
            if self.tradition in ["sephardi"]:
                return Gevurot.MORID_HATAL

            # diaspora_ashkenazi
            return Gevurot.NEITHER  # neither = 2

        # Shemini Atzeret to Pesach
        if (
            HebrewDate(self.hebrew_year_p, Months.TISHREI, 22)
            < self.hebrew_date
            < HebrewDate(self.hebrew_year_p, Months.NISAN, 15)
        ):
            return Gevurot.MASHIV_HARUACH

        # Pesach to Next Shemini Atzeret
        if (
            HebrewDate(self.hebrew_year_p, Months.NISAN, 15)
            < self.hebrew_date
            < HebrewDate(self.hebrew_year_p + 1, Months.TISHREI, 22)
        ):
            if self.tradition in ["sephardi"]:
                return Gevurot.MORID_HATAL  # Morid = 0

            # ashkenazi
            return Gevurot.NEITHER  # neither = 2

        # Default
        return None

    def get_geshamim(self) -> Union[Geshamim, None]:
        """
        Periods:
        From Pesach I (Musaf) to Cheilat geshamim
        Cheilat geshamim to Pesach I (Shacharit)
        """

        # From Prev Pesach to Cheilat geshamim:
        if (
            HebrewDate(self.hebrew_year_p - 1, Months.NISAN, 15)
            < self.hebrew_date
            < self.get_cheilat_geshamim_hdate()
        ):
            if self.tradition in ["sephardi"]:
                return Geshamim.BARKHEINU
            return Geshamim.VETEN_BERACHA

        # From Cheilat geshamim to Pesach:
        if (
            self.get_cheilat_geshamim_hdate()
            < self.hebrew_date
            < HebrewDate(self.hebrew_year_p, Months.NISAN, 15)
        ) or (self.hebrew_date == self.get_cheilat_geshamim_hdate()):
            if self.tradition in ["sephardi"]:
                return Geshamim.BARECH_ALEINU
            return Geshamim.VETEN_TAL

        if self.tradition in ["sephardi"]:
            return Geshamim.BARKHEINU
        return Geshamim.VETEN_BERACHA

    def get_prayer_for_date(self) -> str:
        """
        Returns the appropriate prayer phrases for the given date, tradition,
        and language. The tradition can be 'ashkenazi', "sephardi'.
        The language can be 'english', 'french', or 'hebrew'.
        """
        self.set_language(self.language)
        geshamim = self.get_geshamim()
        gevurot = self.get_gevurot()
        if geshamim is not None:
            geshamim.set_language(self.language)

        if gevurot is not None:
            gevurot.set_language(self.language)

        return f"{gevurot} - {geshamim}"
