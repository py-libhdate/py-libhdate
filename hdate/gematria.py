"""Gematria for hebrew numbers."""

from hdate.translator import get_language

DIGITS = (
    (" ", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"),
    ("ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"),
    (" ", "ק", "ר", "ש", "ת"),
)


def hebrew_number(num: int, short: bool = False) -> str:
    """Return "Gimatria" number."""
    if get_language() != "he":
        return str(num)
    if not 0 <= num < 10000:
        raise ValueError(f"num must be between 0 to 9999, got:{num}")
    hstring = ""
    if num >= 1000:
        hstring += DIGITS[0][num // 1000]
        hstring += "' "
        num = num % 1000
    while num >= 400:
        hstring += DIGITS[2][4]
        num = num - 400
    if num >= 100:
        hstring += DIGITS[2][num // 100]
        num = num % 100
    if num >= 10:
        if num in [15, 16]:
            num = num - 9
        hstring += DIGITS[1][num // 10]
        num = num % 10
    if num > 0:
        hstring += DIGITS[0][num]
    # possibly add the ' and " to hebrew numbers
    if not short:
        if len(hstring) < 2:
            hstring += "'"
        else:
            hstring = hstring[:-1] + '"' + hstring[-1]
    return hstring
