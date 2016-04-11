import hdate_julian as hj
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
        self.gdate = date
        hdate_set_gdate()
    
    def _set_h_from_jd(self, jd_tishrey1_next_year, jd_tishrey1):
         = (self._jd + 1) % 7 + 1
        self._h_size_of_year = jd_tishrey1_next_year - jd_tishrey1
        self._h_new_year_weekday = (jd_tishrey1 + 1) % 7 + 1
        self._h_year_type = hj._get_year_type (self._h_size_of_year , self._h_new_year_weekday)
        self._h_days = self._jd - jd_tishrey1 + 1
        self._h_weeks = ((self._h_days - 1) + (self._h_new_year_weekday - 1)) / 7 + 1        
    
    def hdate_set_gdate(self):
        self._jd = hj._gdate_to_jd(self.gdate.day, self.gdate.month, self.gdate.year)
        self._h_day, self._h_month, self._h_year, jd_tishrey1, jd_tishrey1_next_year = hj._jd_to_hdate(self._jd)
        self._set_h_from_jd(self._jd, jd_tishrey1, jd_tishrey1_next_year)
        
    def hdate_set_hdate(self, d, m, y):
        self._jd, jd_tishrey1, jd_tishrey1_next_year = hj._hdate_to_jd (d, m, y)
        gd, gm, gy = hj._jd_to_gdate (jd)
        self.gdate = datetime.date(gy, gm, gd)
        self._set_h_from_jd(self._jd, jd_tishrey1, jd_tishrey1_next_year)
        
    def hdate_set_jd(self, jd):
        gd, gm, gy = hj._jd_to_gdate(jd)
        self.gdate = datetime.date(gy, gm, gd)
        self.hdate_set_gdate()
    
    def get_hebrew_date(self):
        return self._h_day, self._h_month, self._h_year
        
    def get_holyday(self, diaspora=False):
        """return the number of holyday"""
        holyday = 0
        # holydays table
        holydays_table = [
            [	# Tishrey
                1, 2, 3, 3, 0, 0, 0, 0, 37, 4,
                0, 0, 0, 0, 5, 31, 6, 6, 6, 6,
                7, 27, 8, 0, 0, 0, 0, 0, 0, 0],
            [	# Heshvan
                0, 0, 0, 0, 0, 0, 0, 0, 0, 35,
                35, 35, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [	# Kislev
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 9, 9, 9, 9, 9, 9],
            [	# Tevet
                9, 9, 9, 0, 0, 0, 0, 0, 0, 10,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [	# Shvat
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 11, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 33],
            [	# Adar
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                12, 0, 12, 13, 14, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [	# Nisan
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 15, 32, 16, 16, 16, 16,
                28, 29, 0, 0, 0, 24, 24, 24, 0, 0],
            [	# Iyar
                0, 17, 17, 17, 17, 17, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 18, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 26, 0, 0],
            [	# Sivan
                0, 0, 0, 0, 19, 20, 30, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [	# Tamuz
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 21, 21, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 36, 36],
            [	# Av
                0, 0, 0, 0, 0, 0, 0, 0, 22, 22,
                0, 0, 0, 0, 23, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [	# Elul
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [	# Adar 1
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [	# Adar 2
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                12, 0, 12, 13, 14, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
    
        # sanity check
        if (self._h_month < 1 || self._h_month > 14 || self._h_day < 1 || self._h_day > 30):
            return 0
        
        holyday = holydays_table[self._h_month - 1][self._h_day - 1]
        
        # if tzom on sat delay one day
        # tzom gdalyaho on sat
        if ((holyday == 3) and (self._weekday == 7 || (self._h_day == 4 and self._weekday !=1))):
            holyday = 0
        # 17 of Tamuz on sat
        if ((holyday == 21) and ((self._weekday == 7) || (self._h_day == 18 and self._weekday != 1))):
            holyday = 0
        # 9 of Av on sat
        if ((holyday == 22) and ((self._weekday == 7) || (self._h_day == 10 and self._weekday != 1))):
            holyday = 0
        
        # Hanukah in a long year
        if ((holyday == 9) and (self._h_size_of_year % 10 != 3) and (self._h_day == 3)):
            holyday = 0
        
        # if tanit ester on sat mov to Thu
        if ((holyday == 12) and ((self._weekday == 7) || (self._h_day == 11 and self._weekday != 5))):
            holyday = 0
        
        # yom yerushalym after 68
        if (holyday == 26) and (self.gdate.year < 1968):
            holyday = 0 
        
        # yom ha azmaot and yom ha zicaron
        if (holyday == 17):
            if (self.gdate.year < 1948):
                holyday = 0
            elif (self.gdate.year < 2004):
                if ((self._h_day == 3) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 4) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 5) and (self._weekday != 6 and self._weekday != 7)):
                    holyday = 17
                elif ((self._h_day == 2) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 3) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 4) and (self._weekday != 5 and self._weekday != 6)):
                    holyday = 25
                else:
                    holyday = 0
            else:
                if ((self._h_day == 3) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 4) and (self._weekday == 5)):
                    holyday = 17
                elif ((self._h_day == 6) and (self._weekday == 3)):
                    holyday = 17
                elif ((self._h_day == 5) and (self._weekday != 6 and self._weekday != 7 and self._weekday != 2)):
                    holyday = 17
                elif ((self._h_day == 2) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 3) and (self._weekday == 4)):
                    holyday = 25
                elif ((self._h_day == 5) and (self._weekday == 2)):
                    holyday = 25
                elif ((self._h_day == 4) and (self._weekday != 5 and self._weekday != 6 and self._weekday != 1)):
                    holyday = 25
                else:
                    holyday = 0
        
        # yom ha shoaa, on years after 1958
        if (holyday == 24):
            if (self.gdate.year < 1958):
                holyday = 0
            else:
                if ((self._h_day == 26) and (self._weekday != 5)):
                    holyday = 0
                if ((self._h_day == 28) and (self._weekday != 2)):
                    holyday = 0
                if ((self._h_day == 27) and (self._weekday == 6 || self._weekday == 1)):
                    holyday = 0
        
        # Rabin day, on years after 1997
        if (holyday == 35):
            if (self.gdate.year < 1997):
                holyday = 0
            else:
                if ((self._h_day == 10 || self._h_day == 11) and (self._weekday != 5)):
                    holyday = 0
                if ((self._h_day == 12) and (self._weekday == 6 || self._weekday == 7)):
                    holyday = 0
        
        # Zhabotinsky day, on years after 2005
        if (holyday == 36):
            if (self.gdate.year < 2005):
                holyday = 0
            else:
                if ((self._h_day == 30) and (self._weekday != 1)):
                    holyday = 0
                if ((self._h_day == 29) and (self._weekday == 7)):
                    holyday = 0
        
        # diaspora holidays
        
        # simchat tora only in diaspora in israel just one day shmini+simchat tora
        if (holyday == 8 and !diaspora):
            holyday = 0
        
        # sukkot II holiday only in diaspora
        if (holyday == 31 and !diaspora):
            holyday = 6

        # pesach II holiday only in diaspora
        if (holyday == 32 and !diaspora):
            holyday = 16
        
        # shavot II holiday only in diaspora
        if (holyday == 30 and !diaspora):
            holyday = 0
        
        # pesach VIII holiday only in diaspora
        if (holyday == 29 and !diaspora):
            holyday = 0
        
        return holyday

    def get_omer_day(self):
        """return the day of the omer"""
        sixteen_nissan = HDate()
        sixteen_nissan.hdate_set_hdate(16, 7, self._h_year)
        omer_day = self._jd - sixteen_nissan._jd + 1
        if ((omer_day > 49) or (omer_day < 0)) :
            omer_day = 0

        return omer_day
