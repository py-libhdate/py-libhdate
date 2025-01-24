"""Test the holidays module."""

import datetime as dt
import random
from collections import defaultdict

import pytest
from hypothesis import given, settings, strategies

from hdate import HDate, HebrewDate
from hdate.hebrew_date import Months
from hdate.holidays import HOLIDAYS, Holiday, HolidayManager


# Test against both a leap year and non-leap year
@pytest.mark.parametrize(("year"), ((5783, 5784)))
def test_get_holidays_for_year(year: int) -> None:
    """Test that get_holidays_for_year() returns every holiday."""
    cur_date = HDate(HebrewDate(year, 1, 1))

    expected_holiday_map = defaultdict(set)
    for date, entries in cur_date.get_holidays_for_year().items():
        expected_holiday_map[date.to_gdate()] = {entry.name for entry in entries}

    while cur_date.hdate.year == year:
        if cur_date.holidays is None:
            assert len(expected_holiday_map[cur_date.gdate]) == 0
        else:
            assert {
                holiday.name for holiday in cur_date.holidays
            } == expected_holiday_map[cur_date.gdate]

        cur_date = cur_date.next_day


def test_get_holidays_for_year_non_leap_year() -> None:
    """Test that get_holidays_for_year() returns consistent months."""
    base_date = HDate(HebrewDate(5783, Months.TISHREI, 1))
    for date in base_date.get_holidays_for_year().keys():
        assert date.month not in (Months.ADAR_I, Months.ADAR_II)


def test_get_holidays_for_year_leap_year() -> None:
    """Test that get_holidays_for_year() returns consistent months."""
    base_date = HDate(HebrewDate(5784, Months.TISHREI, 1))
    for date in base_date.get_holidays_for_year().keys():
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
    ([(26, 9), (27, 9), (28, 9)], (5719, 6500), {"yom_hashoah"}),
    ([(3, 10), (4, 10), (5, 10)], (5709, 5763), {"yom_haatzmaut"}),
    ([(3, 10), (4, 10), (5, 10), (6, 10)], (5764, 6500), {"yom_haatzmaut"}),
    ([(2, 10), (3, 10), (4, 10)], (5709, 5763), {"yom_hazikaron"}),
    ([(2, 10), (3, 10), (4, 10), (5, 10)], (5764, 6500), {"yom_hazikaron"}),
    ([(28, 10)], (5728, 6500), {"yom_yerushalayim"}),
    ([(11, 2), (12, 2)], (5758, 6500), {"rabin_memorial_day"}),
    ([(29, 12)], (5765, 6500), {"zeev_zhabotinsky_day"}),
    ([(30, 5)], (5734, 6500), {"family_day", "rosh_chodesh"}),
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
@given(year=strategies.integers(min_value=4000, max_value=6000))
def test_get_holidays_moving(
    possible_dates: list[tuple[int, int]], holiday: str, year: int
) -> None:
    """Test holidays that are moved based on the DOW."""
    print(f"Testing {holiday} for {year}")
    valid_dates = 0
    mgr = HolidayManager(diaspora=True)
    for date in possible_dates:
        date_under_test = HebrewDate(year, date[1], date[0])
        holidays = mgr.lookup(date_under_test)
        assert (holiday_found := len(holidays) == 1) or len(holidays) == 0
        if holiday_found:
            valid_dates += 1
            assert holidays[0].name == holiday
    assert valid_dates == 1, "Only a single date should be valid"


@pytest.mark.parametrize("possible_dates, years, expected", NEW_HOLIDAYS)
def test_new_holidays_multiple_date(
    possible_dates: list[tuple[int, int]], years: tuple[int, int], expected: set[str]
) -> None:
    """Test holidays that have multiple possible dates."""
    year = random.randint(*years)
    print(f"Testing {expected} for {year}")
    valid_dates = 0
    mgr = HolidayManager(diaspora=False)
    for date in possible_dates:
        date_under_test = HebrewDate(year, date[1], date[0])
        holidays = mgr.lookup(date_under_test)
        assert (holiday_found := len(holidays) > 0) or len(holidays) == 0
        if holiday_found and expected == set(h.name for h in holidays):
            valid_dates += 1
    assert valid_dates == 1, "Only a single date should be valid"


@pytest.mark.parametrize("possible_dates, years, expected", NEW_HOLIDAYS)
def test_new_holidays_invalid_before(
    possible_dates: list[tuple[int, int]], years: tuple[int, int], expected: set[str]
) -> None:
    """Test holidays that were created over time."""
    # Yom hazikaron and yom ha'atsmaut don't test for before 5764
    if years[0] == 5764 and expected.intersection({"yom_hazikaron", "yom_haatzmaut"}):
        return
    year = random.randint(5000, years[0] - 1)
    print(f"Testing {expected} for {year}")
    mgr = HolidayManager(diaspora=False)
    for date in possible_dates:
        date_under_test = HebrewDate(year, date[1], date[0])
        holidays = mgr.lookup(date_under_test)
        assert len(holidays) == 0 or (
            len(holidays) == 1 and holidays[0].name == "rosh_chodesh"
        )


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
@given(year=strategies.integers(min_value=5000, max_value=6000))
def test_get_holiday_adar(possible_days: list[int], holiday: str, year: int) -> None:
    """Test holidays for Adar I/Adar II."""
    date = HebrewDate(year)
    date.month = Months.ADAR_II if date.is_leap_year() else Months.ADAR
    mgr = HolidayManager(diaspora=False)
    print(f"Testing {holiday} for {date!r}")
    valid_dates = 0
    for day in possible_days:
        dut = date.replace(day=day)
        holidays = mgr.lookup(dut)
        assert (holiday_found := len(holidays) == 1) or len(holidays) == 0
        if holiday_found:
            assert holidays[0].name == holiday
            valid_dates += 1
    assert valid_dates == 1


@given(year=strategies.integers(min_value=5000, max_value=6000))
@settings(deadline=None)
def test_get_tishrei_rosh_chodesh(year: int) -> None:
    """30th of Tishrei should be Rosh Chodesh"""
    myhdate = HDate(HebrewDate(year, Months.TISHREI, 30))
    assert myhdate.holidays[0].name == "rosh_chodesh"
    myhdate = HDate(HebrewDate(year, Months.TISHREI, 1))
    assert myhdate.holidays[0].name == "rosh_hashana_i"


@pytest.mark.parametrize("language", ["english", "french", "hebrew"])
def test_get_all_holidays(language: str) -> None:
    """Helper method to get all the holiday descriptions in the specified language."""

    def holiday_name(holiday: Holiday, language: str) -> str:
        holiday.set_language(language)
        return str(holiday)

    doubles = {
        "french": "Hanoukka, Rosh Hodesh",
        "hebrew": "חנוכה, ראש חודש",
        "english": "Chanukah, Rosh Chodesh",
    }
    holidays_list = [holiday_name(h, language) for h in HOLIDAYS] + [
        doubles.get(language, doubles["english"])
    ]

    assert HolidayManager.get_all_holiday_names(language) == set(holidays_list)
