"""Test the conversion functions."""

import pytest

from hdate import converters as conv
from hdate.hebrew_date import HebrewDate
from hdate.htables import Months


class TestConverters:
    """Tests for converting one date type to another."""

    def test_gdate_to_gdate(self, random_date):
        """ "Transform Gregorian date to Gregorian date."""
        assert conv.jdn_to_gdate(conv.gdate_to_jdn(random_date)) == random_date

    YEARS_PSHUTA = [5753, 5762, 5756]
    YEARS_MEUBERET = [5749, 5755, 5760]

    SIMPLE_MONTHS = {
        29: [Months.TEVET, Months.IYYAR, Months.TAMMUZ, Months.ELUL],
        30: [Months.TISHREI, Months.SHVAT, Months.NISAN, Months.SIVAN, Months.AV],
    }

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_simple(self, year):
        """Transform Hebrew date to Hebrew date (single Adar)."""
        for days_in_month, months in self.SIMPLE_MONTHS.items():
            for month in months:
                for day in range(1, days_in_month + 1):
                    date = HebrewDate(year, month, day)
                    assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_adar(self, year):
        """Transform Hebrew date to Hebrew date (in Adar)."""
        for day in range(1, 29 + 1):
            date = HebrewDate(year, Months.ADAR, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_heshvan(self, year):
        """Transform Hebrew date to hebrew date (Heshvan)."""
        days_in_month = 29 if not year == 5756 else 30
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.MARCHESHVAN, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_kislev(self, year):
        """Transform Hebrew date to hebrew date (Kislev)."""
        days_in_month = 30 if not year == 5753 else 29
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.KISLEV, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_simple(self, year):
        """Transform Hebrew date to hebrew date (two Adars)."""
        for days_in_month, months in self.SIMPLE_MONTHS.items():
            for month in months:
                for day in range(1, days_in_month + 1):
                    date = HebrewDate(year, month, day)
                    assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_adar(self, year):
        """Transform Hebrew date to hebrew date (two Adars - test Adar)."""
        for day in range(1, 30 + 1):
            date = HebrewDate(year, Months.ADAR_I, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date
        for day in range(1, 29 + 1):
            date = HebrewDate(year, Months.ADAR_II, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_heshvan(self, year):
        """Transform Hebrew date to hebrew date (two Adars - test Heshvan)."""
        days_in_month = 29 if not year == 5760 else 30
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.MARCHESHVAN, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_kislev(self, year):
        """Transform Hebrew date to hebrew date (two Adars - test Kislev)."""
        days_in_month = 30 if not year == 5749 else 29
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.KISLEV, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date
