"""Test the holidays module."""

import datetime as dt
import random
import typing
from collections import defaultdict

import pytest
from hypothesis import given, settings, strategies

from hdate import HDateInfo, HebrewDate
from hdate.hebrew_date import Months
from hdate.holidays import HolidayDatabase, is_yom_tov
from hdate.translator import Language, set_language
from tests.conftest import valid_hebrew_date


# Test against both a leap year and non-leap year
@pytest.mark.parametrize(("year"), (5783, 5784))
def test_get_holidays_for_year(year: int, holiday_db: HolidayDatabase) -> None:
    """Test that get_holidays_for_year() returns every holiday."""
    cur_date = HebrewDate(year, Months.TISHREI, 1)

    expected_holiday_map = defaultdict(set)
    for date, entries in holiday_db.lookup_holidays_for_year(cur_date).items():
        if cur_date.is_leap_year():
            assert date.month != Months.ADAR
        else:
            assert date.month not in (Months.ADAR_I, Months.ADAR_II)

        expected_holiday_map[date.to_gdate()] = {entry.name for entry in entries}

    while cur_date.year == year:
        gdate = cur_date.to_gdate()
        if len(holidays := holiday_db.lookup(cur_date)) == 0:
            assert len(expected_holiday_map[gdate]) == 0
        else:
            assert {holiday.name for holiday in holidays} == expected_holiday_map[
                gdate
            ], f"Error on {gdate}"

        cur_date += dt.timedelta(days=1)


NON_MOVING_HOLIDAYS = [
    ((Months.TISHREI, 1), {"rosh_hashana_i"}),
    ((Months.TISHREI, 2), {"rosh_hashana_ii"}),
    ((Months.TISHREI, 9), {"erev_yom_kippur"}),
    ((Months.TISHREI, 10), {"yom_kippur"}),
    ((Months.TISHREI, 15), {"sukkot"}),
    ((Months.TISHREI, 17), {"hol_hamoed_sukkot"}),
    ((Months.TISHREI, 18), {"hol_hamoed_sukkot"}),
    ((Months.TISHREI, 19), {"hol_hamoed_sukkot"}),
    ((Months.TISHREI, 20), {"hol_hamoed_sukkot"}),
    ((Months.TISHREI, 21), {"hoshana_raba"}),
    ((Months.NISAN, 15), {"pesach"}),
    ((Months.NISAN, 17), {"hol_hamoed_pesach"}),
    ((Months.NISAN, 18), {"hol_hamoed_pesach"}),
    ((Months.NISAN, 19), {"hol_hamoed_pesach"}),
    ((Months.NISAN, 20), {"hol_hamoed_pesach"}),
    ((Months.NISAN, 21), {"pesach_vii"}),
    ((Months.SIVAN, 5), {"erev_shavuot"}),
    ((Months.SIVAN, 6), {"shavuot"}),
    ((Months.KISLEV, 25), {"chanukah"}),
    ((Months.KISLEV, 26), {"chanukah"}),
    ((Months.KISLEV, 27), {"chanukah"}),
    ((Months.KISLEV, 28), {"chanukah"}),
    ((Months.KISLEV, 29), {"chanukah"}),
    ((Months.TEVET, 1), {"chanukah", "rosh_chodesh"}),
    ((Months.TEVET, 2), {"chanukah"}),
    ((Months.TEVET, 10), {"asara_btevet"}),
    ((Months.SHVAT, 15), {"tu_bshvat"}),
    ((Months.IYYAR, 18), {"lag_bomer"}),
    ((Months.AV, 15), {"tu_bav"}),
]

DIASPORA_ISRAEL_HOLIDAYS = [
    # Date, holiday in Diaspora, holiday in Israel
    ((Months.TISHREI, 16), {"sukkot_ii"}, {"hol_hamoed_sukkot"}),
    ((Months.TISHREI, 22), {"shmini_atzeret"}, {"shmini_atzeret", "simchat_torah"}),
    ((Months.TISHREI, 23), {"simchat_torah"}, {}),
    ((Months.NISAN, 16), {"pesach_ii"}, {"hol_hamoed_pesach"}),
    ((Months.NISAN, 22), {"pesach_viii"}, {}),
    ((Months.SIVAN, 7), {"shavuot_ii"}, {}),
]

