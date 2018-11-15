# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import random

import pytest

import hdate.converters as conv
from hdate import HDate, HebrewDate

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic

HEBREW_YEARS_INFO = {
    # year, dow rosh hashana, length, dow pesach
    5753: (2, 353, 3), 5773: (2, 353, 3), 5777: (2, 353, 3),
    5756: (2, 355, 5), 5759: (2, 355, 5), 5780: (2, 355, 5), 5783: (2, 355, 5),
    5762: (3, 354, 5), 5766: (3, 354, 5), 5769: (3, 354, 5),
    5748: (5, 354, 7), 5751: (5, 354, 7), 5758: (5, 354, 7), 5772: (5, 354, 7),
    5775: (5, 354, 7), 5778: (5, 354, 7),
    5754: (5, 355, 1), 5785: (5, 355, 1),
    5761: (7, 353, 1), 5781: (7, 353, 1),
    5750: (7, 355, 3), 5764: (7, 355, 3), 5767: (7, 355, 3), 5770: (7, 355, 3),
    5788: (7, 355, 3),
    5749: (2, 383, 5), 5790: (2, 383, 5),
    5752: (2, 385, 7), 5776: (2, 385, 7), 5779: (2, 385, 7),
    5755: (3, 384, 7), 5782: (3, 384, 7),
    5765: (5, 383, 1), 5768: (5, 383, 1), 5812: (5, 383, 1),
    5744: (5, 385, 3), 5771: (5, 385, 3), 5774: (5, 385, 3),
    5757: (7, 383, 3), 5784: (7, 383, 3),
    5760: (7, 385, 5), 5763: (7, 385, 5), 5787: (7, 385, 5)
}


class TestHDate(object):

    @pytest.fixture
    def default_values(self):
        return HDate()

    def test_assign_bad_hdate_value(self):
        bad_month_value = HebrewDate(5779, 15, 3)
        bad_day_value = HebrewDate(5779, 10, 35)
        with pytest.raises(TypeError):
            HDate().hdate = "not a HebrewDate"
        with pytest.raises(ValueError):
            HDate().hdate = bad_month_value
        with pytest.raises(ValueError):
            HDate().hdate = bad_day_value

    @pytest.mark.parametrize('execution_number', list(range(10)))
    def test_random_hdate(self, execution_number, rand_date):
        _hdate = HDate()
        _hdate.hdate = rand_date.hdate
        assert _hdate._jdn == rand_date._jdn
        assert _hdate.hdate == rand_date.hdate
        assert _hdate.gdate == rand_date.gdate

    def test_conv_get_size_of_hebrew_year(self):
        for year, info in list(HEBREW_YEARS_INFO.items()):
            assert conv.get_size_of_hebrew_year(year) == info[1]

    @pytest.mark.parametrize('execution_number', list(range(10)))
    def test_hdate_get_size_of_hebrew_years(self, execution_number,
                                            rand_date):
        assert (rand_date.year_size() ==
                conv.get_size_of_hebrew_year(rand_date.hdate.year))

    def test_rosh_hashana_day_of_week(self, rand_date):
        for year, info in list(HEBREW_YEARS_INFO.items()):
            rand_date.hdate = HebrewDate(
                year, rand_date.hdate.month, rand_date.hdate.day)
            assert rand_date.rosh_hashana_dow() == info[0]

    def test_pesach_day_of_week(self, rand_date):
        for year, info in list(HEBREW_YEARS_INFO.items()):
            rand_date.hdate = HebrewDate(year, 7, 15)
            assert rand_date.dow == info[2]
            assert rand_date._holiday_entry().index == 15


