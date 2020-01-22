# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import random

import pytest

import hdate.converters as conv
from hdate import HDate, HebrewDate
from hdate.htables import Months

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic

HEBREW_YEARS_INFO = {
    # year, dow rosh hashana, length, dow pesach
    5753: (2, 353, 3),
    5773: (2, 353, 3),
    5777: (2, 353, 3),
    5756: (2, 355, 5),
    5759: (2, 355, 5),
    5780: (2, 355, 5),
    5783: (2, 355, 5),
    5762: (3, 354, 5),
    5766: (3, 354, 5),
    5769: (3, 354, 5),
    5748: (5, 354, 7),
    5751: (5, 354, 7),
    5758: (5, 354, 7),
    5772: (5, 354, 7),
    5775: (5, 354, 7),
    5778: (5, 354, 7),
    5754: (5, 355, 1),
    5785: (5, 355, 1),
    5761: (7, 353, 1),
    5781: (7, 353, 1),
    5750: (7, 355, 3),
    5764: (7, 355, 3),
    5767: (7, 355, 3),
    5770: (7, 355, 3),
    5788: (7, 355, 3),
    5749: (2, 383, 5),
    5790: (2, 383, 5),
    5752: (2, 385, 7),
    5776: (2, 385, 7),
    5779: (2, 385, 7),
    5755: (3, 384, 7),
    5782: (3, 384, 7),
    5765: (5, 383, 1),
    5768: (5, 383, 1),
    5812: (5, 383, 1),
    5744: (5, 385, 3),
    5771: (5, 385, 3),
    5774: (5, 385, 3),
    5757: (7, 383, 3),
    5784: (7, 383, 3),
    5760: (7, 385, 5),
    5763: (7, 385, 5),
    5787: (7, 385, 5),
}


class TestHDate(object):
    @pytest.fixture
    def default_values(self):
        return HDate()

    def test_assign_bad_hdate_value(self):
        bad_day_value = HebrewDate(5779, 10, 35)
        with pytest.raises(TypeError):
            HDate().hdate = "not a HebrewDate"
        with pytest.raises(ValueError):
            HebrewDate(5779, 15, 3)
        with pytest.raises(ValueError):
            HDate().hdate = bad_day_value

    @pytest.mark.parametrize("execution_number", list(range(10)))
    def test_random_hdate(self, execution_number, rand_hdate):
        _hdate = HDate()
        _hdate.hdate = rand_hdate.hdate
        assert _hdate._jdn == rand_hdate._jdn
        assert _hdate.hdate == rand_hdate.hdate
        assert _hdate.gdate == rand_hdate.gdate

    def test_conv_get_size_of_hebrew_year(self):
        for year, info in list(HEBREW_YEARS_INFO.items()):
            assert conv.get_size_of_hebrew_year(year) == info[1]

    @pytest.mark.parametrize("execution_number", list(range(10)))
    def test_hdate_get_size_of_hebrew_years(self, execution_number, rand_hdate):
        assert rand_hdate.year_size() == conv.get_size_of_hebrew_year(
            rand_hdate.hdate.year
        )

    def test_rosh_hashana_day_of_week(self, rand_hdate):
        for year, info in list(HEBREW_YEARS_INFO.items()):
            rand_hdate.hdate = HebrewDate(
                year, rand_hdate.hdate.month, rand_hdate.hdate.day
            )
            assert rand_hdate.rosh_hashana_dow() == info[0]

    def test_pesach_day_of_week(self, rand_hdate):
        for year, info in list(HEBREW_YEARS_INFO.items()):
            rand_hdate.hdate = HebrewDate(year, 7, 15)
            assert rand_hdate.dow == info[2]
            assert rand_hdate.holiday_name == "pesach"

    UPCOMING_SHABBATOT = [
        ((2018, 11, 30), (2018, 12, 1), (5779, 3, 22)),
        ((2018, 12, 1), (2018, 12, 1), (5779, 3, 23)),
        ((2018, 12, 2), (2018, 12, 8), (5779, 3, 24)),
        ((2018, 12, 3), (2018, 12, 8), (5779, 3, 25)),
        ((2018, 12, 4), (2018, 12, 8), (5779, 3, 26)),
        ((2018, 12, 5), (2018, 12, 8), (5779, 3, 27)),
        ((2018, 12, 6), (2018, 12, 8), (5779, 3, 28)),
        ((2018, 12, 7), (2018, 12, 8), (5779, 3, 29)),
        ((2018, 12, 8), (2018, 12, 8), (5779, 3, 30)),
        ((2018, 12, 9), (2018, 12, 15), (5779, 4, 1)),
    ]

    @pytest.mark.parametrize(
        "current_date, shabbat_date, hebrew_date", UPCOMING_SHABBATOT
    )
    def test_upcoming_shabbat(self, current_date, shabbat_date, hebrew_date):
        hd = HDate(gdate=datetime.date(*current_date))
        assert hd.hdate == HebrewDate(*hebrew_date)
        next_shabbat = hd.upcoming_shabbat
        assert next_shabbat.gdate == datetime.date(*shabbat_date)

    def test_prev_and_next_day(self, rand_hdate):
        assert (rand_hdate.previous_day.gdate - rand_hdate.gdate) == datetime.timedelta(
            -1
        )
        assert (rand_hdate.next_day.gdate - rand_hdate.gdate) == datetime.timedelta(1)