MOVING_HOLIDAYS = [
    # Possible dates, name
    ([(Months.TISHREI, 3), (Months.TISHREI, 4)], "tzom_gedaliah"),
    ([(Months.TAMMUZ, 17), (Months.TAMMUZ, 18)], "tzom_tammuz"),
    ([(Months.AV, 9), (Months.AV, 10)], "tisha_bav"),
]

NEW_HOLIDAYS = [
    # Possible dates, test year range, name
    (
        [(Months.NISAN, 26), (Months.NISAN, 27), (Months.NISAN, 28)],
        (5719, 6500),
        {"yom_hashoah"},
    ),
    (
        [(Months.IYYAR, 3), (Months.IYYAR, 4), (Months.IYYAR, 5)],
        (5709, 5763),
        {"yom_haatzmaut"},
    ),
    (
        [(Months.IYYAR, 3), (Months.IYYAR, 4), (Months.IYYAR, 5), (Months.IYYAR, 6)],
        (5764, 6500),
        {"yom_haatzmaut"},
    ),
    (
        [(Months.IYYAR, 2), (Months.IYYAR, 3), (Months.IYYAR, 4)],
        (5709, 5763),
        {"yom_hazikaron"},
    ),
    (
        [(Months.IYYAR, 2), (Months.IYYAR, 3), (Months.IYYAR, 4), (Months.IYYAR, 5)],
        (5764, 6500),
        {"yom_hazikaron"},
    ),
    ([(Months.IYYAR, 28)], (5728, 6500), {"yom_yerushalayim"}),
    (
        [(Months.MARCHESHVAN, 11), (Months.MARCHESHVAN, 12)],
        (5758, 6500),
        {"rabin_memorial_day"},
    ),
    ([(Months.TAMMUZ, 29)], (5765, 6500), {"zeev_zhabotinsky_day"}),
    ([(Months.SHVAT, 30)], (5734, 6500), {"family_day", "rosh_chodesh"}),
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
    year: int, date: tuple[Months, int], expected: set[str], holiday_db: HolidayDatabase
) -> None:
    """Test holidays that have a fixed hebrew date."""
    rand_hdate = HebrewDate(year, *date)
    assert set(holiday.name for holiday in holiday_db.lookup(rand_hdate)) == expected


@pytest.mark.parametrize(
    "date, diaspora_holiday, israel_holiday", DIASPORA_ISRAEL_HOLIDAYS
)
@pytest.mark.parametrize(("holiday_db"), (True, False), indirect=True)
@given(year=strategies.integers(min_value=4000, max_value=6000))
def test_get_diaspora_israel_holidays(
    year: int,
    date: tuple[Months, int],
    diaspora_holiday: set[str],
    israel_holiday: set[str],
    holiday_db: HolidayDatabase,
) -> None:
    """Test holidays that differ based on diaspora/israel."""
    rand_hdate = HebrewDate(year, *date)
    holidays = holiday_db.lookup(rand_hdate)
    expected = diaspora_holiday if holiday_db.diaspora else israel_holiday
    if expected:
        assert set(holiday.name for holiday in holidays) == expected
    else:
        assert not holidays


@pytest.mark.parametrize("possible_dates, holiday", MOVING_HOLIDAYS)
@given(year=strategies.integers(min_value=4000, max_value=6000))
def test_get_holidays_moving(
    possible_dates: list[tuple[Months, int]],
    holiday: str,
    year: int,
    holiday_db: HolidayDatabase,
) -> None:
    """Test holidays that are moved based on the DOW."""
    print(f"Testing {holiday} for {year}")
    valid_dates = 0
    for date in possible_dates:
        date_under_test = HebrewDate(year, *date)
        holidays = holiday_db.lookup(date_under_test)
        assert (holiday_found := len(holidays) == 1) or len(holidays) == 0
        if holiday_found:
            valid_dates += 1
            assert holidays[0].name == holiday
    assert valid_dates == 1, "Only a single date should be valid"


