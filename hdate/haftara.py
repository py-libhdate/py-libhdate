"""Haftara module, contains Haftara lookup information and related functions."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import IntEnum, auto

from hdate.hebrew_date import HebrewDate, Months, Weekday, is_leap_year
from hdate.parasha import Parasha, ParashaDatabase
from hdate.translator import TranslatorMixin


class Haftara(TranslatorMixin, IntEnum):
    """Haftara enum."""

    NONE = 0
    BERESHIT = auto()
    NOACH = auto()
    LECH_LECHA = auto()
    VAYERA = auto()
    CHAYEI_SARA = auto()
    TOLDOT = auto()
    VAYETZEI = auto()
    VAYISHLACH = auto()
    VAYESHEV = auto()
    MIKETZ = auto()
    VAYIGASH = auto()
    VAYECHI = auto()
    SHEMOT = auto()
    VAERA = auto()
    BO = auto()
    BESHALACH = auto()
    YITRO = auto()
    MISHPATIM = auto()
    TERUMAH = auto()
    TETZAVEH = auto()
    KI_TISA = auto()
    VAYAKHEL = auto()
    PEKUDEI = auto()
    VAYIKRA = auto()
    TZAV = auto()
    SHMINI = auto()
    TAZRIA = auto()
    METZORA = auto()
    ACHREI_MOT = auto()
    KEDOSHIM = auto()
    EMOR = auto()
    BEHAR = auto()
    BECHUKOTAI = auto()
    BAMIDBAR = auto()
    NASSO = auto()
    BEHAALOTCHA = auto()
    SHLACH = auto()
    KORACH = auto()
    CHUKAT = auto()
    BALAK = auto()
    PINCHAS = auto()
    MATOT = auto()
    MASEI = auto()
    DEVARIM = auto()
    VAETCHANAN = auto()
    EIKEV = auto()
    REEH = auto()
    SHOFTIM = auto()
    KI_TEITZEI = auto()
    KI_TAVO = auto()
    NITZAVIM = auto()
    VAYEILECH = auto()
    HAAZINU = auto()
    VEZOT_HABRACHA = auto()
    VAYAKHEL_PEKUDEI = auto()
    TAZRIA_METZORA = auto()
    ACHREI_MOT_KEDOSHIM = auto()
    BEHAR_BECHUKOTAI = auto()
    CHUKAT_BALAK = auto()
    MATOT_MASEI = auto()
    NITZAVIM_VAYEILECH = auto()

    # Special Haftarot
    SHEKALIM = auto()
    ZACHOR = auto()
    PARAH = auto()
    HACHODESH = auto()
    SHABBAT_ROSH_CHODESH = auto()
    MACHAR_CHODESH = auto()
    HANUKKAH_1 = auto()
    HANUKKAH_2 = auto()
    SHABBAT_HAGADOL = auto()
    SHABBAT_SHUVA = auto()
    ROSH_HASHANA_1 = auto()
    ROSH_HASHANA_2 = auto()
    YOM_KIPPUR_SHACHARIT = auto()
    YOM_KIPPUR_MINCHA = auto()
    SUKKOT_1 = auto()
    SUKKOT_2 = auto()
    SHABBAT_HOL_HAMOED_SUKKOT = auto()
    SHEMINI_ATZERET = auto()
    SIMCHAT_TORAH = auto()
    PESACH_1 = auto()
    PESACH_2 = auto()
    SHABBAT_HOL_HAMOED_PESACH = auto()
    PESACH_7 = auto()
    PESACH_8 = auto()
    SHAVUOT_1 = auto()
    SHAVUOT_2 = auto()
    TISHA_BAV_SHACHARIT = auto()
    TISHA_BAV_MINCHA = auto()


@dataclass
class HaftaraDatabase:
    """Container class for haftara information."""

    diaspora: bool

    def lookup(self, date: HebrewDate) -> Haftara:
        """Lookup the haftara for a given date or upcoming Saturday."""
        # 1. Check if date itself is a Yom Tov / Holiday / Fast Day with Haftara
        holiday_haftara = self._lookup_holiday_haftara(date)
        if holiday_haftara != Haftara.NONE:
            return holiday_haftara

        # If date is Saturday, use date. Otherwise, use upcoming Saturday.
        if date.dow() == Weekday.SATURDAY:
            shabbat_date = date
        else:
            shabbat_date = date + dt.timedelta(days=Weekday.SATURDAY - date.dow())

        # Check if upcoming Shabbat falls on Yom Tov / Holiday
        shabbat_holiday_haftara = self._lookup_holiday_haftara(shabbat_date)
        if shabbat_holiday_haftara != Haftara.NONE:
            return shabbat_holiday_haftara

        # 2. Check Shabbat Overrides

        # 2a. Hanukkah on Shabbat
        hanukkah_haftara = self._lookup_hanukkah_haftara(shabbat_date)
        if hanukkah_haftara != Haftara.NONE:
            return hanukkah_haftara

        # 2b. Four Parashiot (Shekalim, Zachor, Parah, HaChodesh)
        four_parashiot_haftara = self._lookup_four_parashiot_haftara(shabbat_date)
        if four_parashiot_haftara != Haftara.NONE:
            return four_parashiot_haftara

        # 2c. Shabbat Hagadol (Shabbat immediately before Pesach)
        if shabbat_date.month == Months.NISAN and 8 <= shabbat_date.day <= 14:
            return Haftara.SHABBAT_HAGADOL

        # 2d. Shabbat Shuva (Shabbat between Rosh Hashana and Yom Kippur)
        if shabbat_date.month == Months.TISHREI and 2 <= shabbat_date.day <= 9:
            return Haftara.SHABBAT_SHUVA

        # 2e. 3 of Rebuke / 7 of Consolation
        rebuke_consolation_haftara = self._lookup_rebuke_consolation_haftara(
            shabbat_date
        )
        if rebuke_consolation_haftara != Haftara.NONE:
            return rebuke_consolation_haftara

        # 2f. Shabbat Rosh Chodesh
        if shabbat_date.day in (1, 30):
            return Haftara.SHABBAT_ROSH_CHODESH

        # 2g. Shabbat Machar Chodesh (Erev Rosh Chodesh when Rosh Chodesh is Sunday)
        if shabbat_date.day == 29:
            return Haftara.MACHAR_CHODESH

        # 3. Regular Parasha Haftara
        parasha_db = ParashaDatabase(self.diaspora)
        parasha = parasha_db.lookup(shabbat_date)
        if parasha != Parasha.NONE:
            try:
                return Haftara[parasha.name]
            except KeyError:
                return Haftara.NONE

        return Haftara.NONE

    def _lookup_holiday_haftara(self, date: HebrewDate) -> Haftara:
        """Lookup holiday haftara for a specific date."""
        m = date.month
        d = date.day

        if m == Months.TISHREI:
            if d == 1:
                return Haftara.ROSH_HASHANA_1
            if d == 2:
                return Haftara.ROSH_HASHANA_2
            if d == 10:
                return Haftara.YOM_KIPPUR_SHACHARIT
            if d == 15:
                return Haftara.SUKKOT_1
            if d == 16 and self.diaspora:
                return Haftara.SUKKOT_2
            if 16 <= d <= 21 and date.dow() == Weekday.SATURDAY:
                return Haftara.SHABBAT_HOL_HAMOED_SUKKOT
            if d == 22:
                return (
                    Haftara.SHEMINI_ATZERET if self.diaspora else Haftara.SIMCHAT_TORAH
                )
            if d == 23 and self.diaspora:
                return Haftara.SIMCHAT_TORAH

        elif m == Months.NISAN:
            if d == 15:
                return Haftara.PESACH_1
            if d == 16 and self.diaspora:
                return Haftara.PESACH_2
            if 16 <= d <= 20 and date.dow() == Weekday.SATURDAY:
                return Haftara.SHABBAT_HOL_HAMOED_PESACH
            if d == 21:
                return Haftara.PESACH_7
            if d == 22 and self.diaspora:
                return Haftara.PESACH_8

        elif m == Months.SIVAN:
            if d == 6:
                return Haftara.SHAVUOT_1
            if d == 7 and self.diaspora:
                return Haftara.SHAVUOT_2

        elif m == Months.AV:
            # Tisha B'Av (9 Av, or 10 Av if 9th falls on Saturday)
            tisha_bav_day = (
                10
                if HebrewDate(date.year, Months.AV, 9).dow() == Weekday.SATURDAY
                else 9
            )
            if d == tisha_bav_day:
                return Haftara.TISHA_BAV_SHACHARIT

        return Haftara.NONE

    def _lookup_hanukkah_haftara(self, date: HebrewDate) -> Haftara:
        """Check if date falls on Shabbat Hanukkah."""
        if date.dow() != Weekday.SATURDAY:
            return Haftara.NONE

        # Hanukkah starts 25 Kislev
        hanukkah_start = HebrewDate(date.year, Months.KISLEV, 25)
        # Hanukkah lasts 8 days
        days_since_start = (date - hanukkah_start).days
        if 0 <= days_since_start < 8:
            # If there are two Shabbatot in Hanukkah (first one early in Hanukkah)
            if days_since_start >= 7:
                return Haftara.HANUKKAH_2
            return Haftara.HANUKKAH_1

        return Haftara.NONE

    def _lookup_four_parashiot_haftara(self, date: HebrewDate) -> Haftara:
        """Check if date falls on one of the Four Parashiot."""
        is_leap = is_leap_year(date.year)
        adar_month = Months.ADAR_II if is_leap else Months.ADAR

        # Shekalim: Shabbat on or immediately before 1 Adar (or Adar II)
        rosh_chodesh_adar = HebrewDate(date.year, adar_month, 1)
        days_to_rc_adar = (rosh_chodesh_adar - date).days
        if 0 <= days_to_rc_adar <= 6:
            return Haftara.SHEKALIM

        # Zachor: Shabbat immediately before Purim (14 Adar / Adar II)
        purim = HebrewDate(date.year, adar_month, 14)
        days_to_purim = (purim - date).days
        if 1 <= days_to_purim <= 7:
            return Haftara.ZACHOR

        # HaChodesh: Shabbat on or immediately before 1 Nisan
        rosh_chodesh_nisan = HebrewDate(date.year, Months.NISAN, 1)
        days_to_rc_nisan = (rosh_chodesh_nisan - date).days
        if 0 <= days_to_rc_nisan <= 6:
            return Haftara.HACHODESH

        # Parah: Shabbat preceding Shabbat HaChodesh
        # Calculate HaChodesh Shabbat date:
        hachodesh_shabbat_day = (
            1
            if rosh_chodesh_nisan.dow() == Weekday.SATURDAY
            else 1 - rosh_chodesh_nisan.dow()
        )
        hachodesh_shabbat = rosh_chodesh_nisan + dt.timedelta(
            days=(
                hachodesh_shabbat_day - 1
                if rosh_chodesh_nisan.dow() != Weekday.SATURDAY
                else 0
            )
        )
        # Parah is 7 days before HaChodesh Shabbat
        if (hachodesh_shabbat - date).days == 7:
            return Haftara.PARAH

        return Haftara.NONE

    def _lookup_rebuke_consolation_haftara(self, date: HebrewDate) -> Haftara:
        """Check if date falls on 3 of Rebuke or 7 of Consolation."""
        # 17 Tammuz and 9 Av
        tammuz_17 = HebrewDate(date.year, Months.TAMMUZ, 17)
        tisha_bav = HebrewDate(date.year, Months.AV, 9)

        # 3 of Rebuke: Shabbatot after 17 Tammuz and up to 9 Av
        if (date - tammuz_17).days > 0 and (tisha_bav - date).days >= 0:
            days_after_17_tammuz = (date - tammuz_17).days
            shabbat_count = (days_after_17_tammuz + tammuz_17.dow() - 1) // 7
            if shabbat_count == 1:
                return Haftara.MATOT
            if shabbat_count == 2:
                return Haftara.MASEI
            if shabbat_count == 3:
                return Haftara.DEVARIM

        # 7 of Consolation: Shabbatot after 9 Av up to Rosh Hashana
        if (date - tisha_bav).days > 0 and date.month in (Months.AV, Months.ELUL):
            days_after_tisha_bav = (date - tisha_bav).days
            shabbat_count = (days_after_tisha_bav + tisha_bav.dow() - 1) // 7
            consolation_haftarot = [
                Haftara.VAETCHANAN,
                Haftara.EIKEV,
                Haftara.REEH,
                Haftara.SHOFTIM,
                Haftara.KI_TEITZEI,
                Haftara.KI_TAVO,
                Haftara.NITZAVIM,
            ]
            if 1 <= shabbat_count <= 7:
                return consolation_haftarot[shabbat_count - 1]

        return Haftara.NONE
