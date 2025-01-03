"""Tests relating to Sefirat HaOmer."""

import random

import pytest

from hdate.omer import Omer

OMER_STRINGS = [
    (1, "היום יום אחד לעומר"),
    (2, "היום שני ימים לעומר"),
    (3, "היום שלושה ימים לעומר"),
    (7, "היום שבעה ימים שהם שבוע אחד לעומר"),
    (8, "היום שמונה ימים שהם שבוע אחד ויום אחד לעומר"),
    (10, "היום עשרה ימים שהם שבוע אחד ושלושה ימים לעומר"),
    (13, "היום שלושה עשר יום שהם שבוע אחד וששה ימים לעומר"),
    (14, "היום ארבעה עשר יום שהם שני שבועות לעומר"),
    (17, "היום שבעה עשר יום שהם שני שבועות ושלושה ימים לעומר"),
    (19, "היום תשעה עשר יום שהם שני שבועות וחמשה ימים לעומר"),
    (28, "היום שמונה ועשרים יום שהם ארבעה שבועות לעומר"),
    (30, "היום שלושים יום שהם ארבעה שבועות ושני ימים לעומר"),
    (37, "היום שבעה ושלושים יום שהם חמשה שבועות ושני ימים לעומר"),
    (45, "היום חמשה וארבעים יום שהם ששה שבועות ושלושה ימים לעומר"),
    (49, "היום תשעה וארבעים יום שהם שבעה שבועות לעומר"),
]


@pytest.mark.parametrize("omer_day,hebrew_string", OMER_STRINGS)
def test_get_omer_string(omer_day: int, hebrew_string: str) -> None:
    """Test the value returned by calculating the Omer string."""
    assert get_omer_string(omer_day, language="hebrew") == hebrew_string


@pytest.mark.parametrize("omer_day", range(1, 50))
@pytest.mark.parametrize("language", ["hebrew", "english", "french"])
def test_get_omer(omer_day: int, language: str) -> None:
    """Test the value returned by calculating the Omer."""
    omer = Omer(total_days=omer_day, language=language)
    assert omer.count_str() == get_omer_string(omer_day, language=language)


def test_illegal_value() -> None:
    """Test passing illegal values to Omer."""
    with pytest.raises(ValueError):
        Omer(total_days=random.randint(50, 100))
    with pytest.raises(ValueError):
        Omer(total_days=random.randint(-100, 0))


def get_omer_string(omer: int, language: str = "hebrew") -> str:
    """Return a string representing the count of the Omer."""

    if not 0 < omer < 50:
        raise ValueError(f"Invalid Omer day: {omer}")

    if language == "hebrew":
        return _get_omer_string_hebrew(omer)
    if language == "english":
        return _get_omer_string_english(omer)
    if language == "french":
        return _get_omer_string_french(omer)

    return f"Today is day {omer} of the Omer."


def _get_omer_string_hebrew(omer: int) -> str:
    """Return a string representing the count of the Omer in hebrew."""
    tens = ["", "עשרה", "עשרים", "שלושים", "ארבעים"]
    ones = [
        "",
        "אחד",
        "שנים",
        "שלושה",
        "ארבעה",
        "חמשה",
        "ששה",
        "שבעה",
        "שמונה",
        "תשעה",
    ]

    omer_string = "היום "

    if 10 < omer < 20:
        omer_string += f"{ones[omer % 10]} עשר"
    elif omer >= 10:
        unit_part = ones[omer % 10]
        if omer % 10:
            unit_part += " ו"
        omer_string += unit_part + tens[omer // 10]
    else:

        if omer > 2:
            omer_string += ones[omer]

    if omer > 2:
        if omer < 11:
            omer_string += " ימים "
        else:
            omer_string += " יום "
    elif omer == 1:
        omer_string += "יום אחד "
    else:  # omer == 2
        omer_string += "שני ימים "

    if omer > 6:
        omer_string += "שהם "
        weeks, days = divmod(omer, 7)

        week_mapping = {1: "שבוע אחד ", 2: "שני שבועות "}
        omer_string += week_mapping.get(weeks, f"{ones[weeks]} שבועות ")

        if days:
            day_mapping = {1: "יום אחד ", 2: "שני ימים "}
            omer_string += "ו" + day_mapping.get(days, f"{ones[days]} ימים ")

    omer_string += "לעומר"
    return omer_string


def _get_omer_string_english(omer: int) -> str:
    """Return a string representing the count of the Omer in english."""
    ones = [
        "",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    teens = [
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]
    tens = ["", "", "twenty", "thirty", "forty"]
    omer_string = "Today is "
    if omer < 10:
        omer_string += ones[omer]
    elif 10 <= omer < 20:
        omer_string += teens[omer - 10]
    else:
        ten = omer // 10
        one = omer % 10
        omer_string += tens[ten]
        if one != 0:
            omer_string += "-" + ones[one]
    omer_string += " day"
    if omer != 1:
        omer_string += "s"
    omer_string += " of the Omer"
    # Add weeks and days
    weeks = omer // 7
    days = omer % 7
    if weeks > 0:
        omer_string += f", which is {weeks} week"
        if weeks != 1:
            omer_string += "s"
        if days > 0:
            omer_string += f" and {days} day"
            if days != 1:
                omer_string += "s"
    omer_string += "."
    return omer_string


def _get_omer_string_french(omer: int) -> str:
    """Return a string representing the count of the Omer in french."""
    ones = [
        "",
        "un",
        "deux",
        "trois",
        "quatre",
        "cinq",
        "six",
        "sept",
        "huit",
        "neuf",
    ]
    teens = [
        "dix",
        "onze",
        "douze",
        "treize",
        "quatorze",
        "quinze",
        "seize",
        "dix-sept",
        "dix-huit",
        "dix-neuf",
    ]
    tens = ["", "", "vingt", "trente", "quarante"]

    irregular_ordinals = {
        1: "premier",
        2: "deuxième",
        3: "troisième",
        4: "quatrième",
        5: "cinquième",
        6: "sixième",
        7: "septième",
        8: "huitième",
        9: "neuvième",
        10: "dixième",
        11: "onzième",
        12: "douzième",
        13: "treizième",
        14: "quatorzième",
        15: "quinzième",
        16: "seizième",
        20: "vingtième",
        30: "trentième",
        40: "quarantième",
    }

    # Init
    omer_string = "Aujourd'hui c'est le "

    ten = omer // 10
    one = omer % 10

    # Construction
    if omer in irregular_ordinals:
        ordinal = irregular_ordinals[omer]
    else:
        if omer < 10:
            number_word = ones[omer]
        elif 10 < omer < 20:
            number_word = teens[omer - 10]
        else:
            if one == 1 and ten > 1:
                number_word = tens[ten] + " et un"
            else:
                number_word = tens[ten]
                if one != 0:
                    number_word += "-" + ones[one]

        ordinal = number_word + "ième"

    omer_string += ordinal + " jour de l'Omer"
    # Add weeks and days
    weeks = omer // 7
    days = omer % 7

    if weeks > 0:
        omer_string += f", ce qui fait {weeks} semaine"
        if weeks != 1:
            omer_string += "s"
        if days > 0:
            omer_string += f" et {days} jour"
            if days != 1:
                omer_string += "s"

        omer_string += "."
    return omer_string