@pytest.mark.parametrize("possible_dates, years, expected", NEW_HOLIDAYS)
def test_new_holidays_multiple_date(
    possible_dates: list[tuple[Months, int]],
    years: tuple[int, int],
    expected: set[str],
    holiday_db: HolidayDatabase,
) -> None:
    """Test holidays that have multiple possible dates."""
    year = random.randint(*years)
    print(f"Testing {expected} for {year}")
    valid_dates = 0
    for date in possible_dates:
        date_under_test = HebrewDate(year, *date)
        holidays = holiday_db.lookup(date_under_test)
        assert (holiday_found := len(holidays) > 0) or len(holidays) == 0
        if holiday_found and expected == set(h.name for h in holidays):
            valid_dates += 1
    assert valid_dates == 1, "Only a single date should be valid"


@pytest.mark.parametrize("possible_dates, years, expected", NEW_HOLIDAYS)
def test_new_holidays_invalid_before(
    possible_dates: list[tuple[Months, int]],
    years: tuple[int, int],
    expected: set[str],
    holiday_db: HolidayDatabase,
) -> None:
    """Test holidays that were created over time."""
    # Yom hazikaron and yom ha'atsmaut don't test for before 5764
    if years[0] == 5764 and expected.intersection({"yom_hazikaron", "yom_haatzmaut"}):
        return
    year = random.randint(5000, years[0] - 1)
    print(f"Testing {expected} for {year}")
    for date in possible_dates:
        date_under_test = HebrewDate(year, *date)
        holidays = holiday_db.lookup(date_under_test)
        assert len(holidays) == 0 or (
            len(holidays) == 1 and holidays[0].name == "rosh_chodesh"
        )


@given(year=strategies.integers(min_value=5000, max_value=6000))
@settings(deadline=None)
def test_get_holiday_hanuka_3rd_tevet(year: int) -> None:
    """Test Chanuka falling on 3rd of Tevet."""
    year_size = HebrewDate.year_size(year)
    myhdate = HDateInfo(HebrewDate(year, Months.TEVET, 3))
    if year_size in (353, 383):
        assert myhdate.holidays[0].name == "chanukah"
    else:
        assert len(myhdate.holidays) == 0
        assert myhdate.is_holiday is False


def test_hanukah_5785() -> None:
    """December 31, 2024 is Hanuka."""
    mydate = HDateInfo(date=dt.date(2024, 12, 31))
    assert "chanukah" == mydate.holidays[0].name
    assert "rosh_chodesh" == mydate.holidays[1].name


@pytest.mark.parametrize("possible_days, holiday", ADAR_HOLIDAYS)
@given(year=strategies.integers(min_value=5000, max_value=6000))
def test_get_holiday_adar(
    possible_days: list[int], holiday: str, year: int, holiday_db: HolidayDatabase
) -> None:
    """Test holidays for Adar I/Adar II."""
    date = HebrewDate(year)
    month = Months.ADAR_II if date.is_leap_year() else Months.ADAR
    valid_dates = 0
    for day in possible_days:
        dut = date.replace(month=month, day=day)
        print(f"Testing {holiday} for {dut!r}")
        holidays = holiday_db.lookup(dut)
        assert (holiday_found := len(holidays) == 1) or len(holidays) == 0
        if holiday_found:
            assert holidays[0].name == holiday
            valid_dates += 1
    assert valid_dates == 1


@given(year=strategies.integers(min_value=5000, max_value=6000))
@settings(deadline=None)
def test_get_tishrei_rosh_chodesh(year: int) -> None:
    """30th of Tishrei should be Rosh Chodesh"""
    myhdate = HDateInfo(HebrewDate(year, Months.TISHREI, 30))
    assert myhdate.holidays[0].name == "rosh_chodesh"
    myhdate = HDateInfo(HebrewDate(year, Months.TISHREI, 1))
    assert myhdate.holidays[0].name == "rosh_hashana_i"