class TestSpecialDays(object):

    NON_MOVING_HOLIDAYS = [
        ((1, 1), "rosh_hashana_i"),
        ((2, 1), "rosh_hashana_ii"),
        ((9, 1), "erev_yom_kippur"),
        ((10, 1), "yom_kippur"),
        ((15, 1), "sukkot"),
        ((17, 1), "hol_hamoed_sukkot"),
        ((18, 1), "hol_hamoed_sukkot"),
        ((19, 1), "hol_hamoed_sukkot"),
        ((20, 1), "hol_hamoed_sukkot"),
        ((21, 1), "hoshana_raba"),
        ((22, 1), "shmini_atzeret"),
        ((15, 7), "pesach"),
        ((17, 7), "hol_hamoed_pesach"),
        ((18, 7), "hol_hamoed_pesach"),
        ((19, 7), "hol_hamoed_pesach"),
        ((20, 7), "hol_hamoed_pesach"),
        ((21, 7), "pesach_vii"),
        ((5, 9), "erev_shavuot"),
        ((6, 9), "shavuot"),
        ((25, 3), "chanukah"),
        ((26, 3), "chanukah"),
        ((27, 3), "chanukah"),
        ((28, 3), "chanukah"),
        ((29, 3), "chanukah"),
        ((1, 4), "chanukah"),
        ((2, 4), "chanukah"),
        ((10, 4), "asara_btevet"),
        ((15, 5), "tu_bshvat"),
        ((18, 8), "lag_bomer"),
        ((15, 11), "tu_bav"),
    ]

    DIASPORA_ISRAEL_HOLIDAYS = [
        # Date, holiday in Diaspora, holiday in Israel
        ((16, 1), "sukkot_ii", "hol_hamoed_sukkot"),
        ((23, 1), "simchat_torah", ""),
        ((16, 7), "pesach_ii", "hol_hamoed_pesach"),
        ((22, 7), "pesach_viii", ""),
        ((7, 9), "shavuot_ii", ""),
    ]

    MOVING_HOLIDAYS = [
        # Possible dates, name
        ([(3, 1), (4, 1)], "tzom_gedaliah"),
        ([(17, 10), (18, 10)], "tzom_tammuz"),
        ([(9, 11), (10, 11)], "tisha_bav"),
    ]

    NEW_HOLIDAYS = [
        # Possible dates, test year range, name
        ([(26, 7), (27, 7), (28, 7)], (5719, 6500), "yom_hashoah"),
        ([(3, 8), (4, 8), (5, 8)], (5709, 5763), "yom_haatzmaut"),
        ([(3, 8), (4, 8), (5, 8), (6, 8)], (5764, 6500), "yom_haatzmaut"),
        ([(2, 8), (3, 8), (4, 8)], (5709, 5763), "yom_hazikaron"),
        ([(2, 8), (3, 8), (4, 8), (5, 8)], (5764, 6500), "yom_hazikaron"),
        ([(28, 8)], (5728, 6500), "yom_yerushalayim"),
        ([(11, 2), (12, 2)], (5758, 6500), "rabin_memorial_day"),
        ([(29, 10)], (5765, 6500), "zeev_zhabotinsky_day"),
        ([(30, 5)], (5734, 6500), "family_day"),
    ]

    ADAR_HOLIDAYS = [
        ([11, 13], "taanit_esther"),
        ([14], "purim"),
        ([15], "shushan_purim"),
        ([7], "memorial_day_unknown"),
    ]

    UPCOMING_HOLIDAYS = [
        ((2018, 8, 8), (2018, 9, 10), "rosh_hashana_i", "BOTH"),
        ((2018, 9, 8), (2018, 9, 10), "rosh_hashana_i", "BOTH"),
        ((2018, 9, 10), (2018, 9, 10), "rosh_hashana_i", "BOTH"),
        ((2018, 9, 11), (2018, 9, 11), "rosh_hashana_ii", "BOTH"),
        ((2018, 9, 12), (2018, 9, 19), "yom_kippur", "BOTH"),
        ((2018, 9, 19), (2018, 9, 19), "yom_kippur", "BOTH"),
        ((2018, 9, 20), (2018, 9, 24), "sukkot", "BOTH"),
        ((2018, 9, 24), (2018, 9, 24), "sukkot", "BOTH"),
        ((2018, 9, 25), (2018, 9, 25), "sukkot_ii", "DIASPORA"),
        ((2018, 9, 25), (2018, 10, 1), "shmini_atzeret", "ISRAEL"),
        ((2018, 9, 26), (2018, 10, 1), "shmini_atzeret", "BOTH"),
        ((2018, 10, 2), (2018, 10, 2), "simchat_torah", "DIASPORA"),
        ((2018, 10, 2), (2019, 4, 20), "pesach", "ISRAEL"),
        ((2018, 10, 3), (2019, 4, 20), "pesach", "BOTH"),
    ]

    @pytest.mark.parametrize(
        "current_date, holiday_date, holiday_name, where", UPCOMING_HOLIDAYS
    )
    def test_get_next_yom_tov(
        self, current_date, holiday_date, holiday_name, where, rand_hdate
    ):
        if where == "BOTH" or where == "DIASPORA":
            hdate = HDate(gdate=datetime.date(*current_date), diaspora=True)
            next_yom_tov = hdate.upcoming_yom_tov
            assert next_yom_tov.gdate == datetime.date(*holiday_date)
        if where == "BOTH" or where == "ISRAEL":
            hdate = HDate(gdate=datetime.date(*current_date), diaspora=False)
            next_yom_tov = hdate.upcoming_yom_tov
            assert next_yom_tov.gdate == datetime.date(*holiday_date)

    UPCOMING_SHABBAT_OR_YOM_TOV = [
        ((2018, 9, 8), True, {"start": (2018, 9, 8), "end": (2018, 9, 8)}),
        ((2018, 9, 9), True, {"start": (2018, 9, 10), "end": (2018, 9, 11)}),
        ((2018, 9, 16), True, {"start": (2018, 9, 19), "end": (2018, 9, 19)}),
        ((2018, 9, 24), True, {"start": (2018, 9, 24), "end": (2018, 9, 25)}),
        ((2018, 9, 25), True, {"start": (2018, 9, 24), "end": (2018, 9, 25)}),
        ((2018, 9, 24), False, {"start": (2018, 9, 24), "end": (2018, 9, 24)}),
        ((2018, 9, 24), True, {"start": (2018, 9, 24), "end": (2018, 9, 25)}),
        ((2018, 3, 30), True, {"start": (2018, 3, 31), "end": (2018, 4, 1)}),
        ((2018, 3, 30), False, {"start": (2018, 3, 31), "end": (2018, 3, 31)}),
        ((2017, 9, 22), True, {"start": (2017, 9, 21), "end": (2017, 9, 23)}),
        ((2017, 9, 22), False, {"start": (2017, 9, 21), "end": (2017, 9, 23)}),
        ((2017, 10, 4), True, {"start": (2017, 10, 5), "end": (2017, 10, 7)}),
        ((2017, 10, 4), False, {"start": (2017, 10, 5), "end": (2017, 10, 5)}),
        ((2017, 10, 6), True, {"start": (2017, 10, 5), "end": (2017, 10, 7)}),
        ((2017, 10, 6), False, {"start": (2017, 10, 7), "end": (2017, 10, 7)}),
        ((2016, 6, 12), True, {"start": (2016, 6, 11), "end": (2016, 6, 13)}),
    ]

    @pytest.mark.parametrize(
        "current_date, diaspora, dates", UPCOMING_SHABBAT_OR_YOM_TOV
    )
    def test_get_next_shabbat_or_yom_tov(self, current_date, diaspora, dates):
        hd = HDate(gdate=datetime.date(*current_date), diaspora=diaspora)
        assert hd.upcoming_shabbat_or_yom_tov.first_day.gdate == datetime.date(
            *dates["start"]
        )
        assert hd.upcoming_shabbat_or_yom_tov.last_day.gdate == datetime.date(
            *dates["end"]
        )

    @pytest.mark.parametrize("date, holiday", NON_MOVING_HOLIDAYS)
    def test_get_holidays_non_moving(self, rand_hdate, date, holiday):
        rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, date[1], date[0])
        assert rand_hdate.holiday_name == holiday
        assert rand_hdate.is_holiday

    @pytest.mark.parametrize(
        "date, diaspora_holiday, israel_holiday", DIASPORA_ISRAEL_HOLIDAYS
    )
    def test_get_diaspora_israel_holidays(
        self, rand_hdate, date, diaspora_holiday, israel_holiday
    ):
        rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, date[1], date[0])
        assert rand_hdate.holiday_name == israel_holiday
        rand_hdate.diaspora = True
        assert rand_hdate.holiday_name == diaspora_holiday
        assert rand_hdate.is_holiday

    @pytest.mark.parametrize("possible_dates, holiday", MOVING_HOLIDAYS)
    def test_get_holidays_moving(self, possible_dates, holiday):
        found_matching_holiday = False
        year = random.randint(5000, 6500)

        print("Testing " + holiday + " for " + str(year))

        for date in possible_dates:
            date_under_test = HDate(hebrew=False)
            date_under_test.hdate = HebrewDate(year, date[1], date[0])
            if date_under_test.holiday_name == holiday:
                print("date ", date_under_test, " matched")
                for other in possible_dates:
                    if other != date:
                        other_date = HDate(hebrew=False)
                        other_date.hdate = HebrewDate(year, other[1], other[0])
                        print("checking ", other_date, " doesn't match")
                        assert other_date.holiday_name != holiday
                found_matching_holiday = True
                assert date_under_test.is_holiday

        assert found_matching_holiday

    @pytest.mark.parametrize("possible_dates, years, holiday", NEW_HOLIDAYS)
    def test_new_holidays_multiple_date(self, possible_dates, years, holiday):
        found_matching_holiday = False
        year = random.randint(*years)

        print("Testing " + holiday + " for " + str(year))

        for date in possible_dates:
            date_under_test = HDate(hebrew=False)
            date_under_test.hdate = HebrewDate(year, date[1], date[0])
            if date_under_test.holiday_name == holiday:
                print("date ", date_under_test, " matched")
                for other in possible_dates:
                    if other != date:
                        other_date = HDate(hebrew=False)
                        other_date.hdate = HebrewDate(year, other[1], other[0])
                        print("checking ", other_date, " doesn't match")
                        assert other_date.holiday_name != holiday
                found_matching_holiday = True
                assert date_under_test.is_holiday

        assert found_matching_holiday

    @pytest.mark.parametrize("possible_dates, years, holiday", NEW_HOLIDAYS)
    def test_new_holidays_invalid_before(self, possible_dates, years, holiday):
        # Yom hazikaron and yom ha'atsmaut don't test for before 5764
        if years[0] == 5764 and holiday in ["yom_hazikaron", "yom_haatzmaut"]:
            return
        year = random.randint(5000, years[0] - 1)
        print("Testing " + holiday + " for " + str(year))
        for date in possible_dates:
            date_under_test = HDate()
            date_under_test.hdate = HebrewDate(year, date[1], date[0])
            assert date_under_test.holiday_name == ""

    def test_get_holiday_hanuka_3rd_tevet(self):
        year = random.randint(5000, 6000)
        year_size = conv.get_size_of_hebrew_year(year)
        myhdate = HDate(heb_date=HebrewDate(year, 4, 3))
        print(year_size)
        if year_size in [353, 383]:
            assert myhdate.holiday_name == "chanukah"
        else:
            assert myhdate.holiday_name == ""

    @pytest.mark.parametrize("possible_days, holiday", ADAR_HOLIDAYS)
    def test_get_holiday_adar(self, possible_days, holiday):
        year = random.randint(5000, 6000)
        year_size = conv.get_size_of_hebrew_year(year)
        month = 6 if year_size < 360 else 14
        myhdate = HDate()

        for day in possible_days:
            myhdate.hdate = HebrewDate(year, month, day)
            if day == 13 and myhdate.dow == 7 and holiday == "taanit_esther":
                assert myhdate.holiday_name == ""
            elif day == 11 and myhdate.dow != 5 and holiday == "taanit_esther":
                assert myhdate.holiday_name == ""
            else:
                assert myhdate.holiday_name == holiday

    @pytest.mark.parametrize("execution_number", list(range(10)))
    def test_get_omer_day(self, execution_number, rand_hdate):
        if (
            rand_hdate.hdate.month not in [Months.Nisan, Months.Iyyar, Months.Sivan]
            or rand_hdate.hdate.month == Months.Nisan
            and rand_hdate.hdate.day < 16
            or rand_hdate.hdate.month == Months.Sivan
            and rand_hdate.hdate.day > 5
        ):
            assert rand_hdate.omer_day == 0

        nissan = list(range(16, 30))
        iyyar = list(range(1, 29))
        sivan = list(range(1, 5))

        for day in nissan:
            rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, 7, day)
            assert rand_hdate.omer_day == day - 15
        for day in iyyar:
            rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, 8, day)
            assert rand_hdate.omer_day == day + 15
        for day in sivan:
            rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, 9, day)
            assert rand_hdate.omer_day == day + 44

    def test_daf_yomi(self):
        # Random test date
        myhdate = HDate(gdate=datetime.date(2014, 4, 28), hebrew=False)
        assert myhdate.daf_yomi == "Beitzah 29"
        # Beginning/end of cycle:
        myhdate = HDate(gdate=datetime.date(2020, 1, 4), hebrew=False)
        assert myhdate.daf_yomi == "Niddah 73"
        myhdate = HDate(gdate=datetime.date(2020, 1, 5), hebrew=False)
        assert myhdate.daf_yomi == "Berachos 2"
        myhdate = HDate(gdate=datetime.date(2020, 3, 7), hebrew=True)
        assert myhdate.daf_yomi == u"ברכות סד"
        myhdate = HDate(gdate=datetime.date(2020, 3, 8), hebrew=True)
        assert myhdate.daf_yomi == u"שבת ב"


