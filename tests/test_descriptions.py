"""Tests for the calendar label and description properties.

These exercise the per-class ``description`` templates (read from each class's
own translation table), the ``Zman`` label, the ``HDateInfo`` ``*_obj``
accessors and the ``HolidayTypes`` translation.
"""

import datetime as dt

import pytest

from hdate import HDateInfo, HebrewDate
from hdate.daf_yomi import Masechta
from hdate.hebrew_date import Months
from hdate.holidays import HolidayDatabase, HolidayTypes
from hdate.omer import Nusach, Omer
from hdate.parasha import Parasha
from hdate.translator import Language, set_language


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Hebrew date: 28 Nisan 5774"),
        ("he", 'תאריך עברי: כ"ח ניסן ה\' תשע"ד'),
    ],
)
def test_hebrew_date_description(language: Language, expected: str) -> None:
    """The Hebrew date description embeds the formatted date."""
    set_language(language)
    assert HebrewDate(5774, Months.NISAN, 28).description == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [("en", "Daf Yomi: Beitzah 29"), ("he", "דף יומי: ביצה כט")],
)
def test_daf_yomi_description(language: Language, expected: str) -> None:
    """The daf yomi object exposes a translated description."""
    set_language(language)
    daf = HDateInfo(date=dt.date(2014, 4, 28)).daf_yomi_obj
    assert isinstance(daf, Masechta)
    assert daf.description == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [("en", "Parshat Hashavua: Nasso"), ("he", "פרשת השבוע: נשא")],
)
def test_parasha_description(language: Language, expected: str) -> None:
    """The parasha object exposes a translated description."""
    set_language(language)
    parasha = HDateInfo(date=dt.date(2024, 6, 15), diaspora=True).parasha_obj
    assert isinstance(parasha, Parasha)
    assert parasha.description == expected


@pytest.mark.parametrize(
    ("language", "prefix"),
    [("en", "Sefirat HaOmer: "), ("he", "ספירת העומר: ")],
)
def test_omer_description(language: Language, prefix: str) -> None:
    """The omer description embeds the count string."""
    set_language(language)
    omer = Omer(total_days=25, nusach=Nusach.SFARAD)
    assert omer.description == f"{prefix}{omer.count_str()}"


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Jewish Holiday: Pesach\nHoliday type: Yom Tov"),
        ("he", "חג יהודי: פסח\nסוג החג: יום טוב"),
    ],
)
def test_holiday_description(language: Language, expected: str) -> None:
    """The holiday description includes the translated holiday type."""
    set_language(language)
    holiday = HolidayDatabase(diaspora=True).lookup(HebrewDate(5784, Months.NISAN, 15))[
        0
    ]
    assert holiday.description == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [("en", "Yom Tov"), ("he", "יום טוב"), ("fr", "Yom Tov")],
)
def test_holiday_type_value(language: Language, expected: str) -> None:
    """HolidayTypes is translatable via str()."""
    set_language(language)
    assert str(HolidayTypes.YOM_TOV) == expected


@pytest.mark.parametrize("language", ["en", "fr", "he"])
@pytest.mark.parametrize("holiday_type", list(HolidayTypes))
def test_holiday_type_all_translated(
    language: Language,
    holiday_type: HolidayTypes,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Every HolidayTypes member has a translation in every language."""
    set_language(language)
    assert str(holiday_type) != holiday_type.name
    assert "not found" not in caplog.text


def test_calendar_objects_match_string_properties() -> None:
    """The ``*_obj`` accessors stringify to the existing string properties."""
    set_language("en")
    info = HDateInfo(date=dt.date(2024, 6, 15), diaspora=True)
    assert isinstance(info.parasha_obj, Parasha)
    assert isinstance(info.daf_yomi_obj, Masechta)
    assert str(info.parasha_obj) == info.parasha
    assert str(info.daf_yomi_obj) == info.daf_yomi
