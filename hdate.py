import datetime


def M(h, p):
    return ((h * PARTS_IN_HOUR) + p)

PARTS_IN_HOUR = 1080
PARTS_IN_DAY = 24 * PARTS_IN_HOUR
PARTS_IN_WEEK = 7 * PARTS_IN_DAY
PARTS_IN_MONTH = PARTS_IN_DAY + M(12, 793)  # Tikun for regular month


class HDate(object):

    def __init__(self, date=None):
        if date is None:
            date = datetime.date.today()
        elif not isinstance(date, datetime.date):
            raise TypeError
        self._date = date

    def _M(self, h, p):
        return (h * self.PARTS_IN_HOUR) + p
        
    def _days_since_3744(self, hebrew_year):
        """Return: Number of days since 3,1,3744 """
        # Start point for calculation is Molad new year 3744 (16BC)
        years_from_3744 = hebrew_year - 3744
        molad_3744 = M(1 + 6, 779)  # Molad 3744 + 6 hours in parts
        # Time in months
        leap_months = (years_from_3744 * 7 + 1) / 19  # Number of leap months
        leap_left = (years_from_3744 * 7 + 1) % 19  # Months left of leap cycle
        months = years_from_3744 * 12 + leap_months  # Total Number of months
        # Time in parts and days
        parts = months * PARTS_IN_MONTH + molad_3744  # Molad This year + Molad 3744 - corections
        days = months * 28 + parts / PARTS_IN_DAY - 2  # 28 days in month + corections
        
        # Time left for round date in corections
        parts_left_in_week = parts % PARTS_IN_WEEK  # 28 % 7 = 0 so only corections counts
        parts_left_in_day = parts % PARTS_IN_DAY
        week_day = parts_left_in_week / PARTS_IN_DAY

        # Special cases of Molad Zaken
        if ((leap_left < 12 and week_day == 3 and
             parts_left_in_day >= M(9 + 6, 204)) or
            (leap_left < 7 and week_day == 2 and
             parts_left_in_day >= M(15 + 6, 589))):
            days += 1
            week_day += 1
        # ADU
        if (week_day == 1 or week_day == 4 or week_day == 6):
            days += 1
        return days

    def _get_size_of_hebrew_year(self, hebrew_year):
        """Return: total days in hebrew year"""
        return self._days_since_3744(hebrew_year + 1) - self._days_since_3744(hebrew_year)

    def _get_year_type(size_of_year, new_year_dw):
        """Return: type of the year
Args:
    size_of_year: Length of year in days
    new_year_dw First week day of year
table:
year type | year length | Tishery 1 day of week
| 1       | 353         | 2
| 2       | 353         | 7
| 3       | 354         | 3
| 4       | 354         | 5
| 5       | 355         | 2
| 6       | 355         | 5
| 7       | 355         | 7
| 8       | 383         | 2
| 9       | 383         | 5
|10       | 383         | 7
|11       | 384         | 3
|12       | 385         | 2
|13       | 385         | 5
|14       | 385         | 7
"""
        # Only 14 combinations of size and week day are posible
        year_types = [1, 0, 0, 2, 0, 3, 4, 0, 5, 0, 6, 7, 8, 0, 9, 10, 0, 11, 0, 0, 12, 0, 13, 14]
        
        # convert size and first day to 1..24 number
        # 2,3,5,7 -> 1,2,3,4
        # 353, 354, 355, 383, 384, 385 -> 0, 1, 2, 3, 4, 5
        offset = (new_year_dw + 1) / 2
        offset = offset + 4 * ((size_of_year % 10 - 3) + (size_of_year / 10 - 35))

        return year_types[offset - 1]

    def _gdate_to_jd(self, day, month, year):
        """Return: The julian day number
Compute Julian day from Gregorian day, month and year
Algorithm from the wikipedia's julian_day """
        a = (14 - month) / 12
        y = year + 4800 - a
        m = month + 12 * a - 3
        jdn = day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045
        return jdn

    def _hdate_to_jd(self, day, month, year):
        """Compute Julian day from Hebrew day, month and year
Return: julian day number,  1 of tishrey julians,  1 of tishrey julians next year"""
        if (month == 13):
            month = 6
        if (month == 14):
            month = 6
            day += 30
            
        # Calculate days since 1,1,3744
        days_from_3744 = self._days_from_3744(year)
        day = days_from_3744 + (59 * (month - 1) + 1) / 2 + day

        # length of year
        length_of_year = self._days_from_3744(year + 1) - days_from_3744
        # Special cases for this year
        if (length_of_year % 10 > 4 and month > 2):  # long Heshvan
            day += 1
        if (length_of_year % 10 < 4 and month > 3):  # short Kislev
            day -= 1
        if (length_of_year > 365 and month > 6):  # leap year
            day += 30

        # adjust to julian
        jd = day + 1715118
        jd_tishrey1 = days_from_3744 + 1715119
        jd_tishrey1_next_year = jd_tishrey1 + length_of_year
                        
        return jd, jd_tishrey1, jd_tishrey1_next_year

    