@pytest.mark.parametrize("diaspora", ["ISRAEL", "DIASPORA"])
@pytest.mark.parametrize("language", typing.get_args(Language))
def test_get_all_holidays(language: Language, diaspora: str) -> None:
    """Test the method to get all the holiday descriptions in a specified language."""

    _diaspora = diaspora == "DIASPORA"
    set_language(language)
    names = HolidayDatabase(_diaspora).get_all_names()

    expected = {
        "fr": {
            "DIASPORA": {"Souccot II", "Pessah II"},
            "ISRAEL": {
                "Rosh Hodesh, Fête de la Famille",
                "Shemini Atseret, Simhat Torah",
            },
            "": {"Yom Kippour", "Hanoukka, Rosh Hodesh", "Pourim", "Pessah"},
        },
        "he": {
            "DIASPORA": {"שני של סוכות", "שני של פסח"},
            "ISRAEL": {"ראש חודש, יום המשפחה", "שמיני עצרת, שמחת תורה"},
            "": {"יום הכפורים", "חנוכה, ראש חודש", "פורים", "פסח"},
        },
        "en": {
            "DIASPORA": {"Sukkot II", "Pesach II"},
            "ISRAEL": {"Rosh Chodesh, Family Day", "Shmini Atzeret, Simchat Torah"},
            "": {"Yom Kippur", "Chanukah, Rosh Chodesh", "Purim", "Pesach"},
        },
    }
    fake = {"Non-existing Holiday", "Foo", "Bar"}
    assert all(entry in names for entry in expected[language][""])
    assert all(entry in names for entry in expected[language][diaspora])
    assert all(item not in names for item in fake)


@pytest.mark.parametrize(("diaspora"), (False, True))
@pytest.mark.parametrize(("language"), typing.get_args(Language))
@given(date=valid_hebrew_date())
def test_all_in_get_names(date: HebrewDate, diaspora: bool, language: Language) -> None:
    """Test that all holidays are actually returned by get_all_names()"""
    set_language(language)
    holiday_db = HolidayDatabase(diaspora=diaspora)
    next_date = holiday_db.lookup_next_holiday(date)
    holidays = holiday_db.lookup(next_date)
    expected = ", ".join(str(holiday) for holiday in holidays)
    all_names = holiday_db.get_all_names()
    assert expected in all_names


@pytest.mark.parametrize(("diaspora"), (False, True))
@given(date=valid_hebrew_date())
def test_is_yom_tov(date: HebrewDate, diaspora: bool) -> None:
    """Test is yom tov returns the same value for date and gdate."""
    assert is_yom_tov(date, diaspora) == is_yom_tov(date.to_gdate(), diaspora)


def test_is_yom_tov_special_dates() -> None:
    """Test is yom tov for known values"""
    assert is_yom_tov(HebrewDate(5785, Months.TISHREI, 1))
    assert is_yom_tov(HebrewDate(5785, Months.TISHREI, 2))
    assert not is_yom_tov(HebrewDate(5785, Months.TISHREI, 3))
    assert is_yom_tov(HebrewDate(5785, Months.TISHREI, 23), True)
    assert not is_yom_tov(HebrewDate(5785, Months.TISHREI, 23), False)


@pytest.mark.parametrize(
    "year, month, day, is_holiday, expected",
    [
        # this is not true
        (5785, Months.IYYAR, 5, False, "yom_haatzmaut"),
        (5785, Months.IYYAR, 4, False, "yom_hazikaron"),
        (5785, Months.NISAN, 27, False, "yom_hashoah"),
        # this is true
        (5785, Months.IYYAR, 3, True, "yom_haatzmaut"),
        (5785, Months.IYYAR, 2, True, "yom_hazikaron"),
        (5785, Months.NISAN, 26, True, "yom_hashoah"),
    ],
)
def test_new_holidays_known_dates(
    year: int, month: Months, day: int, is_holiday: bool, expected: str
) -> None:
    """Test that well-known new holidays are found only on their correct date."""
    # Test the holiday date
    holiday_db = HolidayDatabase(diaspora=False)
    date = HebrewDate(year, month, day)
    holidays = holiday_db.lookup(date)
    assert len(holidays) == int(is_holiday)
    if holidays:
        assert holidays[0].name == expected
