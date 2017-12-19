# -*- coding: utf-8 -*-

"""String functions returning the requested hebrew/english info."""
from __future__ import division

from hdate.htables import DAYS
from hdate.htables import DIGITS
from hdate.htables import HOLIDAYS
from hdate.htables import MONTHS
from hdate.htables import PARASHAOT
from hdate.htables import ZMANIM


def hebrew_number(num, hebrew=True, short=False):
    """Return "Gimatria" number."""
    if not hebrew:
        return str(num)
    if not 0 <= num < 10000:
        raise ValueError('num must be between 0 to 9999, got:{}'.format(num))
    hstring = u""
    if num >= 1000:
        hstring += DIGITS[0][num // 1000]
        hstring += u"' "
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
            hstring += u"'"
        else:
            hstring = hstring[:-1] + u'"' + hstring[-1]
    return hstring


def get_hebrew_date(day, month, year, omer=0, dow=0, holiday=0,
                    short=False, hebrew=True):
    """Return a string representing the given date."""
    # Day
    res = u"{} {}".format(hebrew_number(day, hebrew=hebrew, short=short),
                          u"ב" if hebrew else u"")
    # Month
    res += MONTHS[month-1][hebrew]
    # Year
    res += u" " + hebrew_number(year, hebrew=hebrew, short=short)

    # Weekday
    if dow:
        dw_str = u"יום " if hebrew else u""
        dw_str += DAYS[dow-1][hebrew][short]
        res = dw_str + u" " + res
    if short:
        return res

    # Omer
    if 0 < omer < 50:
        res += u" " + hebrew_number(omer, hebrew=hebrew, short=short)
        res += u" " + u"בעומר" if hebrew else u" in the Omer"

    # Holiday
    for _holiday in (x for x in HOLIDAYS if x.index == holiday):
        desc = _holiday.description[hebrew]
        res += u" " + desc if not hebrew else desc[short]
    return res


def get_omer_string(omer):
    """Return a string representing the count of the Omer."""
    tens = [u"", u"עשרה", u"עשרים", u"שלושים", u"ארבעים"]
    ones = [u"", u"אחד", u"שנים", u"שלושה", u"ארבעה", u"חמשה",
            u"ששה", u"שבעה", u"שמונה", u"תשעה"]
    if not 0 < omer < 50:
        raise ValueError('Invalid Omer day: {}'.format(omer))
    ten = omer // 10
    one = omer % 10
    omer_string = u'היום '
    if 10 < omer < 20:
        omer_string += ones[one] + u' עשר'
    elif omer > 9:
        omer_string += ones[one]
        if one:
            omer_string += u' ו'
    if omer > 2:
        if omer > 20 or omer in [10, 20]:
            omer_string += tens[ten]
        if omer < 11:
            omer_string += ones[one] + u' ימים '
        else:
            omer_string += u' יום '
    elif omer == 1:
        omer_string += u'יום אחד '
    else:  # omer == 2
        omer_string += u'שני ימים '
    if omer > 6:
        omer_string += u'שהם '
        weeks = omer // 7
        days = omer % 7
        if weeks > 2:
            omer_string += ones[weeks] + u' שבועות '
        elif weeks == 1:
            omer_string += u'שבוע אחד '
        else:  # weeks == 2
            omer_string += u'שני שבועות '
        if days:
            omer_string += u'ו'
            if days > 2:
                omer_string += ones[days] + u' ימים '
            elif days == 1:
                omer_string += u'יום אחד '
            else:  # days == 2
                omer_string += u'שני ימים '
    omer_string += u'לעומר'
    return omer_string


def get_parashe(parasha, short=False, hebrew=True):
    """Get the string representing the parasha."""
    res = PARASHAOT[parasha][hebrew]
    if short:
        return res
    return u"{} {}".format(u"פרשת" if hebrew else u"Parashat", res)


def get_zmanim_string(zmanim, hebrew=True):
    """Get the string representing the zmanim of the day."""
    res = u""
    for zman in ZMANIM:
        if zman.zman in zmanim:
            time = zmanim[zman.zman]
            res += u"{} - {:02d}:{:02d}\n".format(
                zman.description[hebrew], time.hour, time.minute)
    return res
