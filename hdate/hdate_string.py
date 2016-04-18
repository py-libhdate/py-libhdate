from htables import digits
def hebrew_number(i, short_form=False):
    if i > 11000 or i < 0:
        raise ValueError('number must be between 0 to 11000, got:{}'.format(i))
    s = ''
    if i >= 1000:
        s += htables.digits[i/1000] 
        i = i % 1000
    while i >= 400:
        s += digits[2][4]
        i = i - 400
    if i >= 100:
        s += digits[2][i / 100]
        i = i % 100
    if i >= 10:
        if i in [15, 16]:
            i = i - 9
        s += digits[1][i / 10]
        i = i % 10
    if i > 0:
        s += digits[0][i]
    # possibly add the ' and " to hebrew numbers
    