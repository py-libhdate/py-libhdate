"""Tests dealing with parshat hashavua."""

import datetime as dt

import pytest
from hypothesis import given, settings, strategies

from hdate import HDate, HebrewDate
from hdate.hebrew_date import Months

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
            list(range(44, 51))[61],
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
            list(range(44, 51))[61],
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
def test_get_reading_israel(year: int, parshiyot: list[list[int]]) -> None:
    """Test parshat hashavua in Israel."""
    mydate = HDate(language="english", diaspora=False)
    mydate.hdate = HebrewDate(year, 1, 1)

    # Get next Saturday
    tdelta = dt.timedelta((12 - mydate.gdate.weekday()) % 7)
    mydate.gdate += tdelta

    shabatot = [item for subl in parshiyot for item in subl]
    for shabbat in shabatot:
        print("Testing: ", mydate)
        assert mydate.get_reading() == shabbat
        mydate.gdate += dt.timedelta(days=7)
    mydate.hdate = HebrewDate(year, 1, 22)
    # VeZot Habracha in Israel always falls on 22 of Tishri
    assert mydate.get_reading() == 54


@pytest.mark.parametrize("year, parshiyot", READINGS_FOR_YEAR_DIASPORA)
def test_get_reading_diaspora(year: int, parshiyot: list[list[int]]) -> None:
    """Test parshat hashavua in the diaspora."""
    mydate = HDate(language="english", diaspora=True)
    mydate.hdate = HebrewDate(year, 1, 1)

    # Get next Saturday
    tdelta = dt.timedelta((12 - mydate.gdate.weekday()) % 7)
    mydate.gdate += tdelta

    shabatot = [item for subl in parshiyot for item in subl]
    for shabbat in shabatot:
        print("Testing: ", mydate)
        assert mydate.get_reading() == shabbat
        mydate.gdate += dt.timedelta(days=7)
    mydate.hdate = HebrewDate(year, 1, 23)
    # VeZot Habracha in Israel always falls on 22 of Tishri
    assert mydate.get_reading() == 54


@pytest.mark.parametrize("diaspora", [True, False])
@given(year=strategies.integers(min_value=4000, max_value=6000))
def test_nitzavim_always_before_rosh_hashana(year: int, diaspora: bool) -> None:
    """A property: Nitzavim alway falls before rosh hashana."""
    mydate = HDate(language="english", diaspora=diaspora)
    mydate.hdate = HebrewDate(year, Months.TISHREI, 1)
    tdelta = dt.timedelta((12 - mydate.gdate.weekday()) % 7 - 7)
    # Go back to the previous shabbat
    mydate.gdate += tdelta
    print("Testing date: {mydate} which is {tdelta} days before Rosh Hashana")
    assert mydate.get_reading() in [51, 61]


@pytest.mark.parametrize("diaspora", [True, False])
@given(year=strategies.integers(min_value=4000, max_value=6000))
@settings(deadline=None)  # Calculation of reading is slow
def test_vayelech_or_haazinu_always_after_rosh_hashana(
    year: int, diaspora: bool
) -> None:
    """A property: Vayelech or Haazinu always falls after rosh hashana."""
    mydate = HDate(language="english", diaspora=diaspora)
    mydate.hdate = HebrewDate(year, Months.TISHREI, 1)
    tdelta = dt.timedelta((12 - mydate.gdate.weekday()) % 7)
    # Go to the next shabbat (unless shabbat falls on Rosh Hashana)
    mydate.gdate += tdelta
    print(f"Testing date: {mydate} which is {tdelta} days after Rosh Hashana")
    assert mydate.get_reading() in [52, 53, 0]


def test_last_week_of_the_year() -> None:
    """The last day of the year is parshat Vayelech."""
    mydate = HDate()
    mydate.hdate = HebrewDate(5779, Months.ELUL, 29)
    assert mydate.get_reading() == 52
