"""Test Tekufot objects."""

import datetime as dt

import pytest

from hdate.tekufot import Nusachim, Tekufot, TekufotNames
from hdate.translator import Language, set_language


@pytest.mark.parametrize(
    "date, expected",
    [
        (
            dt.date(2024, 11, 1),
            {
                "Tishrei": dt.datetime(2024, 10, 7, 3, 0),
                "Tevet": dt.datetime(2025, 1, 6, 10, 30),
                "Nissan": dt.datetime(2025, 4, 7, 18, 0),
                "Tammuz": dt.datetime(2025, 7, 8, 1, 30),
            },
        ),
        (
            dt.date(2026, 4, 7),
            {
                "Tishrei": dt.datetime(2025, 10, 7, 9, 0),
                "Tevet": dt.datetime(2026, 1, 6, 16, 30),
                "Nissan": dt.datetime(2026, 4, 8, 0, 0),
                "Tammuz": dt.datetime(2026, 7, 8, 7, 30),
            },
        ),
    ],
)
def test_get_tekufot(date: dt.date, expected: dict[TekufotNames, dt.datetime]) -> None:
    """Test that Tekufot calculations return the correct datetime values."""
    tekufot = Tekufot(date=date, diaspora=False)
    for key, expected_dt in expected.items():
        assert (
            actual := tekufot.get_tekufa(key)
        ) == expected_dt, f"Mismatch for {key}: {expected_dt=}, {actual=}"


@pytest.mark.parametrize(
    "date, diaspora, expected",
    [
        (dt.date(1924, 10, 5), True, dt.date(1924, 12, 5)),
        (dt.date(2024, 10, 5), True, dt.date(2024, 12, 5)),
        (dt.date(2024, 10, 5), False, dt.date(2024, 11, 8)),
        (dt.date(2023, 10, 5), True, dt.date(2023, 12, 6)),
        (dt.date(2123, 10, 5), True, dt.date(2123, 12, 7)),
    ],
)
def test_get_cheilat_geshamim(date: dt.date, expected: dt.date, diaspora: bool) -> None:
    """Test Cheilat Geshamim start dates based on location."""
    tekufot = Tekufot(date=date, diaspora=diaspora)
    result = tekufot.tchilat_geshamim.to_gdate()
    assert result == expected, "Cheilat Geshamim date mismatch"


# pylint: disable=line-too-long
# Pylint counts the hebrew vowels as separate characters
@pytest.mark.parametrize(
    "date, tradition, language, expected",
    [
        (
            dt.date(2024, 12, 13),
            "ashkenazi",
            "en",
            "Mashiv ha-ruach u-morid ha-geshem - VeTen Tal uMatar Livracha",
        ),
        (dt.date(2024, 12, 13), "sephardi", "he", "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרֵךְ עָלֵינוּ"),
        (dt.date(2025, 4, 25), "sephardi", "en", "Morid ha-tal - Barkheinu"),
        (dt.date(2025, 4, 25), "ashkenazi", "en", "(Silence) - VeTen Beracha"),
        (dt.date(2025, 4, 25), "ashkenazi", "he", "(שתיקה) - וְתֵן בְּרָכָה"),
        (
            dt.date(2026, 10, 10),
            "ashkenazi",
            "en",
            "Mashiv ha-ruach u-morid ha-geshem - VeTen Beracha",
        ),
        (dt.date(2026, 10, 10), "sephardi", "he", "מַשִּׁיב הָרוּחַ וּמוֹרִיד הַגֶּשֶׁם - בָּרְכֵנוּ"),
    ],
)
# pylint: enable=line-too-long
def test_tekufot_prayer_for_date(
    date: dt.date, tradition: Nusachim, language: Language, expected: str
) -> None:
    """
    Tests that the method get_prayer_for_date returns the expected phrase
    for each combination of (date, tradition, language).
    """
    set_language(language)
    tekufot = Tekufot(date=date, diaspora=True, tradition=tradition)
    actual_phrase = tekufot.get_prayer_for_date()
    assert (
        actual_phrase == expected
    ), f"{date=}, {tradition=}, {language=}\n{actual_phrase=} {expected=}\n"


def test_invalid_tekufa() -> None:
    """Test that an exception is raised when an invalid Tekufa is requested."""
    with pytest.raises(ValueError) as excinfo:
        Tekufot().get_tekufa("foo")  # type: ignore
    assert "Invalid Tekufot name: foo" in str(excinfo.value)