class TestSpecialDays(object):

    NON_MOVING_HOLIDAYS = [
        ((1, 1), 1, "Rosh Hashana"),
        ((2, 1), 2, "Rosh Hashana II"),
        ((9, 1), 37, "Erev Yom Kippur"),
        ((10, 1), 4, "Yom Kippur"),
        ((15, 1), 5, "Sukkot"),
        ((17, 1), 6, "Chol Hamoed Sukkot"),
        ((18, 1), 6, "Chol Hamoed Sukkot"),
        ((19, 1), 6, "Chol Hamoed Sukkot"),
        ((20, 1), 6, "Chol Hamoed Sukkot"),
        ((21, 1), 7, "Hoshana Raba"),
        ((22, 1), 27, "Shmini Atseret"),
        ((15, 7), 15, "Pesach"),
        ((17, 7), 16, "Chol Hamoed Pesach"),
        ((18, 7), 16, "Chol Hamoed Pesach"),
        ((19, 7), 16, "Chol Hamoed Pesach"),
        ((20, 7), 16, "Chol Hamoed Pesach"),
        ((21, 7), 28, "Shvi'i shel Pesach"),
        ((5, 9), 19, "Erev Shavuot"),
        ((6, 9), 20, "Shavuot"),

        ((25, 3), 9, "Chanuka"),
        ((26, 3), 9, "Chanuka"),
        ((27, 3), 9, "Chanuka"),
        ((28, 3), 9, "Chanuka"),
        ((29, 3), 9, "Chanuka"),
        ((1, 4), 9, "Chanuka"),
        ((2, 4), 9, "Chanuka"),
        ((10, 4), 10, "Asara b'Tevet"),
        ((15, 5), 11, "Tu b'Shvat"),
        ((18, 8), 18, "Lag BaOmer"),
        ((15, 11), 23, "Tu b'Av")
    ]

    DIASPORA_ISRAEL_HOLIDAYS = [
        # Date, holiday in Diaspora, holiday in Israel
        ((16, 1), 31, 6, "Sukkot II"),
        ((23, 1), 8, 0, "Simchat Torah"),
        ((16, 7), 32, 16, "Pesach II"),
        ((22, 7), 29, 0, "Acharon Shel Pesach"),
        ((7, 9), 30, 0, "Shavuot II")
    ]

    MOVING_HOLIDAYS = [
        # Possible dates, test year range, holiday result, name
        ([(3, 1), (4, 1)], (5000, 6500), 3, "Tsom Gedalya"),
        ([(17, 10), (18, 10)], (5000, 6500), 21, "Shiva Asar b'Tamuz"),
        ([(9, 11), (10, 11)], (5000, 6500), 22, "Tisha b'Av"),
        ([(26, 7), (27, 7), (28, 7)], (5719, 6500), 24, "Yom Hasho'a"),
        ([(3, 8), (4, 8), (5, 8)], (5709, 5763), 17, "Yom Ha'atsmaut"),
        ([(3, 8), (4, 8), (5, 8), (6, 8)], (5764, 6500), 17, "Yom Ha'atsmaut"),
        ([(2, 8), (3, 8), (4, 8)], (5709, 5763), 25, "Yom Hazikaron"),
        ([(2, 8), (3, 8), (4, 8), (5, 8)], (5764, 6500), 25, "Yom Hazikaron"),
        ([(28, 8)], (5728, 6500), 26, "Yom Yerushalayim"),
        ([(11, 2), (12, 2)], (5758, 6500), 35, "Rabin Memorial day"),
        ([(29, 10)], (5765, 6500), 36, "Zhabotinsky day"),
        ([(30, 5)], (5000, 6500), 33, "Family day")
    ]

    ADAR_HOLIDAYS = [
        ([11, 13], 12, "Taanit Esther"),
        ([14], 13, "Purim"),
        ([15], 14, "Shushan Purim"),
        ([7], 34, "Memorial day for fallen whose place of burial is unknown"),
    ]

    @pytest.mark.parametrize('date, holiday, name', NON_MOVING_HOLIDAYS)
    def test_get_holidays_non_moving(self, rand_date, date, holiday, name):
        rand_date.hdate = HebrewDate(rand_date.hdate.year, date[1], date[0])
        assert rand_date._holiday_entry().index == holiday

    @pytest.mark.parametrize('date, diaspora_holiday, israel_holiday, name',
                             DIASPORA_ISRAEL_HOLIDAYS)
    def test_get_diaspora_israel_holidays(self, rand_date, date,
                                          diaspora_holiday, israel_holiday,
                                          name):
        rand_date.hdate = HebrewDate(rand_date.hdate.year, date[1], date[0])
        assert rand_date._holiday_entry().index == israel_holiday
        rand_date.diaspora = True
        assert rand_date._holiday_entry().index == diaspora_holiday

    @pytest.mark.parametrize('possible_dates, years, holiday, name',
                             MOVING_HOLIDAYS)
    def test_get_holidays_moving(self, possible_dates, years, holiday, name):
        found_matching_holiday = False
        year = random.randint(*years)

        print("Testing " + name + " for " + str(year))

        for date in possible_dates:
            date_under_test = HDate(hebrew=False)
            date_under_test.hdate = HebrewDate(year, date[1], date[0])
            if date_under_test._holiday_entry().index == holiday:
                print("date ", date_under_test, " matched")
                for other in possible_dates:
                    if other != date:
                        other_date = HDate(hebrew=False)
                        other_date.hdate = HebrewDate(year, other[1], other[0])
                        print("checking ", other_date, " doesn't match")
                        assert other_date._holiday_entry().index != holiday
                found_matching_holiday = True

        assert found_matching_holiday

        # Test holiday == 0 before 'since'
        # In case of yom hazikaron and yom ha'atsmaut don't test for the
        # case of 0 between 5708 and 5764
        if years[0] != 5000:
            if years[0] == 5764 and holiday in [17, 25]:
                return
            year = random.randint(5000, years[0] - 1)
            print("Testing " + name + " for " + str(year))
            for date in possible_dates:
                date_under_test = HDate()
                date_under_test.hdate = HebrewDate(year, date[1], date[0])
                assert date_under_test._holiday_entry().index == 0

    def test_get_holiday_hanuka_3rd_tevet(self):
        year = random.randint(5000, 6000)
        year_size = conv.get_size_of_hebrew_year(year)
        myhdate = HDate()
        myhdate.hdate = HebrewDate(year, 4, 3)
        print(year_size)
        if year_size in [353, 383]:
            assert myhdate._holiday_entry().index == 9
        else:
            assert myhdate._holiday_entry().index == 0

    @pytest.mark.parametrize('possible_days, holiday, name', ADAR_HOLIDAYS)
    def test_get_holiday_adar(self, possible_days, holiday, name):
        year = random.randint(5000, 6000)
        year_size = conv.get_size_of_hebrew_year(year)
        month = 6 if year_size < 360 else 14
        myhdate = HDate()

        for day in possible_days:
            myhdate.hdate = HebrewDate(year, month, day)
            if day == 13 and myhdate.dow == 7 and holiday == 12:
                assert myhdate._holiday_entry().index == 0
            elif day == 11 and myhdate.dow != 5 and holiday == 12:
                assert myhdate._holiday_entry().index == 0
            else:
                assert myhdate._holiday_entry().index == holiday

    @pytest.mark.parametrize('execution_number', list(range(10)))
    def test_get_omer_day(self, execution_number, rand_date):
        if (rand_date.hdate.month not in [7, 8, 9] or
                rand_date.hdate.month == 7 and rand_date.hdate.day < 16 or
                rand_date.hdate.month == 9 and rand_date.hdate.day > 5):
            assert rand_date.omer_day == 0

        nissan = list(range(16, 30))
        iyyar = list(range(1, 29))
        sivan = list(range(1, 5))

        for day in nissan:
            rand_date.hdate = HebrewDate(rand_date.hdate.year, 7, day)
            assert rand_date.omer_day == day - 15
        for day in iyyar:
            rand_date.hdate = HebrewDate(rand_date.hdate.year, 8, day)
            assert rand_date.omer_day == day + 15
        for day in sivan:
            rand_date.hdate = HebrewDate(rand_date.hdate.year, 9, day)
            assert rand_date.omer_day == day + 44


