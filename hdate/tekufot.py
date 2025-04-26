"""
The class attempts to compute:
    - The tekufot (seasons) in the Hebrew calendar: Nissan, Tammuz, Tishrei, and Tevet.
    - Calculaltion are based on Shmuel calendar (Talmud Bavli, Eruvin 56a)
    - Rav Ada’s Tekufah: Closer to the astronomical solar year,
      shorter by 5min than Schmuel (365 days, 5 hours, 997 parts/chalakim) is not used
    - Cheilat Geshamim start date, which differs between the diaspora and Israel.
    - Halachic prayer periods based on key Jewish holidays and seasonal changes.
    - Appropriate prayer phrases depending on the current date and tradition.
"""

import datetime as dt
import typing
from calendar import isleap
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from hdate.hebrew_date import HebrewDate, Months
from hdate.translator import TranslatorMixin


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


Nusachim = Literal["sephardi", "ashkenazi"]
TekufotNames = Literal["Tishrei", "Tevet", "Nissan", "Tammuz"]


@dataclass
class Tekufot(TranslatorMixin):
    """
    A class that calculates and manages Jewish seasonal times (Tekufot),
    periods for prayer insertions, and associated halachic dates such as
    the start of Cheilat Geshamim (requesting rain)."""

    date: dt.date = field(default_factory=dt.date.today)
    diaspora: bool = False
    tradition: Nusachim = "sephardi"

    def __post_init__(self) -> None:
        # Convert current date Hebrew Date
        self.hebrew_date = HebrewDate.from_gdate(self.date)
        self.hebrew_year_p = self.hebrew_date.year
        self.gregorian_year_p = self.hebrew_year_p - 3760

    def get_tekufa(self, name: TekufotNames) -> dt.datetime:
        """Calculate the approximate dates and times of the Tekufot.

        This is a simplified approximation. Traditional calculations may differ.
        """
        if name not in typing.get_args(TekufotNames):
            raise ValueError(f"Invalid Tekufot name: {name}")

        # Start with Tekufa Nissan:
        # Historically approximated at the spring equinox.
        # Every 100 years, moves by a single day, unless it's a year divisible by 400
        # For years between 1900 and 2100, it's April 7th

        _gregorian_year_p = self.gregorian_year_p // 100
        _gregorian_year_p -= _gregorian_year_p // 4
        equinox_day = _gregorian_year_p - 8

        date_equinox_april = dt.date(self.gregorian_year_p, 4, equinox_day)

        # Hours shift depends on leap year cycles
        hours_delta_nissan = (self.gregorian_year_p % 4) * 6

        # Tekufa Nissan: start at date_equinox_april at 12:00
        tekufa_nissan = dt.datetime.combine(
            date_equinox_april, dt.time(12, 0)
        ) + dt.timedelta(hours=hours_delta_nissan)

        # Tekufa intervals are about 91 days and 7.5 hours apart
        tekufa_interval = dt.timedelta(days=91, hours=7, minutes=30)

        # From Nissan to Tevet (minus interval)
        values = {
            "Nissan": tekufa_nissan,
            "Tevet": (tekufa_tevet := tekufa_nissan - tekufa_interval),
            "Tishrei": tekufa_tevet - tekufa_interval,
            "Tammuz": tekufa_nissan + tekufa_interval,
        }
        return values[name]

    @property
    def tchilat_geshamim(self) -> HebrewDate:
        """
        Calculates the start date for the prayers for rain (Cheilat Geshamim).
        In the diaspora, it is 60 days (add 59 days) after Tekufat Tishrei.
        In Israel, it is fixed at the 7th of Cheshvan.
        """

        if self.diaspora:
            # Cheilat Geshamim starts 60 days after Tekufat Tishrei.
            cheilat_geshamim_dt = self.get_tekufa("Tishrei") + dt.timedelta(days=59)
            if isleap(cheilat_geshamim_dt.year + 1):
                # If next year is a leap year, add an extra day since the day that will
                # be added to the upcoming month of February has already been
                # accumulated.
                cheilat_geshamim_dt += dt.timedelta(days=1)
            cheilat_geshamim = HebrewDate.from_gdate(cheilat_geshamim_dt.date())
        else:
            # In Israel: 7th of Cheshvan
            cheilat_geshamim = HebrewDate(self.hebrew_year_p, Months.MARCHESHVAN, 7)

        return cheilat_geshamim

    def get_gevurot(self) -> Gevurot:
        """
        From Pesach to Shemini Atzeret:
          Sephardi: Morid (0)
          Ashkenazi: neither (2)
        From Shemini Atzeret to Next Pesach:
          All: Mashiv (1)
        """
        shmini_atseret = HebrewDate(0, Months.TISHREI, 22)
        pesach = HebrewDate(0, Months.NISAN, 15)
        if shmini_atseret <= self.hebrew_date < pesach:
            return Gevurot.MASHIV_HARUACH

        if self.diaspora and self.tradition == "ashkenazi":
            return Gevurot.NEITHER

        # Default according to most traditions
        return Gevurot.MORID_HATAL

    def get_geshamim(self) -> Geshamim:
        """
        Periods:
        From Pesach I (Musaf) to Cheilat geshamim
        Cheilat geshamim to Pesach I (Shacharit)
        """
        pesach = HebrewDate(0, Months.NISAN, 15)

        if self.tchilat_geshamim <= self.hebrew_date < pesach:
            if self.tradition in ["sephardi"]:
                return Geshamim.BARECH_ALEINU
            return Geshamim.VETEN_TAL

        if self.tradition in ["sephardi"]:
            return Geshamim.BARKHEINU
        return Geshamim.VETEN_BERACHA

    def get_prayer_for_date(self) -> str:
        """
        Returns the appropriate prayer phrases for the given date,
        and tradition. The tradition can be 'ashkenazi', "sephardi'.
        """
        geshamim = self.get_geshamim()
        gevurot = self.get_gevurot()

        return f"{gevurot} - {geshamim}"
