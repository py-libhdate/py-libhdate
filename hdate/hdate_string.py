# -*- coding: utf-8 -*-

from htables import DIGITS, HEBREW_MONTHS, HOLIDAYS, PARASHAOT, DAYS_TABLE
from htables import ZMANIM_TYPES, ZMANIM_STRING


def hebrew_number(num, hebrew=True, short=False):
    """
    Return "Gimatria" number
    """
    if not hebrew:
        return str(num)
    if num > 10000 or num < 0:
        raise ValueError('num must be between 0 to 9999, got:{}'.format(num))
    hstring = u''
    if num >= 1000:
        hstring += DIGITS[0][num / 1000].decode("utf-8")
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
    tens = ["", "עשרה", "עשרים", "שלושים", "ארבעים"]
    ones = ["", "אחד", "שנים", "שלושה", "ארבעה", "חמשה",
            "ששה", "שבעה", "שמונה", "תשעה"]
    if omer < 1 or omer > 49:
        raise ValueError('Invalid Omer day: {}'.format(omer))
    ten = omer / 10
    one = omer % 10
    omer_string = 'היום '
    if omer > 10 and omer < 20:
        omer_string += ones[one] + ' עשר '
    elif omer > 9:
        omer_string += tens[ten] + ' '
        if one:
            omer_string += 'ו'
    if omer > 2:
        omer_string += ones[one]
        if omer < 11:
            omer_string += ' ימים '
        else:
            omer_string += ' יום '
    elif omer == 1:
        omer_string += 'יום אחד '
    elif omer == 2:
        omer_string += 'שני ימים '
    if omer > 6:
        omer_string += 'שהם '
        weeks = omer / 7
        days = omer % 7
        if weeks > 2:
            omer_string += ones[weeks] + ' שבועות '
        elif weeks == 1:
            omer_string += 'שבוע אחד '
        elif weeks == 2:
            omer_string += 'שני שבועות '
        if days:
            omer_string += 'ו'
            if days > 2:
                omer_string += ones[days] + ' ימים '
            elif days == 1:
                omer_string += 'יום אחד '
            elif days == 2:
                omer_string += 'שני ימים '
    omer_string += 'לעומר'
    return omer_string


def get_parashe(parasha, short=False, hebrew=True):
    is_hebrew = 1 if hebrew else 0
    is_short = 1 if short else 0
    res = PARASHAOT[is_hebrew][parasha]
    if is_short:
        return res
    if is_hebrew:
        return "{} {}".format("פרשת" if is_hebrew else "Parashat", res)
    return


def get_zmanim_string(zmanim, hebrew=True):
    res = ''
    lang = 'heb' if hebrew else 'eng'
    for zman in ZMANIM_TYPES:
        if zman in zmanim:
            time = zmanim[zman]
            res += '{} - {:02d}:{:02d}\n'.format(ZMANIM_STRING[lang][zman],
                                                 time.hour, time.minute)
    return res
