# -*- coding: utf-8 -*-
"""Test the conversion functions."""
import pytest

from hdate import converters as conv
from hdate.common import HebrewDate
from hdate.htables import Months


class TestConverters(object):
    def test_gdate_to_gdate(self, random_date):
        assert conv.jdn_to_gdate(conv.gdate_to_jdn(random_date)) == random_date

    YEARS_PSHUTA = [5753, 5762, 5756]
    YEARS_MEUBERET = [5749, 5755, 5760]

    SIMPLE_MONTHS = {
        29: [Months.Tevet, Months.Iyyar, Months.Tammuz, Months.Elul],
        30: [Months.Tishrei, Months.Shvat, Months.Nisan, Months.Sivan, Months.Av],
    }

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_simple(self, year):
        for days_in_month, months in self.SIMPLE_MONTHS.items():
            for month in months:
                for day in range(1, days_in_month + 1):
                    date = HebrewDate(year, month, day)
                    assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_adar(self, year):
        for day in range(1, 29 + 1):
            date = HebrewDate(year, Months.Adar, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_heshvan(self, year):
        days_in_month = 29 if not year == 5756 else 30
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.Marcheshvan, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_PSHUTA)
    def test_hdate_to_hdate_pshuta_kislev(self, year):
        days_in_month = 30 if not year == 5753 else 29
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.Kislev, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_simple(self, year):
        for days_in_month, months in self.SIMPLE_MONTHS.items():
            for month in months:
                for day in range(1, days_in_month + 1):
                    date = HebrewDate(year, month, day)
                    assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_adar(self, year):
        for day in range(1, 30 + 1):
            date = HebrewDate(year, Months.Adar_I, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date
        for day in range(1, 29 + 1):
            date = HebrewDate(year, Months.Adar_II, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_heshvan(self, year):
        days_in_month = 29 if not year == 5760 else 30
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.Marcheshvan, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date

    @pytest.mark.parametrize("year", YEARS_MEUBERET)
    def test_hdate_to_hdate_meuberet_kislev(self, year):
        days_in_month = 30 if not year == 5749 else 29
        for day in range(1, days_in_month + 1):
            date = HebrewDate(year, Months.Kislev, day)
            assert conv.jdn_to_hdate(conv.hdate_to_jdn(date)) == date
