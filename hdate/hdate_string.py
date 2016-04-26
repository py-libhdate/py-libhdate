# -*- coding: utf-8 -*-

from htables import digits, hebrew_months, holidays, parashaot, days_table, zmanim_types, zmanim_string
def hebrew_number(num, hebrew=True, short=False):
    """
    Return "Gimatria" number
    """
    if not hebrew:
        return str(num)
    if num > 10000 or num < 0:
        raise ValueError('number must be between 0 to 9999, got:{}'.format(num))
    s = u''
    if num >= 1000:
        s += digits[0][num /1000].decode("utf-8")
        num = num % 1000
    while num >= 400:
        s += digits[2][4].decode("utf-8")
        num = num - 400
    if num >= 100:
        s += digits[2][num  / 100].decode("utf-8")
        num = num % 100
    if num >= 10:
        if num in [15, 16]:
            num = num - 9
        s += digits[1][num  / 10].decode("utf-8")
        num = num % 10
    if num > 0:
        s += digits[0][num].decode("utf-8")
    # possibly add the ' and " to hebrew numbers
    if not short:
        if len(s) < 2:
            s+= "'"
        else:
            s = s[:-1] + '"' + s[-1]
    return s
    
def get_hebrew_date(day, month, year, omer=0, dw=0, holiday=0, short=False, hebrew=True):
    is_hebrew = 1 if hebrew else 0
    is_short = 1 if short else 0
    res = u'{} {}'.format(hebrew_number(day, hebrew=is_hebrew, short=is_short),
                               "ב".decode("utf-8") if is_hebrew else "")
    if is_hebrew:
        res += hebrew_months[is_hebrew][month-1].decode("utf-8")
    else:
        res += hebrew_months[is_hebrew][month-1]        
    res += " " + hebrew_number(year, hebrew=is_hebrew, short=is_short)
    if dw:
        dw_str = ''
        if is_hebrew:
            dw_str = 'יום '
        dw_str += days_table[is_hebrew][is_short][dw-1]
        res = dw_str.decode("utf-8") + " " +res
    if is_short:
        return res
    if omer > 0 and omer < 50:
        res += " " + hebrew_number(omer, hebrew=is_hebrew, short=is_short)
        res += " " + "בעומר".decode("utf-8") if is_hebrew else " in the Omer"
    if holiday:
        res += " " + holidays[is_hebrew][is_short][holiday-1].decode("utf-8")
    return res
 
def get_omer_string(omer):
    tens = ["", "עשרה", "עשרים", "שלושים", "ארבעים"]
    ones = ["", "אחד", "שנים", "שלושה", "ארבעה", "חמשה", "ששה", "שבעה", "שמונה", "תשעה"]
    if omer < 1 or omer > 49:
        raise ValueError('Invalid Omer day: {}'.format(omer))
    t = omer / 10
    o = omer % 10
    s = 'היום '
    if omer > 10 and omer < 20:
        s += ones[o] + ' עשר '        
    elif omer > 9 :
        s += tens[t] + ' '
        if o:
            s += 'ו'
    if omer > 2:
        s += ones[o]
        if omer < 11:
           s += ' ימים '
        else:
           s += ' יום '            
    elif omer == 1:
        s += 'יום אחד '
    elif omer == 2:
        s += 'שני ימים '
    if omer > 6:
        s += 'שהם '
        w = omer / 7
        d = omer % 7
        if w > 2 :
            s += ones[w] + ' שבועות '
        elif w == 1:
            s += 'שבוע אחד '
        elif w == 2:
            s += 'שני שבועות '
        if d:
            s += 'ו'
            if d > 2 :
                s += ones[d] + ' ימים '
            elif d == 1:
                s += 'יום אחד '
            elif d == 2:
                s += 'שני ימים '        
    s += 'לעומר'
    return s
 
def get_parashe(parasha, short=False, hebrew=True):
    is_hebrew = 1 if hebrew else 0
    is_short = 1 if short else 0
    res = parashaot[is_hebrew]
    if is_short:
        return res
    if is_hebrew:
        return "{} {}".format("פרשת" if is_hebrew else "Parashat", res)
    return 
    
def get_zmanim_string(zmanim, hebrew=True):
    res = ''
    lang = 'heb' if hebrew else 'eng'
    for z in zmanim_types:
        if z in zmanim:
            d = zmanim[z]
            res += '{} - {:02d}:{:02d}\n'.format(zmanim_string[lang][z], d.hour, d.minute)
    return res