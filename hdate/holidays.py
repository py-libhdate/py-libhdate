"""Holidays module, contains the holiday information and related functions."""

from __future__ import annotations

import datetime as dt
from bisect import bisect_left
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from itertools import product
from typing import Callable, ClassVar, Iterable, Literal, Optional, Union

from hdate.hebrew_date import CHANGING_MONTHS, LONG_MONTHS, HebrewDate, Months, Weekday
from hdate.translator import Language, TranslatorMixin


class HolidayTypes(Enum):
    """Container class for holiday type integer mappings."""

    YOM_TOV = 1
    EREV_YOM_TOV = 2
    HOL_HAMOED = 3
    MELACHA_PERMITTED_HOLIDAY = 4
    FAST_DAY = 5
    MODERN_HOLIDAY = 6
    MINOR_HOLIDAY = 7
    MEMORIAL_DAY = 8
    ISRAEL_NATIONAL_HOLIDAY = 9
    ROSH_CHODESH = 10


FilterType = Union[list[HolidayTypes], HolidayTypes]


@dataclass(frozen=True)
class Holiday(TranslatorMixin):
    """Container class for holiday information."""

    type: HolidayTypes
    name: str
    date: Union[tuple[Union[Months, tuple[Months, ...]], Union[int, tuple[int, ...]]]]
    date_functions_list: list[
        Callable[[HebrewDate], Union[bool, Callable[[], bool]]]
    ] = field(default_factory=list)
    israel_diaspora: Literal["ISRAEL", "DIASPORA", ""] = ""


@dataclass
class HolidayDatabase:
    """Container class for holiday information."""

    diaspora: bool

    _diaspora_holidays: ClassVar[dict[HebrewDate, list[Holiday]]]
    _israel_holidays: ClassVar[dict[HebrewDate, list[Holiday]]]
    _all_holidays: ClassVar[dict[HebrewDate, list[Holiday]]]

    def __post_init__(self) -> None:
        self._instance_holidays = deepcopy(self._all_holidays)
        if self.diaspora:
            for date, holidays in self._diaspora_holidays.items():
                self._instance_holidays[date].extend(holidays)
        else:
            for date, holidays in self._israel_holidays.items():
                self._instance_holidays[date].extend(holidays)
        self._instance_holidays = dict(sorted(self._instance_holidays.items()))

    @classmethod
    def register_holidays(cls, holidays: list[Holiday]) -> None:
        """Register a list of holidays with the holiday manager."""

        cls._diaspora_holidays = defaultdict(list)
        cls._israel_holidays = defaultdict(list)
        cls._all_holidays = defaultdict(list)

        def holiday_dates_cross_product(
            dates: Union[
                tuple[Union[Months, tuple[Months, ...]], Union[int, tuple[int, ...]]]
            ],
        ) -> Iterable[tuple[Months, int]]:
            """Given a (days, months) pair, compute the cross product.

            If days and/or months are singletons, they are converted to a list.
            """
            months = (dates[0],) if isinstance(dates[0], Months) else dates[0]
            days = (dates[1],) if isinstance(dates[1], int) else dates[1]

            return product(months, days)

        for holiday in holidays:
            for date in holiday_dates_cross_product(holiday.date):
                index = HebrewDate(0, *date)
                if holiday.israel_diaspora == "ISRAEL":
                    cls._israel_holidays[index].append(holiday)
                elif holiday.israel_diaspora == "DIASPORA":
                    cls._diaspora_holidays[index].append(holiday)
                else:
                    cls._all_holidays[index].append(holiday)

    def _get_filtered_holidays(
        self, types: Optional[FilterType]
    ) -> dict[HebrewDate, list[Holiday]]:
        """Return a list of filtered holidays, based on type."""
        filtered_holidays = deepcopy(self._instance_holidays)
        if types:
            types = [types] if isinstance(types, HolidayTypes) else types
            filtered_holidays = {
                _date: [holiday for holiday in holidays if holiday.type in types]
                for _date, holidays in filtered_holidays.items()
                if any(holiday.type in types for holiday in holidays)
            }
        return filtered_holidays

    def lookup(
        self, date: HebrewDate, types: Optional[FilterType] = None
    ) -> list[Holiday]:
        """Lookup the holidays for a given date."""
        filtered_holidays = self._get_filtered_holidays(types)
        if all(_date != date for _date in filtered_holidays):
            return []
        holidays = filtered_holidays[date.replace(year=0)]
        return [
            holiday
            for holiday in holidays
            if all(func(date) for func in holiday.date_functions_list)
        ]

    def lookup_holidays_for_year(
        self, date: HebrewDate, types: Optional[FilterType] = None
    ) -> dict[HebrewDate, list[Holiday]]:
        """Lookup the holidays for a given year."""
        filtered_holidays = self._get_filtered_holidays(types)
        result = {
            (real_date := _date.replace(year=date.year)): [
                holiday
                for holiday in holidays
                if all(func(real_date) for func in holiday.date_functions_list)
            ]
            for _date, holidays in filtered_holidays.items()
            if _date.valid_for_year(date.year)
        }
        return {
            _date: _holidays
            for _date, _holidays in result.items()
            if len(_holidays) > 0
        }

    def lookup_next_holiday(
        self,
        date: HebrewDate,
        types: Optional[Union[list[HolidayTypes], HolidayTypes]] = None,
    ) -> HebrewDate:
        """Lookup the next holiday for a given date (with optional type filter)."""
        filtered_holidays = self._get_filtered_holidays(types)
        valid_dates = [
            _date
            for _date in list(filtered_holidays.keys())
            if _date.valid_for_year(date.year)
        ]
        next_date_idx = bisect_left(valid_dates, date)
        if next_date_idx == len(valid_dates):
            return HebrewDate(year=date.year + 1)
        next_date = valid_dates[next_date_idx]
        return next_date.replace(year=date.year)

    def get_all_names(self, language: Language) -> list[str]:
        """Return all the holiday names in a given language."""
        result = {""}  # Empty string for case of no holiday
        for holidays in self._instance_holidays.values():
            holiday_names = {holiday.name for holiday in holidays}
            if {"yom_haatzmaut", "yom_hazikaron"} == holiday_names:
                continue
            for holiday in holidays:
                holiday.set_language(language)
            holiday_strs = list(dict.fromkeys(str(holiday) for holiday in holidays))
            result.add(", ".join(holiday_strs))
        return list(sorted(result))


