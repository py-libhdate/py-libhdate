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


# Test against both a leap year and non-leap year
@pytest.mark.parametrize(("year"), ((5783, 5784)))
def test_get_holidays_for_year(year: int) -> None:
    """Test that get_holidays_for_year() returns every holiday."""
    cur_date = HDate(HebrewDate(year, 1, 1))

    expected_holiday_map = defaultdict(list)
    for entry, date in cur_date.get_holidays_for_year():
        expected_holiday_map[date.to_gdate()].append(entry.name)

    while cur_date.hdate.year == year:
        actual_holiday = cur_date.holidays
        if isinstance(actual_holiday, list):
            assert [holiday.name for holiday in actual_holiday] == expected_holiday_map[
                cur_date.gdate
            ]
        else:
            assert len(expected_holiday_map[cur_date.gdate]) == 0
        cur_date = cur_date.next_day


def test_get_holidays_for_year_non_leap_year() -> None:
    """Test that get_holidays_for_year() returns consistent months."""
    base_date = HDate(HebrewDate(5783, Months.TISHREI, 1))
    for _, date in base_date.get_holidays_for_year():
        assert date.month not in (Months.ADAR_I, Months.ADAR_II)


def test_get_holidays_for_year_leap_year() -> None:
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


@pytest.mark.parametrize("date, expected", NON_MOVING_HOLIDAYS)
@given(year=strategies.integers(min_value=4000, max_value=6000))
@settings(deadline=None)
def test_get_holidays_non_moving(
    year: int, date: tuple[int, int], expected: set[str]
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
    possible_dates: list[tuple[int, int]], holiday: str
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
                holiday.name == "rosh_chodesh" for holiday in date_under_test.holidays
            )
        else:
            assert len(date_under_test.holidays) == 0


@given(year=strategies.integers(min_value=5000, max_value=6000))
@settings(deadline=None)
def test_get_holiday_hanuka_3rd_tevet(year: int) -> None:
    """Test Chanuka falling on 3rd of Tevet."""
    year_size = HebrewDate.year_size(year)
    myhdate = HDate(HebrewDate(year, 4, 3))
    if year_size in (353, 383):
        assert myhdate.holidays[0].name == "chanukah"
    else:
        assert len(myhdate.holidays) == 0
        assert myhdate.is_holiday is False


def test_hanukah_5785() -> None:
    """December 31, 2024 is Hanuka."""
    mydate = HDate(date=dt.date(2024, 12, 31))
    assert "chanukah" == mydate.holidays[0].name
    assert "rosh_chodesh" == mydate.holidays[1].name


@pytest.mark.parametrize("possible_days, holiday", ADAR_HOLIDAYS)
def test_get_holiday_adar(possible_days: list[int], holiday: str) -> None:
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
def test_get_tishrei_rosh_chodesh(year: int) -> None:
    """30th of Tishrei should be Rosh Chodesh"""
    myhdate = HDate(HebrewDate(year, Months.TISHREI, 30))
    assert myhdate.holidays[0].name == "rosh_chodesh"
    myhdate = HDate(HebrewDate(year, Months.TISHREI, 1))
    assert myhdate.holidays[0].name == "rosh_hashana_i"
