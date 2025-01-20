"""Test the holidays module."""

import datetime as dt
import random
from collections import defaultdict
from typing import Union

import pytest
from hypothesis import given, settings, strategies

from hdate import HDate, HebrewDate
from hdate.hebrew_date import Months
from hdate.holidays import HolidayManager


def test_holiday_manager() -> None:
    """Test the holiday manager."""
    assert isinstance(HolidayManager(diaspora=False), HolidayManager)


class TestSpecialDays:
    """Test HDate in terms of special days."""

    def test_is_leap_year(self) -> None:
        """Test that is_leap_year() working as expected for leap year."""
        leap_date = HebrewDate(5784, 1, 1)
        assert leap_date.is_leap_year()

    def test_is_not_leap_year(self) -> None:
        """Test that is_leap_year() working as expected for non-leap year."""
        leap_date = HebrewDate(5783, 1, 1)
        assert not leap_date.is_leap_year()

    # Test against both a leap year and non-leap year
    @pytest.mark.parametrize(("year"), ((5783, 5784)))
    def test_get_holidays_for_year(self, year: int) -> None:
        """Test that get_holidays_for_year() returns every holiday."""
        cur_date = HDate(HebrewDate(year, 1, 1))

        expected_holiday_map = defaultdict(list)
        for entry, date in cur_date.get_holidays_for_year():
            expected_holiday_map[date.to_gdate()].append(entry.name)

        while cur_date.hdate.year == year:
            actual_holiday = cur_date.holidays
            if isinstance(actual_holiday, list):
                assert [
                    holiday.name for holiday in actual_holiday
                ] == expected_holiday_map[cur_date.gdate]
            else:
                assert len(expected_holiday_map[cur_date.gdate]) == 0
            cur_date = cur_date.next_day

    def test_get_holidays_for_year_non_leap_year(self) -> None:
        """Test that get_holidays_for_year() returns consistent months."""
        base_date = HDate(HebrewDate(5783, Months.TISHREI, 1))
        for _, date in base_date.get_holidays_for_year():
            assert date.month not in (Months.ADAR_I, Months.ADAR_II)

    def test_get_holidays_for_year_leap_year(self) -> None:
        """Test that get_holidays_for_year() returns consistent months."""
        base_date = HDate(HebrewDate(5784, Months.TISHREI, 1))
        for _, date in base_date.get_holidays_for_year():
            assert date.month != Months.ADAR

    NON_MOVING_HOLIDAYS = [
        ((1, 1), {"rosh_hashana_i"}),
        ((2, 1), {"rosh_hashana_ii"}),
        ((9, 1), {"erev_yom_kippur"}),
        ((10, 1), {"yom_kippur"}),
        ((15, 1), {"sukkot"}),
        ((17, 1), {"hol_hamoed_sukkot"}),
        ((18, 1), {"hol_hamoed_sukkot"}),
        ((19, 1), {"hol_hamoed_sukkot"}),
        ((20, 1), {"hol_hamoed_sukkot"}),
        ((21, 1), {"hoshana_raba"}),
        ((15, 9), {"pesach"}),
        ((17, 9), {"hol_hamoed_pesach"}),
        ((18, 9), {"hol_hamoed_pesach"}),
        ((19, 9), {"hol_hamoed_pesach"}),
        ((20, 9), {"hol_hamoed_pesach"}),
        ((21, 9), {"pesach_vii"}),
        ((5, 11), {"erev_shavuot"}),
        ((6, 11), {"shavuot"}),
        ((25, 3), {"chanukah"}),
        ((26, 3), {"chanukah"}),
        ((27, 3), {"chanukah"}),
        ((28, 3), {"chanukah"}),
        ((29, 3), {"chanukah"}),
        ((1, 4), {"chanukah", "rosh_chodesh"}),
        ((2, 4), {"chanukah"}),
        ((10, 4), {"asara_btevet"}),
        ((15, 5), {"tu_bshvat"}),
        ((18, 10), {"lag_bomer"}),
        ((15, 13), {"tu_bav"}),
    ]

    DIASPORA_ISRAEL_HOLIDAYS = [
        # Date, holiday in Diaspora, holiday in Israel
        ((16, 1), {"sukkot_ii"}, {"hol_hamoed_sukkot"}),
        ((22, 1), {"shmini_atzeret"}, {"shmini_atzeret", "simchat_torah"}),
        ((23, 1), {"simchat_torah"}, {}),
        ((16, 9), {"pesach_ii"}, {"hol_hamoed_pesach"}),
        ((22, 9), {"pesach_viii"}, {}),
        ((7, 11), {"shavuot_ii"}, {}),
    ]

    MOVING_HOLIDAYS = [
        # Possible dates, name
        ([(3, 1), (4, 1)], "tzom_gedaliah"),
        ([(17, 12), (18, 12)], "tzom_tammuz"),
        ([(9, 13), (10, 13)], "tisha_bav"),
    ]

    NEW_HOLIDAYS = [
        # Possible dates, test year range, name
        ([(26, 9), (27, 9), (28, 9)], (5719, 6500), "yom_hashoah"),
        ([(3, 10), (4, 10), (5, 10)], (5709, 5763), "yom_haatzmaut"),
        ([(3, 10), (4, 10), (5, 10), (6, 10)], (5764, 6500), "yom_haatzmaut"),
        ([(2, 10), (3, 10), (4, 10)], (5709, 5763), "yom_hazikaron"),
        ([(2, 10), (3, 10), (4, 10), (5, 10)], (5764, 6500), "yom_hazikaron"),
        ([(28, 10)], (5728, 6500), "yom_yerushalayim"),
        ([(11, 2), (12, 2)], (5758, 6500), "rabin_memorial_day"),
        ([(29, 12)], (5765, 6500), "zeev_zhabotinsky_day"),
        ([(30, 5)], (5734, 6500), ["family_day", "rosh_chodesh"]),
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
        self,
        current_date: tuple[int, int, int],
        holiday_date: tuple[int, int, int],
        holiday_name: str,
        where: str,
    ) -> None:
        """Testing the value of next yom tov."""
        print(f"Testing holiday {holiday_name}")
        if where in ("BOTH", "DIASPORA"):
            hdate = HDate(date=dt.date(*current_date), diaspora=True)
            next_yom_tov = hdate.upcoming_yom_tov
            assert next_yom_tov.gdate == dt.date(*holiday_date)
        if where in ("BOTH", "ISRAEL"):
            hdate = HDate(date=dt.date(*current_date), diaspora=False)
            next_yom_tov = hdate.upcoming_yom_tov
            assert next_yom_tov.gdate == dt.date(*holiday_date)

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
    def test_get_next_shabbat_or_yom_tov(
        self,
        current_date: tuple[int, int, int],
        diaspora: bool,
        dates: dict[str, tuple[int, int, int]],
    ) -> None:
        """Test getting the next shabbat or Yom Tov works."""
        date = HDate(date=dt.date(*current_date), diaspora=diaspora)
        assert date.upcoming_shabbat_or_yom_tov.first_day.gdate == dt.date(
            *dates["start"]
        )
        assert date.upcoming_shabbat_or_yom_tov.last_day.gdate == dt.date(*dates["end"])

    @pytest.mark.parametrize("date, expected", NON_MOVING_HOLIDAYS)
    @given(year=strategies.integers(min_value=4000, max_value=6000))
    @settings(deadline=None)
    def test_get_holidays_non_moving(
        self,
        year: int,
        date: tuple[int, int],
        expected: set[str],
    ) -> None:
        """Test holidays that have a fixed hebrew date."""
        rand_hdate = HDate(HebrewDate(year, date[1], date[0]))
        assert set(holiday.name for holiday in rand_hdate.holidays) == expected
        assert rand_hdate.is_holiday

    @pytest.mark.parametrize(
        "date, diaspora_holiday, israel_holiday", DIASPORA_ISRAEL_HOLIDAYS
    )
    @given(year=strategies.integers(min_value=4000, max_value=6000))
    @settings(deadline=None)
    def test_get_diaspora_israel_holidays(
        self,
        year: int,
        date: tuple[int, int],
        diaspora_holiday: set[str],
        israel_holiday: set[str],
    ) -> None:
        """Test holidays that differ based on diaspora/israel."""
        rand_hdate = HDate(HebrewDate(year, date[1], date[0]), diaspora=False)
        if expected := israel_holiday:
            assert set(holiday.name for holiday in rand_hdate.holidays) == expected
        rand_hdate.diaspora = True
        if expected := diaspora_holiday:
            assert set(holiday.name for holiday in rand_hdate.holidays) == expected
        assert rand_hdate.is_holiday

    @pytest.mark.parametrize("possible_dates, holiday", MOVING_HOLIDAYS)
    def test_get_holidays_moving(
        self, possible_dates: list[tuple[int, int]], holiday: str
    ) -> None:
        """Test holidays that are moved based on the DOW."""
        found_matching_holiday = False
        year = random.randint(5000, 6500)

        print(f"Testing {holiday} for {year}")

        for date in possible_dates:
            date_under_test = HDate(language="english")
            date_under_test.hdate = HebrewDate(year, date[1], date[0])
            if (holidays := date_under_test.holidays) and holidays[0].name == holiday:
                print(f"date {date_under_test} matched")
                for other in possible_dates:
                    if other != date:
                        other_date = HDate(language="english")
                        other_date.hdate = HebrewDate(year, other[1], other[0])
                        print(f"checking {other_date} doesn't match")
                        assert len(other_date.holidays) == 0
                        assert other_date.is_holiday is False
                found_matching_holiday = True
                assert date_under_test.is_holiday

        assert found_matching_holiday

    @pytest.mark.parametrize("possible_dates, years, holiday", NEW_HOLIDAYS)
    def test_new_holidays_multiple_date(
        self,
        possible_dates: list[tuple[int, int]],
        years: tuple[int, int],
        holiday: Union[list[str], str],
    ) -> None:
        """Test holidays that have multiple possible dates."""
        found_matching_holiday = False
        year = random.randint(*years)

        print(f"Testing {holiday} for {year}")

        for date in possible_dates:
            date_under_test = HDate(language="english")
            date_under_test.hdate = HebrewDate(year, date[1], date[0])
            expected = set(holiday) if isinstance(holiday, list) else {holiday}
            if (holidays := date_under_test.holidays) and set(
                holiday.name for holiday in holidays
            ) == expected:
                print(f"date {date_under_test} matched")
                for other in possible_dates:
                    if other != date:
                        other_date = HDate(language="english")
                        other_date.hdate = HebrewDate(year, other[1], other[0])
                        print(f"checking {other_date} doesn't match")
                        if other_date.holidays:
                            assert other_date.holidays[0].name != holiday
                found_matching_holiday = True
                assert date_under_test.is_holiday

        assert found_matching_holiday

    @pytest.mark.parametrize("possible_dates, years, holiday", NEW_HOLIDAYS)
    def test_new_holidays_invalid_before(
        self,
        possible_dates: list[tuple[int, int]],
        years: tuple[int, int],
        holiday: Union[list[str], str],
    ) -> None:
        """Test holidays that were created over time."""
        # Yom hazikaron and yom ha'atsmaut don't test for before 5764
        if years[0] == 5764 and holiday in ["yom_hazikaron", "yom_haatzmaut"]:
            return
        year = random.randint(5000, years[0] - 1)
        print(f"Testing {holiday} for {year}")
        for date in possible_dates:
            date_under_test = HDate()
            date_under_test.hdate = HebrewDate(year, date[1], date[0])
            if date[0] in (1, 30):
                assert any(
                    holiday.name == "rosh_chodesh"
                    for holiday in date_under_test.holidays
                )
            else:
                assert len(date_under_test.holidays) == 0

    @given(year=strategies.integers(min_value=5000, max_value=6000))
    @settings(deadline=None)
    def test_get_holiday_hanuka_3rd_tevet(self, year: int) -> None:
        """Test Chanuka falling on 3rd of Tevet."""
        year_size = HebrewDate.year_size(year)
        myhdate = HDate(HebrewDate(year, 4, 3))
        if year_size in (353, 383):
            assert myhdate.holidays[0].name == "chanukah"
        else:
            assert len(myhdate.holidays) == 0
            assert myhdate.is_holiday is False

    def test_hanukah_5785(self) -> None:
        """December 31, 2024 is Hanuka."""
        mydate = HDate(date=dt.date(2024, 12, 31))
        assert "chanukah" == mydate.holidays[0].name
        assert "rosh_chodesh" == mydate.holidays[1].name

    @pytest.mark.parametrize("possible_days, holiday", ADAR_HOLIDAYS)
    def test_get_holiday_adar(self, possible_days: list[int], holiday: str) -> None:
        """Test holidays for Adar I/Adar II."""
        year = random.randint(5000, 6000)
        date = HebrewDate(year)
        date.month = Months.ADAR_II if date.is_leap_year() else Months.ADAR

        print(f"Testing {holiday} for {date!r}")

        for day in possible_days:
            date.day = day
            myhdate = HDate(date)
            if day == 13 and myhdate.dow == 7 and holiday == "taanit_esther":
                assert len(myhdate.holidays) == 0
                assert myhdate.is_holiday is False
            elif day == 11 and myhdate.dow != 5 and holiday == "taanit_esther":
                assert len(myhdate.holidays) == 0
                assert myhdate.is_holiday is False
            else:
                assert myhdate.holidays[0].name == holiday

    @given(year=strategies.integers(min_value=5000, max_value=6000))
    @settings(deadline=None)
    def test_get_tishrei_rosh_chodesh(self, year: int) -> None:
        """30th of Tishrei should be Rosh Chodesh"""
        myhdate = HDate(HebrewDate(year, Months.TISHREI, 30))
        assert myhdate.holidays[0].name == "rosh_chodesh"
        myhdate = HDate(HebrewDate(year, Months.TISHREI, 1))
        assert myhdate.holidays[0].name == "rosh_hashana_i"

    @given(date=strategies.dates())
    @settings(deadline=None)
    def test_get_omer_day(self, date: dt.date) -> None:
        """Test value of the Omer."""
        rand_hdate = HDate(date)
        if rand_hdate.hdate < HebrewDate(
            0, Months.NISAN, 16
        ) or rand_hdate.hdate > HebrewDate(0, Months.SIVAN, 5):
            assert rand_hdate.omer is None

        nissan = list(range(16, 30))
        iyyar = list(range(1, 29))
        sivan = list(range(1, 5))

        for day in nissan:
            rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, Months.NISAN, day)
            assert rand_hdate.omer is not None
            assert rand_hdate.omer.total_days == day - 15
        for day in iyyar:
            rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, Months.IYYAR, day)
            assert rand_hdate.omer is not None
            assert rand_hdate.omer.total_days == day + 15
        for day in sivan:
            rand_hdate.hdate = HebrewDate(rand_hdate.hdate.year, Months.SIVAN, day)
            assert rand_hdate.omer is not None
            assert rand_hdate.omer.total_days == day + 44

    def test_daf_yomi(self) -> None:
        """Test value of Daf Yomi."""
        # Random test date
        myhdate = HDate(date=dt.date(2014, 4, 28), language="english")
        assert myhdate.daf_yomi == "Beitzah 29"
        # Beginning/end of cycle:
        myhdate = HDate(date=dt.date(2020, 1, 4), language="english")
        assert myhdate.daf_yomi == "Niddah 73"
        myhdate = HDate(date=dt.date(2020, 1, 5), language="english")
        assert myhdate.daf_yomi == "Berachos 2"
        myhdate = HDate(date=dt.date(2020, 3, 7), language="hebrew")
        assert myhdate.daf_yomi == "ברכות סד"
        myhdate = HDate(date=dt.date(2020, 3, 8), language="hebrew")
        assert myhdate.daf_yomi == "שבת ב"