@lru_cache
def is_yom_tov(date: Union[dt.date, HebrewDate], diaspora: bool = False) -> bool:
    """Helper method to check if a given date is a Yom Tov"""
    if isinstance(date, dt.date):
        date = HebrewDate.from_gdate(date)
    holidays = HolidayDatabase(diaspora).lookup(date, types=HolidayTypes.YOM_TOV)
    return len(holidays) > 0


def move_if_not_on_dow(
    original: int, replacement: int, dow_not_orig: Weekday, dow_replacement: Weekday
) -> Callable[[HebrewDate], bool]:
    """
    Return a lambda function.

    Lambda checks that either the original day does not fall on a given
    weekday, or that the replacement day does fall on the expected weekday.
    """
    return lambda x: (
        (x.day == original and x.dow() != dow_not_orig)
        or (x.day == replacement and x.dow() == dow_replacement)
    )


def year_is_before(year: int) -> Callable[[HebrewDate], bool]:
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is before the
    requested year.
    """
    return lambda x: x.year < year


def year_is_after(year: int) -> Callable[[HebrewDate], bool]:
    """
    Return a lambda function.

    Lambda checks that a given HDate object's hebrew year is after the
    requested year.
    """
    return lambda x: x.year > year


HOLIDAYS = (
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_rosh_hashana", (Months.ELUL, 29)),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_i", (Months.TISHREI, 1)),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_ii", (Months.TISHREI, 2)),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        (Months.TISHREI, (3, 4)),
        [move_if_not_on_dow(3, 4, Weekday.SATURDAY, Weekday.SUNDAY)],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_yom_kippur", (Months.TISHREI, 9)),
    Holiday(HolidayTypes.YOM_TOV, "yom_kippur", (Months.TISHREI, 10)),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_sukkot", (Months.TISHREI, 14)),
    Holiday(HolidayTypes.YOM_TOV, "sukkot", (Months.TISHREI, 15)),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_sukkot", (Months.TISHREI, 16), [], "ISRAEL"
    ),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_sukkot", (Months.TISHREI, (17, 18, 19, 20))
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "hoshana_raba", (Months.TISHREI, 21)),
    Holiday(
        HolidayTypes.YOM_TOV, "simchat_torah", (Months.TISHREI, 23), [], "DIASPORA"
    ),
    Holiday(HolidayTypes.YOM_TOV, "simchat_torah", (Months.TISHREI, 22), [], "ISRAEL"),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        (Months.KISLEV, (25, 26, 27, 28, 29, 30)),
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        (Months.TEVET, (1, 2, 3)),
        [lambda x: ((x.short_kislev() and x.day == 3) or (x.day in [1, 2]))],
    ),
    Holiday(HolidayTypes.FAST_DAY, "asara_btevet", (Months.TEVET, 10)),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bshvat", (Months.SHVAT, 15)),
    Holiday(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ((Months.ADAR, Months.ADAR_II), (11, 13)),
        [move_if_not_on_dow(13, 11, Weekday.SATURDAY, Weekday.THURSDAY)],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        ((Months.ADAR, Months.ADAR_II), 14),
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        ((Months.ADAR, Months.ADAR_II), 15),
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_pesach", (Months.NISAN, 14)),
    Holiday(HolidayTypes.YOM_TOV, "pesach", (Months.NISAN, 15)),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_pesach", (Months.NISAN, 16), [], "ISRAEL"
    ),
    Holiday(HolidayTypes.HOL_HAMOED, "hol_hamoed_pesach", (Months.NISAN, (17, 18, 19))),
    Holiday(HolidayTypes.EREV_YOM_TOV, "hol_hamoed_pesach", (Months.NISAN, 20)),
    Holiday(HolidayTypes.YOM_TOV, "pesach_vii", (Months.NISAN, 21)),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        (Months.IYYAR, (3, 4, 5)),
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(5, 4, Weekday.FRIDAY, Weekday.THURSDAY)  # type: ignore
            or move_if_not_on_dow(5, 3, Weekday.SATURDAY, Weekday.THURSDAY),
        ],
    ),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        (Months.IYYAR, (3, 4, 5, 6)),
        [
            year_is_after(5763),
            move_if_not_on_dow(5, 4, Weekday.FRIDAY, Weekday.THURSDAY)  # type: ignore
            or move_if_not_on_dow(5, 3, Weekday.SATURDAY, Weekday.THURSDAY)
            or move_if_not_on_dow(5, 6, Weekday.MONDAY, Weekday.TUESDAY),
        ],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "lag_bomer", (Months.IYYAR, 18)),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_shavuot", (Months.SIVAN, 5)),
    Holiday(HolidayTypes.YOM_TOV, "shavuot", (Months.SIVAN, 6)),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        (Months.TAMMUZ, (17, 18)),
        [move_if_not_on_dow(17, 18, Weekday.SATURDAY, Weekday.SUNDAY)],
    ),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        (Months.AV, (9, 10)),
        [move_if_not_on_dow(9, 10, Weekday.SATURDAY, Weekday.SUNDAY)],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bav", (Months.AV, 15)),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hashoah",
        (Months.NISAN, (26, 27, 28)),
        [
            move_if_not_on_dow(27, 28, Weekday.SUNDAY, Weekday.MONDAY)  # type: ignore
            or move_if_not_on_dow(27, 26, Weekday.FRIDAY, Weekday.THURSDAY),
            year_is_after(5718),
        ],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        (Months.IYYAR, (2, 3, 4)),
        [
            year_is_after(5708),
            year_is_before(5764),
            move_if_not_on_dow(
                4, 3, Weekday.THURSDAY, Weekday.WEDNESDAY
            )  # type: ignore
            or move_if_not_on_dow(4, 2, Weekday.FRIDAY, Weekday.WEDNESDAY),
        ],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        (Months.IYYAR, (2, 3, 4, 5)),
        [
            year_is_after(5763),
            move_if_not_on_dow(
                4, 3, Weekday.THURSDAY, Weekday.WEDNESDAY
            )  # type: ignore
            or move_if_not_on_dow(4, 2, Weekday.FRIDAY, Weekday.WEDNESDAY)
            or move_if_not_on_dow(4, 5, Weekday.SUNDAY, Weekday.MONDAY),
        ],
    ),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_yerushalayim",
        (Months.IYYAR, 28),
        [year_is_after(5727)],
    ),
    Holiday(HolidayTypes.YOM_TOV, "shmini_atzeret", (Months.TISHREI, 22)),
    Holiday(HolidayTypes.YOM_TOV, "pesach_viii", (Months.NISAN, 22), [], "DIASPORA"),
    Holiday(HolidayTypes.YOM_TOV, "shavuot_ii", (Months.SIVAN, 7), [], "DIASPORA"),
    Holiday(HolidayTypes.YOM_TOV, "sukkot_ii", (Months.TISHREI, 16), [], "DIASPORA"),
    Holiday(HolidayTypes.YOM_TOV, "pesach_ii", (Months.NISAN, 16), [], "DIASPORA"),
    Holiday(
        HolidayTypes.ISRAEL_NATIONAL_HOLIDAY,
        "family_day",
        (Months.SHVAT, 30),
        [year_is_after(5733)],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "memorial_day_unknown",
        ((Months.ADAR, Months.ADAR_II), 7),
        [],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        (Months.MARCHESHVAN, (11, 12)),
        [
            move_if_not_on_dow(12, 11, Weekday.FRIDAY, Weekday.THURSDAY),
            year_is_after(5757),
        ],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "zeev_zhabotinsky_day",
        (Months.TAMMUZ, 29),
        [year_is_after(5764)],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.ROSH_CHODESH,
        "rosh_chodesh",
        (tuple(set(Months) - {Months.TISHREI}), 1),
    ),
    Holiday(
        HolidayTypes.ROSH_CHODESH, "rosh_chodesh", (LONG_MONTHS + CHANGING_MONTHS, 30)
    ),
)

HolidayDatabase.register_holidays(list(HOLIDAYS))
