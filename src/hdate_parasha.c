/*  libhdate - Hebrew calendar library
 *
 *  Copyright (C) 1984-2003 Amos Shapir, 2004-2007  Yaacov Zamir <kzamir@walla.co.il>
 *  
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "hdate.h"
#include "support.h"

/**
 @brief Return number of hebrew parasha.
 
 @author Yaacov Zamir 2003-2005, Reading tables by Zvi Har'El

 @param hebdate The hdate_struct of the date to use.
 @param diaspora if True give diaspora readings
 @return the name of parasha 1. Bereshit etc..
 (55 trow 61 are joined strings e.g. Vayakhel Pekudei)
*/
int
hdate_get_parasha (hdate_struct const * h, int diaspora)
{
	static int join_flags[2][14][7] =
	{
		{
			{1, 1, 1, 1, 0, 1, 1}, /* 1 be erez israel */
			{1, 1, 1, 1, 0, 1, 0}, /* 2 */
			{1, 1, 1, 1, 0, 1, 1}, /* 3 */
			{1, 1, 1, 0, 0, 1, 0}, /* 4 */
			{1, 1, 1, 1, 0, 1, 1}, /* 5 */
			{0, 1, 1, 1, 0, 1, 0}, /* 6 */
			{1, 1, 1, 1, 0, 1, 1}, /* 7 */
			{0, 0, 0, 0, 0, 1, 1}, /* 8 */
			{0, 0, 0, 0, 0, 0, 0}, /* 9 */
			{0, 0, 0, 0, 0, 1, 1}, /* 10 */
			{0, 0, 0, 0, 0, 0, 0}, /* 11 */
			{0, 0, 0, 0, 0, 0, 0}, /* 12 */
			{0, 0, 0, 0, 0, 0, 1}, /* 13 */
			{0, 0, 0, 0, 0, 1, 1}  /* 14 */
		},
		{
			{1, 1, 1, 1, 0, 1, 1}, /* 1 in diaspora */
			{1, 1, 1, 1, 0, 1, 0}, /* 2 */
			{1, 1, 1, 1, 1, 1, 1}, /* 3 */
			{1, 1, 1, 1, 0, 1, 0}, /* 4 */
			{1, 1, 1, 1, 1, 1, 1}, /* 5 */
			{0, 1, 1, 1, 0, 1, 0}, /* 6 */
			{1, 1, 1, 1, 0, 1, 1}, /* 7 */
			{0, 0, 0, 0, 1, 1, 1}, /* 8 */
			{0, 0, 0, 0, 0, 0, 0}, /* 9 */
			{0, 0, 0, 0, 0, 1, 1}, /* 10 */
			{0, 0, 0, 0, 0, 1, 0}, /* 11 */
			{0, 0, 0, 0, 0, 1, 0}, /* 12 */
			{0, 0, 0, 0, 0, 0, 1}, /* 13 */
			{0, 0, 0, 0, 1, 1, 1}  /* 14 */
		}
	};
	
	int reading;
	
	/* if simhat tora return vezot habracha */
	if (h->hd_mon == 1)
	{
		/* simhat tora is a day after shmini atzeret outsite israel */
		if (h->hd_day == 22 && !diaspora) return 54;
		if (h->hd_day == 23 && diaspora) return 54;
	}
	
	
	if (h->hd_mon == 1 && h->hd_day == 22)
	{
		return 54;
	}
	
	/* if not shabat return none */
	if (h->hd_dw != 7)
	{
		return 0;
	}
	
	/* check for diaspora readings */
	diaspora = diaspora?1:0;
	
	switch (h->hd_weeks)
	{
	case  1:
		if (h->hd_new_year_dw == 7)
		{
			/* Rosh hashana */
			return 0;
		}
		else if ((h->hd_new_year_dw == 2) || (h->hd_new_year_dw == 3))
		{
			return 52;
		}
		else /* if (h->hd_new_year_dw == 5) */
		{
			return 53;
		}
		break;
	case  2:
		if (h->hd_new_year_dw == 5)
		{
			/* Yom kippur */
			return 0;
		}
		else
		{
			return 53;
		}
		break;
	case  3:
		/* Succot */
		return 0;
		break;
	case  4:
		if (h->hd_new_year_dw == 7)
		{
			/* Simhat tora in israel */
			if (!diaspora) return 54;
			/* Not simhat tora in diaspora */
			else return 0;
		}
		else
		{
			return 1;
		}
		break;
	default:
		/* simhat tora on week 4 bereshit too */
		reading = h->hd_weeks - 3;
		
		/* was simhat tora on shabat ? */
		if (h->hd_new_year_dw == 7)
			reading = reading - 1;
		
		/* no joining */
		if (reading < 22)
		{
			return reading;
		}
		
		/* pesach */
		if ((h->hd_mon == 7) && (h->hd_day > 14))
		{
			/* Shmini of pesach in diaspora is on the 22 of the month*/
			if (diaspora && (h->hd_day <= 22))
				return 0;
			if (!diaspora && (h->hd_day < 22))
				return 0;
		}
		
		/* Pesach allways removes one */
		if (((h->hd_mon == 7) && (h->hd_day > 21)) || (h->hd_mon > 7 && h->hd_mon < 13))
		{
			reading--;
			
			/* on diaspora, shmini of pesach may fall on shabat if next new year is on shabat */
			if (diaspora &&
				(((h->hd_new_year_dw + h->hd_size_of_year) % 7) == 2))
			{
				reading--;
			}
		}
		
		/* on diaspora, shavot may fall on shabat if next new year is on shabat */
		if (diaspora && 
			(h->hd_mon < 13) && 
			((h->hd_mon > 9) || (h->hd_mon == 9 && h->hd_day >= 7)) && 
			((h->hd_new_year_dw + h->hd_size_of_year) % 7) == 0)
		{
			if (h->hd_mon == 9 && h->hd_day == 7)
			{
				return 0;
			}
			else
			{
				reading--;
			}
		}
		
		/* joining */
		if (join_flags[diaspora][h->hd_year_type - 1][0] && (reading >= 22))
		{
			if (reading == 22)
			{
				return 55;
			}
			else
			{
				reading++;
			}
		}
		if (join_flags[diaspora][h->hd_year_type - 1][1] && (reading >= 27))
		{
			if (reading == 27)
			{
				return 56;
			}
			else
			{
				reading++;
			}
		}
		if (join_flags[diaspora][h->hd_year_type - 1][2] && (reading >= 29))
		{
			if (reading == 29)
			{
				return 57;
			}
			else
			{
				reading++;
			}
		}
		if (join_flags[diaspora][h->hd_year_type - 1][3] && (reading >= 32))
		{
			if (reading == 32)
			{
				return 58;
			}
			else
			{
				reading++;
			}
		}
		
		if (join_flags[diaspora][h->hd_year_type - 1][4] && (reading >= 39))
		{
			if (reading == 39)
			{
				return 59;
			}
			else
			{
				reading++;
			}
		}
		if (join_flags[diaspora][h->hd_year_type - 1][5] && (reading >= 42))
		{
			if (reading == 42)
			{
				return 60;
			}
			else
			{
				reading++;
			}
		}
		if (join_flags[diaspora][h->hd_year_type - 1][6] && (reading >= 51))
		{
			if (reading == 51)
			{
				return 61;
			}
			else
			{
				reading++;
			}
		}
		break;
	}

	return reading;
}