class TestHDateReading(object):

    READINGS_FOR_YEAR_DIASPORA = [
        # שנים מעוברות
        # זשה
        (
            5763,
            [
                [0, 53, 0],
                list(range(29)),
                [0],
                list(range(29, 35)),
                [0],
                list(range(35, 39)),
                [59, 41, 60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # זחג
        (
            5757,
            [
                [0, 53, 0],
                list(range(29)),
                [0],
                list(range(29, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # השג
        (5774, [[53, 0], list(range(30)), [0], list(range(30, 51)), [61]]),
        # החא
        (5768, [[53, 0], list(range(30)), [0], list(range(30, 51))]),
        # גכז
        (
            5755,
            [
                [52, 53],
                list(range(29)),
                [0, 0],
                list(range(29, 42)),
                [60],
                list(range(44, 51)),
            ],
        ),
        # בשז
        (
            5776,
            [
                [52, 53],
                list(range(29)),
                [0, 0],
                list(range(29, 42)),
                [60],
                list(range(44, 51)),
            ],
        ),
        # בחה
        (
            5749,
            [
                [52, 53],
                list(range(29)),
                [0],
                list(range(29, 35)),
                [0],
                list(range(35, 39)),
                [59, 41, 60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # שנים פשוטות
        # השא
        (
            5754,
            [
                [53, 0],
                list(range(26)),
                [0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 54)),
            ],
        ),
        # בשה
        (
            5756,
            [
                [52, 53],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58, 34, 0],
                list(range(35, 39)),
                [59, 41, 60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # זחא
        (
            5761,
            [
                [0, 53, 0],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 52)),
            ],
        ),
        # גכה
        (
            5769,
            [
                [52, 53],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58, 34, 0],
                list(range(35, 39)),
                [59, 41, 60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # זשג
        (
            5770,
            [
                [0, 53, 0],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # הכז
        (
            5775,
            [
                [53, 0],
                list(range(22)),
                [55, 24, 25, 0, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 51)),
            ],
        ),
        # בחג
        (
            5777,
            [
                [52, 53],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        (
            5778,
            [
                [53, 0],
                list(range(22)),
                [55, 24, 25, 0, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 52)),
            ],
        ),
    ]

    READINGS_FOR_YEAR_ISRAEL = [
        # שנים מעוברות
        # זשה
        (
            5763,
            [
                [0, 53, 0, 54],
                list(range(1, 29)),
                [0],
                list(range(29, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # זחג
        (
            5757,
            [
                [0, 53, 0, 54],
                list(range(1, 29)),
                [0],
                list(range(29, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # השג
        (5774, [[53, 0], list(range(30)), [0], list(range(30, 51)), [61]]),
        # החא
        (5768, [[53, 0], list(range(30)), [0], list(range(30, 51))]),
        # גכז
        (5755, [[52, 53], list(range(29)), [0], list(range(29, 51))]),
        # בשז
        (5776, [[52, 53], list(range(29)), [0], list(range(29, 51))]),
        # בחה
        (
            5749,
            [
                [52, 53],
                list(range(29)),
                [0],
                list(range(29, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # שנים פשוטות
        # השא
        (
            5754,
            [
                [53, 0],
                list(range(26)),
                [0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 54)),
            ],
        ),
        # בשה
        (
            5756,
            [
                [52, 53],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # זחא
        (
            5761,
            [
                [0, 53, 0, 54],
                list(range(1, 22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 52)),
            ],
        ),
        # גכה
        (
            5769,
            [
                [52, 53],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # זשג
        (
            5770,
            [
                [0, 53, 0, 54],
                list(range(1, 22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
        # הכז
        (
            5775,
            [
                [53, 0],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57],
                list(range(31, 42)),
                [60],
                list(range(44, 52)),
            ],
        ),
        # בחג
        (
            5777,
            [
                [52, 53],
                list(range(22)),
                [55, 24, 25, 0, 26, 56, 57, 31, 58],
                list(range(34, 42)),
                [60],
                list(range(44, 51)),
                [61],
            ],
        ),
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

    @pytest.mark.parametrize("year", range(5740, 5800))
    def test_nitzavim_always_before_rosh_hashana(self, year):
        mydate = HDate(hebrew=False, diaspora=False)
        mydate.hdate = HebrewDate(year, Months.Tishrei, 1)
        tdelta = datetime.timedelta((12 - mydate.gdate.weekday()) % 7 - 7)
        # Go back to the previous shabbat
        mydate.gdate += tdelta
        print(
            "Testing date: {} which is {} days before Rosh Hashana".format(
                mydate, tdelta
            )
        )
        assert mydate.get_reading() in [51, 61]

    @pytest.mark.parametrize("year", range(5740, 5800))
    def test_vayelech_or_haazinu_always_after_rosh_hashana(self, year):
        mydate = HDate(hebrew=False, diaspora=True)
        mydate.hdate = HebrewDate(year, Months.Tishrei, 1)
        tdelta = datetime.timedelta((12 - mydate.gdate.weekday()) % 7)
        # Go to the next shabbat (unless shabbat falls on Rosh Hashana)
        mydate.gdate += tdelta
        print(
            "Testing date: {} which is {} days after Rosh Hashana".format(
                mydate, tdelta
            )
        )
        assert mydate.get_reading() in [52, 53, 0]

    def test_last_week_of_the_year(self):
        mydate = HDate()
        mydate.hdate = HebrewDate(5779, Months.Elul, 29)
        assert mydate.get_reading() == 52
