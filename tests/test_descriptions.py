"""Tests for the calendar description properties.

These exercise the per-class ``description`` templates (read from each class's
own translation table), the ``HDateInfo`` ``*_obj`` accessors and the
``HolidayTypes`` translation.
"""

import datetime as dt

import pytest

from hdate import HDateInfo, HebrewDate, Zmanim
from hdate.daf_yomi import Masechta
from hdate.hebrew_date import Months
from hdate.holidays import HolidayDatabase, HolidayTypes
from hdate.omer import Nusach, Omer
from hdate.parasha import Parasha
from hdate.tekufot import Tekufot
from hdate.translator import Language, set_language
from hdate.zmanim import Zman


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


def _all_zmanim() -> dict[str, Zman]:
    """Collect every ``Zman`` a ``Zmanim`` can produce, keyed by name.

    The regular times all appear on any given day, while ``candle_lighting``
    and ``havdalah`` only materialise around Shabbat, so we sweep a two-week
    window to make sure every option is represented.
    """
    collected: dict[str, Zman] = {}
    start = dt.date(2024, 1, 1)
    for offset in range(14):
        zmanim = Zmanim(date=start + dt.timedelta(days=offset))
        collected.update(zmanim.zmanim)
        for obj in (zmanim.candle_lighting_obj, zmanim.havdalah_obj):
            if obj is not None:
                collected[obj.name] = obj
    return collected


@pytest.mark.parametrize("language", ["en", "fr", "he"])
def test_all_zmanim_translated(
    language: Language, caplog: pytest.LogCaptureFixture
) -> None:
    """Every zman option has a translated name and description in every language.

    This guards against a new zman being added without its ``_description``
    translation: ``Zman`` no longer falls back, so a missing key surfaces as
    the raw key plus a "not found" log entry.
    """
    set_language(language)
    zmanim = _all_zmanim()
    # Sanity check that the sweep actually collected the special-case times too.
    assert {"candle_lighting", "havdalah"} <= set(zmanim)

    for name, zman in zmanim.items():
        assert (
            zman.description != f"{name}_description"
        ), f"missing description for {name} ({language})"
        # Descriptions embed the local time via a {time} placeholder.
        assert zman.local.strftime("%H:%M") in zman.description

    # Zmanim are also stringified via their base name, so those keys must be
    # translated too -- including candle_lighting and havdalah, which are only
    # reachable through the *_obj accessors.
    for name, zman in zmanim.items():
        assert str(zman) != name, f"missing name translation for {name} ({language})"

    assert "not found" not in caplog.text


def test_calendar_objects_match_string_properties() -> None:
    """The ``*_obj`` accessors stringify to the existing string properties."""
    set_language("en")
    info = HDateInfo(date=dt.date(2024, 6, 15), diaspora=True)
    assert isinstance(info.parasha_obj, Parasha)
    assert isinstance(info.daf_yomi_obj, Masechta)
    assert str(info.parasha_obj) == info.parasha
    assert str(info.daf_yomi_obj) == info.daf_yomi


@pytest.mark.parametrize("language", ["en", "fr", "he"])
def test_classes_without_a_description_have_no_description(language: Language) -> None:
    """Classes with no ``description`` translation don't grow a bogus one.

    The base property must fail as a missing attribute rather than returning
    the literal key, so consumers can probe it with ``hasattr``.
    """
    set_language(language)
    for obj in (HDateInfo(date=dt.date(2024, 6, 15)), Zmanim(), Months.NISAN):
        assert not hasattr(obj, "description")
        with pytest.raises(AttributeError):
            _ = obj.description


def test_unnameable_class_cannot_be_stringified() -> None:
    """A class with no ``name`` attribute says so rather than mistranslating."""
    set_language("en")
    tekufot = Tekufot(dt.date(2024, 6, 15))
    with pytest.raises(NameError):
        _ = str(tekufot)


def test_omer_description_is_empty_outside_the_omer() -> None:
    """Outside the Omer there is no count, so there is nothing to describe."""
    set_language("en")
    omer = Omer(total_days=0, nusach=Nusach.SFARAD)
    assert str(omer) == ""
    assert omer.description == ""