class TestHDateReading(object):

    READINGS_FOR_YEAR_DIASPORA = [
        # שנים מעוברות
        # זשה
        (5763, [[0, 53, 0], list(range(29)), [0], list(range(29, 35)), [0],
                list(range(35, 39)), [59, 41, 60], list(range(44, 51)), [61]]),
        # זחג
        (5757, [[0, 53, 0], list(range(29)), [0], list(range(29, 42)), [60],
                list(range(44, 51)), [61]]),
        # השג
        (5774, [[53, 0], list(range(30)), [0], list(range(30, 51)), [61]]),
        # החא
        (5768, [[53, 0], list(range(30)), [0], list(range(30, 51))]),
        # גכז
        (5755, [[52, 53], list(range(29)), [0, 0], list(range(29, 42)), [60],
                list(range(44, 51))]),
        # בשז
        (5776, [[52, 53], list(range(29)), [0, 0], list(range(29, 42)), [60],
                list(range(44, 51))]),
        # בחה
        (5749, [[52, 53], list(range(29)), [0], list(range(29, 35)), [0],
                list(range(35, 39)), [59, 41, 60], list(range(44, 51)), [61]]),
        # שנים פשוטות
        # השא
        (5754, [[53, 0], list(range(26)), [0, 26, 56, 57, 31, 58],
                list(range(34, 42)), [60], list(range(44, 54))]),
        # בשה
        (5756, [[52, 53], list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58, 34, 0],
                list(range(35, 39)), [59, 41, 60], list(range(44, 51)), [61]]),
        # זחא
        (5761, [[0, 53, 0], list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58], list(range(34, 42)), [60],
                list(range(44, 52))]),
        # גכה
        (5769, [[52, 53], list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58, 34, 0],
                list(range(35, 39)), [59, 41, 60], list(range(44, 51)), [61]]),
        # זשג
        (5770, [[0, 53, 0], list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58], list(range(34, 42)), [60],
                list(range(44, 51)), [61]]),
        # הכז
        (5775, [[53, 0], list(range(22)),
                [55, 24, 25, 0, 0, 26, 56, 57, 31, 58], list(range(34, 42)),
                [60], list(range(44, 51))]),
        # בחג
        (5777, [[52, 53], list(range(22)), [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)), [60], list(range(44, 51)), [61]])
    ]

    READINGS_FOR_YEAR_ISRAEL = [
        # שנים מעוברות
        # זשה
        (5763, [[0, 53, 0, 54], list(range(1, 29)), [0], list(range(29, 42)),
                [60], list(range(44, 51)), [61]]),
        # זחג
        (5757, [[0, 53, 0, 54], list(range(1, 29)), [0], list(range(29, 42)),
                [60], list(range(44, 51)), [61]]),
        # השג
        (5774, [[53, 0], list(range(30)), [0], list(range(30, 51)), [61]]),
        # החא
        (5768, [[53, 0], list(range(30)), [0], list(range(30, 51))]),
        # גכז
        (5755, [[52, 53], list(range(29)), [0], list(range(29, 51))]),
        # בשז
        (5776, [[52, 53], list(range(29)), [0], list(range(29, 51))]),
        # בחה
        (5749, [[52, 53], list(range(29)), [0], list(range(29, 42)), [60],
                list(range(44, 51)), [61]]),
        # שנים פשוטות
        # השא
        (5754, [[53, 0], list(range(26)), [0, 26, 56, 57, 31, 58],
                list(range(34, 42)), [60], list(range(44, 54))]),
        # בשה
        (5756, [[52, 53], list(range(22)), [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)), [60], list(range(44, 51)), [61]]),
        # זחא
        (5761, [[0, 53, 0, 54], list(range(1, 22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58], list(range(34, 42)), [60],
                list(range(44, 52))]),
        # גכה
        (5769, [[52, 53], list(range(22)), [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)), [60], list(range(44, 51)), [61]]),
        # זשג
        (5770, [[0, 53, 0, 54], list(range(1, 22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58], list(range(34, 42)), [60],
                list(range(44, 51)), [61]]),
        # הכז
        (5775, [[53, 0], list(range(22)), [55, 24, 25, 0, 26, 56, 57],
                list(range(31, 42)), [60], list(range(44, 52))]),
        # בחג
        (5777, [[52, 53], list(range(22)), [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)), [60], list(range(44, 51)), [61]])
    ]

    @pytest.mark.parametrize("year, parshiyot", READINGS_FOR_YEAR_ISRAEL)
    def test_get_reading_israel(self, year, parshiyot):
        mydate = HDate(hebrew=False, diaspora=False)
        mydate.hdate = HebrewDate(year, 1, 1)

        # Get next Saturday
        tdelta = datetime.timedelta((12 - mydate.gdate.weekday()) % 7)
        mydate.gdate += tdelta

        shabatot = [item for subl in parshiyot for item in subl]
        for shabat in shabatot:
            print("Testing: ", mydate)
            assert mydate.get_reading() == shabat
            mydate.gdate += datetime.timedelta(days=7)
        mydate.hdate = HebrewDate(year, 1, 22)
        # VeZot Habracha in Israel always falls on 22 of Tishri
        assert mydate.get_reading() == 54

    @pytest.mark.parametrize("year, parshiyot", READINGS_FOR_YEAR_DIASPORA)
    def test_get_reading_diaspora(self, year, parshiyot):
        mydate = HDate(hebrew=False, diaspora=True)
        mydate.hdate = HebrewDate(year, 1, 1)

        # Get next Saturday
        tdelta = datetime.timedelta((12 - mydate.gdate.weekday()) % 7)
        mydate.gdate += tdelta

        shabatot = [item for subl in parshiyot for item in subl]
        for shabat in shabatot:
            print("Testing: ", mydate)
            assert mydate.get_reading() == shabat
            mydate.gdate += datetime.timedelta(days=7)
        mydate.hdate = HebrewDate(year, 1, 23)
        # VeZot Habracha in Israel always falls on 22 of Tishri
        assert mydate.get_reading() == 54
