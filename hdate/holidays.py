"""Holidays module, contains the holiday information and related functions."""

from __future__ import annotations

from bisect import bisect_left
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from itertools import product
from typing import Callable, ClassVar, Literal, Optional, Union

from hdate.hebrew_date import CHANGING_MONTHS, LONG_MONTHS, HebrewDate, Months, Weekday
from hdate.translator import TranslatorMixin


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


@dataclass(frozen=True)
class Holiday(TranslatorMixin):
    """Container class for holiday information."""

    type: HolidayTypes
    name: str
    date: Union[tuple[Union[int, tuple[int, ...]], Union[Months, tuple[Months, ...]]]]
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
            holiday: Holiday,
        ) -> product[tuple[int, ...]]:
            """Given a (days, months) pair, compute the cross product.

            If days and/or months are singletons, they are converted to a list.
            """
            return product(
                *([x] if isinstance(x, (int, Months)) else x for x in holiday.date)
            )

        for holiday in holidays:
            for date in holiday_dates_cross_product(holiday):
                index = HebrewDate(0, *reversed(date))
                if holiday.israel_diaspora == "ISRAEL":
                    cls._israel_holidays[index].append(holiday)
                elif holiday.israel_diaspora == "DIASPORA":
                    cls._diaspora_holidays[index].append(holiday)
                else:
                    cls._all_holidays[index].append(holiday)

    def lookup(self, date: HebrewDate) -> list[Holiday]:
        """Lookup the holidays for a given date."""
        if all(_date != date for _date in self._instance_holidays):
            return []
        holidays = next(
            h for _date, h in self._instance_holidays.items() if _date == date
        )
        return [
            holiday
            for holiday in holidays
            if all(func(date) for func in holiday.date_functions_list)
        ]

    def _get_filtered_holidays(
        self, types: Optional[Union[list[HolidayTypes], HolidayTypes]]
    ) -> dict[HebrewDate, list[Holiday]]:
        """Return a list of filtered holidays, based on type."""
        filtered_holidays = self._instance_holidays
        if types:
            types = [types] if isinstance(types, HolidayTypes) else types
            filtered_holidays = {
                _date: [holiday for holiday in holidays if holiday.type in types]
                for _date, holidays in self._instance_holidays.items()
                if any(holiday.type in types for holiday in holidays)
            }
        return filtered_holidays

    def lookup_holidays_for_year(
        self,
        date: HebrewDate,
        types: Optional[Union[list[HolidayTypes], HolidayTypes]] = None,
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
        next_date_idx = bisect_left(list(filtered_holidays.keys()), date)
        if next_date_idx == len(filtered_holidays.keys()):
            return HebrewDate(year=date.year + 1)
        next_date = list(filtered_holidays.keys())[next_date_idx]
        return next_date.replace(year=date.year)

    @classmethod
    def get_all_holiday_names(cls, language: str) -> set[str]:
        """Return all the holiday names in a given language."""

        result = []
        for holiday_list in [
            cls._diaspora_holidays,
            cls._israel_holidays,
            cls._all_holidays,
        ]:
            for holidays in holiday_list.values():
                holiday_names = {holiday.name for holiday in holidays}
                if {"yom_haatzmaut", "yom_hazikaron"} == holiday_names:
                    continue
                for holiday in holidays:
                    holiday.set_language(language)
                holiday_strs = sorted(set(str(holiday) for holiday in holidays))
                result.append(", ".join(holiday_strs))
        return set(result)


def correct_adar() -> Callable[[HebrewDate], Union[bool, Callable[[], bool]]]:
    """
    Return a lambda function.

    Lambda checks that the value of the month returned is correct depending on whether
    it's a leap year.
    """
    return lambda x: (
        (x.month not in [Months.ADAR, Months.ADAR_I, Months.ADAR_II])
        or (x.month == Months.ADAR and not x.is_leap_year())
        or (x.month in (Months.ADAR_I, Months.ADAR_II) and x.is_leap_year())
    )


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
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_rosh_hashana", (29, Months.ELUL)),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_i", (1, Months.TISHREI)),
    Holiday(HolidayTypes.YOM_TOV, "rosh_hashana_ii", (2, Months.TISHREI)),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_gedaliah",
        ((3, 4), Months.TISHREI),
        [move_if_not_on_dow(3, 4, Weekday.SATURDAY, Weekday.SUNDAY)],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_yom_kippur", (9, Months.TISHREI)),
    Holiday(HolidayTypes.YOM_TOV, "yom_kippur", (10, Months.TISHREI)),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_sukkot", (14, Months.TISHREI)),
    Holiday(HolidayTypes.YOM_TOV, "sukkot", (15, Months.TISHREI)),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_sukkot", (16, Months.TISHREI), [], "ISRAEL"
    ),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_sukkot", ((17, 18, 19, 20), Months.TISHREI)
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "hoshana_raba", (21, Months.TISHREI)),
    Holiday(
        HolidayTypes.YOM_TOV, "simchat_torah", (23, Months.TISHREI), [], "DIASPORA"
    ),
    Holiday(HolidayTypes.YOM_TOV, "simchat_torah", (22, Months.TISHREI), [], "ISRAEL"),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        ((25, 26, 27, 28, 29, 30), Months.KISLEV),
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "chanukah",
        ((1, 2, 3), Months.TEVET),
        [lambda x: ((x.short_kislev() and x.day == 3) or (x.day in [1, 2]))],
    ),
    Holiday(HolidayTypes.FAST_DAY, "asara_btevet", (10, Months.TEVET)),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bshvat", (15, Months.SHVAT)),
    Holiday(
        HolidayTypes.FAST_DAY,
        "taanit_esther",
        ((11, 13), (Months.ADAR, Months.ADAR_II)),
        [
            correct_adar(),
            move_if_not_on_dow(13, 11, Weekday.SATURDAY, Weekday.THURSDAY),
        ],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "purim",
        (14, (Months.ADAR, Months.ADAR_II)),
        [correct_adar()],
    ),
    Holiday(
        HolidayTypes.MELACHA_PERMITTED_HOLIDAY,
        "shushan_purim",
        (15, (Months.ADAR, Months.ADAR_II)),
        [correct_adar()],
    ),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_pesach", (14, Months.NISAN)),
    Holiday(HolidayTypes.YOM_TOV, "pesach", (15, Months.NISAN)),
    Holiday(
        HolidayTypes.HOL_HAMOED, "hol_hamoed_pesach", (16, Months.NISAN), [], "ISRAEL"
    ),
    Holiday(HolidayTypes.HOL_HAMOED, "hol_hamoed_pesach", ((17, 18, 19), Months.NISAN)),
    Holiday(HolidayTypes.EREV_YOM_TOV, "hol_hamoed_pesach", (20, Months.NISAN)),
    Holiday(HolidayTypes.YOM_TOV, "pesach_vii", (21, Months.NISAN)),
    Holiday(
        HolidayTypes.MODERN_HOLIDAY,
        "yom_haatzmaut",
        ((3, 4, 5), Months.IYYAR),
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
        ((3, 4, 5, 6), Months.IYYAR),
        [
            year_is_after(5763),
            move_if_not_on_dow(5, 4, Weekday.FRIDAY, Weekday.THURSDAY)  # type: ignore
            or move_if_not_on_dow(5, 3, Weekday.SATURDAY, Weekday.THURSDAY)
            or move_if_not_on_dow(5, 6, Weekday.MONDAY, Weekday.TUESDAY),
        ],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "lag_bomer", (18, Months.IYYAR)),
    Holiday(HolidayTypes.EREV_YOM_TOV, "erev_shavuot", (5, Months.SIVAN)),
    Holiday(HolidayTypes.YOM_TOV, "shavuot", (6, Months.SIVAN)),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tzom_tammuz",
        ((17, 18), Months.TAMMUZ),
        [move_if_not_on_dow(17, 18, Weekday.SATURDAY, Weekday.SUNDAY)],
    ),
    Holiday(
        HolidayTypes.FAST_DAY,
        "tisha_bav",
        ((9, 10), Months.AV),
        [move_if_not_on_dow(9, 10, Weekday.SATURDAY, Weekday.SUNDAY)],
    ),
    Holiday(HolidayTypes.MINOR_HOLIDAY, "tu_bav", (15, Months.AV)),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hashoah",
        ((26, 27, 28), Months.NISAN),
        [
            move_if_not_on_dow(27, 28, Weekday.SUNDAY, Weekday.MONDAY)  # type: ignore
            or move_if_not_on_dow(27, 26, Weekday.FRIDAY, Weekday.THURSDAY),
            year_is_after(5718),
        ],
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "yom_hazikaron",
        ((2, 3, 4), Months.IYYAR),
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
        ((2, 3, 4, 5), Months.IYYAR),
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
        (28, Months.IYYAR),
        [year_is_after(5727)],
    ),
    Holiday(HolidayTypes.YOM_TOV, "shmini_atzeret", (22, Months.TISHREI)),
    Holiday(HolidayTypes.YOM_TOV, "pesach_viii", (22, Months.NISAN), [], "DIASPORA"),
    Holiday(HolidayTypes.YOM_TOV, "shavuot_ii", (7, Months.SIVAN), [], "DIASPORA"),
    Holiday(HolidayTypes.YOM_TOV, "sukkot_ii", (16, Months.TISHREI), [], "DIASPORA"),
    Holiday(HolidayTypes.YOM_TOV, "pesach_ii", (16, Months.NISAN), [], "DIASPORA"),
    Holiday(
        HolidayTypes.ISRAEL_NATIONAL_HOLIDAY,
        "family_day",
        (30, Months.SHVAT),
        [year_is_after(5734)],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "memorial_day_unknown",
        (7, (Months.ADAR, Months.ADAR_II)),
        [correct_adar()],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "rabin_memorial_day",
        ((11, 12), Months.MARCHESHVAN),
        [
            move_if_not_on_dow(12, 11, Weekday.FRIDAY, Weekday.THURSDAY),
            year_is_after(5757),
        ],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.MEMORIAL_DAY,
        "zeev_zhabotinsky_day",
        (29, Months.TAMMUZ),
        [year_is_after(5764)],
        "ISRAEL",
    ),
    Holiday(
        HolidayTypes.ROSH_CHODESH,
        "rosh_chodesh",
        (1, tuple(set(Months) - {Months.TISHREI})),
        [correct_adar()],
    ),
    Holiday(
        HolidayTypes.ROSH_CHODESH,
        "rosh_chodesh",
        (30, LONG_MONTHS + CHANGING_MONTHS),
        [correct_adar()],
    ),
)

HolidayDatabase.register_holidays(list(HOLIDAYS))
