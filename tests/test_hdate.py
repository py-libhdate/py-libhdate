"""Test HDate objects."""

import datetime as dt

import pytest
from hypothesis import given, strategies

from hdate import HDate, HebrewDate
from hdate.hebrew_date import Months

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


class TestHDate:
    """Tests for the HDate object."""

    def test_assign_bad_hdate_value(self) -> None:
        """Confirm that bad values raise an error."""
        with pytest.raises(TypeError):
            HDate().hdate = "not a HebrewDate"  # type: ignore
        with pytest.raises(ValueError):
            HebrewDate(5779, 15, 3)  # type: ignore
        with pytest.raises(ValueError):
            HDate().hdate = HebrewDate(5779, Months.NISAN, 35)

    @given(date=strategies.dates())
    def test_random_hdate(self, date: dt.date) -> None:
        """Run multiple cases with random hdates."""
        rand_hdate = HDate(date)
        _hdate = HDate()
        _hdate.hdate = rand_hdate.hdate
        assert _hdate.hdate == rand_hdate.hdate
        assert _hdate.gdate == rand_hdate.gdate

    def test_conv_get_size_of_hebrew_year(self) -> None:
        """Check that the size of year returned is correct."""
        for year, info in list(HEBREW_YEARS_INFO.items()):
            assert HebrewDate.year_size(year) == info[1]

    def test_rosh_hashana_day_of_week(self) -> None:
        """Check that Rosh Hashana's DOW matches the given dates"""
        for year, info in list(HEBREW_YEARS_INFO.items()):
            rosh_hashana = HebrewDate(year)
            assert rosh_hashana.dow() == info[0]

    def test_pesach_day_of_week(self) -> None:
        """ "Check that Pesach DOW matches the given dates."""
        for year, info in list(HEBREW_YEARS_INFO.items()):
            my_hdate = HebrewDate(year, Months.NISAN, 15)
            assert my_hdate.dow() == info[2]

    UPCOMING_SHABBATOT = [
        ((2018, 11, 30), (2018, 12, 1), (5779, Months.KISLEV, 22)),
        ((2018, 12, 1), (2018, 12, 1), (5779, Months.KISLEV, 23)),
        ((2018, 12, 2), (2018, 12, 8), (5779, Months.KISLEV, 24)),
        ((2018, 12, 3), (2018, 12, 8), (5779, Months.KISLEV, 25)),
        ((2018, 12, 4), (2018, 12, 8), (5779, Months.KISLEV, 26)),
        ((2018, 12, 5), (2018, 12, 8), (5779, Months.KISLEV, 27)),
        ((2018, 12, 6), (2018, 12, 8), (5779, Months.KISLEV, 28)),
        ((2018, 12, 7), (2018, 12, 8), (5779, Months.KISLEV, 29)),
        ((2018, 12, 8), (2018, 12, 8), (5779, Months.KISLEV, 30)),
        ((2018, 12, 9), (2018, 12, 15), (5779, Months.TEVET, 1)),
    ]

    @pytest.mark.parametrize(
        "current_date, shabbat_date, hebrew_date", UPCOMING_SHABBATOT
    )
    def test_upcoming_shabbat(
        self,
        current_date: tuple[int, int, int],
        shabbat_date: tuple[int, int, int],
        hebrew_date: tuple[int, Months, int],
    ) -> None:
        """Check the date of the upcoming Shabbat."""
        date = HDate(date=dt.date(*current_date))
        assert date.hdate == HebrewDate(*hebrew_date)
        next_shabbat = date.upcoming_shabbat
        assert next_shabbat.gdate == dt.date(*shabbat_date)

    @given(date=strategies.dates())
    def test_prev_and_next_day(self, date: dt.date) -> None:
        """Check the previous and next day attributes."""
        assert (HDate(date).previous_day.gdate - HDate(date).gdate) == dt.timedelta(-1)
        assert (HDate(date).next_day.gdate - HDate(date).gdate) == dt.timedelta(1)


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


@pytest.mark.parametrize("current_date, diaspora, dates", UPCOMING_SHABBAT_OR_YOM_TOV)
def test_get_next_shabbat_or_yom_tov(
    current_date: tuple[int, int, int],
    diaspora: bool,
    dates: dict[str, tuple[int, int, int]],
) -> None:
    """Test getting the next shabbat or Yom Tov works."""
    date = HDate(date=dt.date(*current_date), diaspora=diaspora)
    assert date.upcoming_shabbat_or_yom_tov.first_day.gdate == dt.date(*dates["start"])
    assert date.upcoming_shabbat_or_yom_tov.last_day.gdate == dt.date(*dates["end"])
