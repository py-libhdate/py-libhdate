# -*- coding: utf-8 -*-

"""String functions returning the requested hebrew/english info."""

from hdate.htables import DIGITS, HEBREW_MONTHS, HOLIDAYS, PARASHAOT
from hdate.htables import DAYS_TABLE, ZMANIM_TYPES, ZMANIM_STRING


def hebrew_number(num, hebrew=True, short=False):
    """Return "Gimatria" number."""
    if not hebrew:
        return str(num)
    if not 0 < num < 10000:
        raise ValueError('num must be between 1 to 9999, got:{}'.format(num))
    hstring = u''
    if num >= 1000:
        hstring += DIGITS[0][num / 1000].decode("utf-8")
        hstring += "' ".decode("utf-8")
        num = num % 1000
    while num >= 400:
        hstring += DIGITS[2][4].decode("utf-8")
        num = num - 400
    if num >= 100:
        hstring += DIGITS[2][num / 100].decode("utf-8")
        num = num % 100
    if num >= 10:
        if num in [15, 16]:
            num = num - 9
        hstring += DIGITS[1][num / 10].decode("utf-8")
        num = num % 10
    if num > 0:
        hstring += DIGITS[0][num].decode("utf-8")
    # possibly add the ' and " to hebrew numbers
    if not short:
        if len(hstring) < 2:
            hstring += "'"
        else:
            hstring = hstring[:-1] + '"' + hstring[-1]
    return hstring


def get_hebrew_date(day, month, year, omer=0, dow=0, holiday=0,
                    short=False, hebrew=True):
    """Return a string representing the given date."""
    is_hebrew = 1 if hebrew else 0
    is_short = 1 if short else 0
    res = u'{} {}'.format(hebrew_number(day, hebrew=is_hebrew, short=is_short),
                          "ב".decode("utf-8") if is_hebrew else "")
    if is_hebrew:
        res += HEBREW_MONTHS[is_hebrew][month-1].decode("utf-8")
    else:
        res += HEBREW_MONTHS[is_hebrew][month-1]
    res += " " + hebrew_number(year, hebrew=is_hebrew, short=is_short)
    if dow:
        dw_str = ''
        if is_hebrew:
            dw_str = 'יום '
        dw_str += DAYS_TABLE[is_hebrew][is_short][dow-1]
        res = dw_str.decode("utf-8") + " " + res
    if is_short:
        return res
    if omer > 0 and omer < 50:
        res += " " + hebrew_number(omer, hebrew=is_hebrew, short=is_short)
        res += " " + "בעומר".decode("utf-8") if is_hebrew else " in the Omer"
    if holiday:
        res += " " + HOLIDAYS[is_hebrew][is_short][holiday-1].decode("utf-8")
    return res


def get_omer_string(omer):
    """Return a string representing the count of the Omer."""
    tens = ["", "עשרה", "עשרים", "שלושים", "ארבעים"]
    ones = ["", "אחד", "שנים", "שלושה", "ארבעה", "חמשה",
            "ששה", "שבעה", "שמונה", "תשעה"]
    if not 0 < omer < 50:
        raise ValueError('Invalid Omer day: {}'.format(omer))
    ten = omer / 10
    one = omer % 10
    omer_string = 'היום '
    if 10 < omer < 20:
        omer_string += ones[one] + ' עשר'
    elif omer > 9:
        omer_string += ones[one]
        if one:
            omer_string += ' ו'
    if omer > 2:
        if omer > 20 or omer in [10, 20]:
            omer_string += tens[ten]
        if omer < 11:
            omer_string += ones[one] + ' ימים '
        else:
            omer_string += ' יום '
    elif omer == 1:
        omer_string += 'יום אחד '
    else:  # omer == 2
        omer_string += 'שני ימים '
    if omer > 6:
        omer_string += 'שהם '
        weeks = omer / 7
        days = omer % 7
        if weeks > 2:
            omer_string += ones[weeks] + ' שבועות '
        elif weeks == 1:
            omer_string += 'שבוע אחד '
        else:  # weeks == 2
            omer_string += 'שני שבועות '
        if days:
            omer_string += 'ו'
            if days > 2:
                omer_string += ones[days] + ' ימים '
            elif days == 1:
                omer_string += 'יום אחד '
            else:  # days == 2
                omer_string += 'שני ימים '
    omer_string += 'לעומר'
    return omer_string


def get_parashe(parasha, short=False, hebrew=True):
    """Get the string representing the parasha."""
    is_hebrew = 1 if hebrew else 0
    is_short = 1 if short else 0
    res = PARASHAOT[is_hebrew][parasha]
    if is_short:
        return res
    return "{} {}".format("פרשת" if is_hebrew else "Parashat", res)


def get_zmanim_string(zmanim, hebrew=True):
    """Get the string representing the zmanim of the day."""
    res = ''
    lang = 'heb' if hebrew else 'eng'
    for zman in ZMANIM_TYPES:
        if zman in zmanim:
            time = zmanim[zman]
            res += '{} - {:02d}:{:02d}\n'.format(ZMANIM_STRING[lang][zman],
                                                 time.hour, time.minute)
    return res
