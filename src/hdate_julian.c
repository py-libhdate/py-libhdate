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

#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#include "hdate.h"
#include "support.h"

#define HOUR 1080
#define DAY  (24*HOUR)
#define WEEK (7*DAY)
#define M(h,p) ((h)*HOUR+p)
#define MONTH (DAY+M(12,793))	/* Tikun for regular month */

/**
 @brief Days since bet (?) Tishrey 3744
 
 @author Amos Shapir 1984 (rev. 1985, 1992) Yaacov Zamir 2003-2005 
 
 @param hebrew_year The Hebrew year
 @return Number of days since 3,1,3744
*/
int
hdate_days_from_3744 (int hebrew_year)
{
	int years_from_3744;
	int molad_3744;
	int leap_months;
	int leap_left;
	int months;
	int parts;
	int days;
	int parts_left_in_week;
	int parts_left_in_day;
	int week_day;

	/* Start point for calculation is Molad new year 3744 (16BC) */
	years_from_3744 = hebrew_year - 3744;
	molad_3744 = M (1 + 6, 779);	/* Molad 3744 + 6 hours in parts */

	/* Time in months */
	leap_months = (years_from_3744 * 7 + 1) / 19;	/* Number of leap months */
	leap_left = (years_from_3744 * 7 + 1) % 19;	/* Months left of leap cycle */
	months = years_from_3744 * 12 + leap_months;	/* Total Number of months */

	/* Time in parts and days */
	parts = months * MONTH + molad_3744;	/* Molad This year + Molad 3744 - corections */
	days = months * 28 + parts / DAY - 2;	/* 28 days in month + corections */

	/* Time left for round date in corections */
	parts_left_in_week = parts % WEEK;	/* 28 % 7 = 0 so only corections counts */
	parts_left_in_day = parts % DAY;
	week_day = parts_left_in_week / DAY;

	/* Special cases of Molad Zaken */
	if ((leap_left < 12 && week_day == 3
	     && parts_left_in_day >= M (9 + 6, 204)) ||
	    (leap_left < 7 && week_day == 2
	     && parts_left_in_day >= M (15 + 6, 589)))
	{
		days++, week_day++;
	}

	/* ADU */
	if (week_day == 1 || week_day == 4 || week_day == 6)
	{
		days++;
	}

	return days;
}

/**
 @brief Size of Hebrew year in days
 
 @param hebrew_year The Hebrew year
 @return Size of Hebrew year
*/
int
hdate_get_size_of_hebrew_year (int hebrew_year)
{
	return hdate_days_from_3744 (hebrew_year + 1) -
		hdate_days_from_3744 (hebrew_year);
}

/**
 @brief Return Hebrew year type based on size and first week day of year.
 
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
 
 @param size_of_year Length of year in days
 @param new_year_dw First week day of year
 @return A number for year type (1..14)
*/
int
hdate_get_year_type (int size_of_year, int new_year_dw)
{
	/* Only 14 combinations of size and week day are posible */
	static int year_types[24] =
		{1, 0, 0, 2, 0, 3, 4, 0, 5, 0, 6, 7,
		8, 0, 9, 10, 0, 11, 0, 0, 12, 0, 13, 14};
	
	int offset;
	
	/* convert size and first day to 1..24 number */
	/* 2,3,5,7 -> 1,2,3,4 */
	/* 353, 354, 355, 383, 384, 385 -> 0, 1, 2, 3, 4, 5 */
	offset = (new_year_dw + 1) / 2;
	offset = offset + 4 * ((size_of_year % 10 - 3) + (size_of_year / 10 - 35));
	
	/* some combinations are imposible */
	return year_types[offset - 1];
}

/**
 @brief Compute Julian day from Gregorian day, month and year
 Algorithm from the wikipedia's julian_day 

 @author Yaacov Zamir

 @param day Day of month 1..31
 @param month Month 1..12
 @param year Year in 4 digits e.g. 2001
 @return The julian day number
 */
int
hdate_gdate_to_jd (int day, int month, int year)
{
	int a;
	int y;
	int m;
	int jdn;
	
	a = (14 - month) / 12;
	y = year + 4800 - a;
	m = month + 12 * a - 3;
	
	jdn = day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045;
	
	return jdn;
}

/**
 @brief Compute Julian day from Hebrew day, month and year
 
 @author Amos Shapir 1984 (rev. 1985, 1992) Yaacov Zamir 2003-2005

 @param day Day of month 1..31
 @param month Month 1..14 (13 - Adar 1, 14 - Adar 2)
 @param year Hebrew year in 4 digits e.g. 5753
 @return The julian day number
 */
int
hdate_hdate_to_jd (int day, int month, int year, int *jd_tishrey1, int *jd_tishrey1_next_year)
{
	int length_of_year;
	int jd;
	int days_from_3744;

	/* Adjust for leap year */
	if (month == 13)
	{
		month = 6;
	}
	if (month == 14)
	{
		month = 6;
		day += 30;
	}

	/* Calculate days since 1,1,3744 */
	days_from_3744 = hdate_days_from_3744 (year);
	day = days_from_3744 + (59 * (month - 1) + 1) / 2 + day;

	/* length of year */
	length_of_year = hdate_days_from_3744 (year + 1) - days_from_3744;
	
	/* Special cases for this year */
	if (length_of_year % 10 > 4 && month > 2)	/* long Heshvan */
		day++;
	if (length_of_year % 10 < 4 && month > 3)	/* short Kislev */
		day--;
	if (length_of_year > 365 && month > 6)	/* leap year */
		day += 30;

	/* adjust to julian */
	jd = day + 1715118;

	/* return the 1 of tishrey julians */
	if (jd_tishrey1 && jd_tishrey1_next_year)
	{
		*jd_tishrey1 = days_from_3744 + 1715119;
		*jd_tishrey1_next_year = *jd_tishrey1 + length_of_year;
	}
	
	return jd;
}

/**
 @brief Converting from the Julian day to the Gregorian day
 Algorithm from 'Julian and Gregorian Day Numbers' by Peter Meyer 

 @author Yaacov Zamir ( Algorithm, Henry F. Fliegel and Thomas C. Van Flandern ,1968)

 @param jd Julian day
 @param d Return Day of month 1..31
 @param m Return Month 1..12
 @param y Return Year in 4 digits e.g. 2001
 */
void
hdate_jd_to_gdate (int jd, int *d, int *m, int *y)
{
	int l, n, i, j;
	l = jd + 68569;
	n = (4 * l) / 146097;
	l = l - (146097 * n + 3) / 4;
	i = (4000 * (l + 1)) / 1461001;	/* that's 1,461,001 */
	l = l - (1461 * i) / 4 + 31;
	j = (80 * l) / 2447;
	*d = l - (2447 * j) / 80;
	l = j / 11;
	*m = j + 2 - (12 * l);
	*y = 100 * (n - 49) + i + l;	/* that's a lower-case L */

	return;
}

/**
 @brief Converting from the Julian day to the Hebrew day
 
 @author Amos Shapir 1984 (rev. 1985, 1992) Yaacov Zamir 2003-2008

 @param jd Julian day
 @param day Return Day of month 1..31
 @param month Return Month 1..14 (13 - Adar 1, 14 - Adar 2)
 @param year Return Year in 4 digits e.g. 2001
 */
void
hdate_jd_to_hdate (int jd, int *day, int *month, int *year, int *jd_tishrey1, int *jd_tishrey1_next_year)
{
	int days;
	int size_of_year;
	int internal_jd_tishrey1, internal_jd_tishrey1_next_year;
	
	/* calculate Gregorian date */
	hdate_jd_to_gdate (jd, day, month, year);

	/* Guess Hebrew year is Gregorian year + 3760 */
	*year = *year + 3760;

	internal_jd_tishrey1 = hdate_days_from_3744 (*year) + 1715119;
	internal_jd_tishrey1_next_year = hdate_days_from_3744 (*year + 1) + 1715119;
	
	/* Check if computed year was underestimated */
	if (internal_jd_tishrey1_next_year <= jd)
	{
		*year = *year + 1;
		internal_jd_tishrey1 = internal_jd_tishrey1_next_year;
		internal_jd_tishrey1_next_year = hdate_days_from_3744 (*year + 1) + 1715119;
	}

	size_of_year = internal_jd_tishrey1_next_year - internal_jd_tishrey1;
	
	/* days into this year, first month 0..29 */
	days = jd - internal_jd_tishrey1;
	
	/* last 8 months allways have 236 days */
	if (days >= (size_of_year - 236)) /* in last 8 months */
	{
		days = days - (size_of_year - 236);
		*month = days * 2 / 59;
		*day = days - (*month * 59 + 1) / 2 + 1;
		
		*month = *month + 4 + 1;
		
		/* if leap */
		if (size_of_year > 355 && *month <=6)
			*month = *month + 8;
	}
	else /* in 4-5 first months */
	{
		/* Special cases for this year */
		if (size_of_year % 10 > 4 && days == 59) /* long Heshvan (day 30 of Heshvan) */
			{
				*month = 1;
				*day = 30;
			}
		else if (size_of_year % 10 > 4 && days > 59) /* long Heshvan */
			{
				*month = (days - 1) * 2 / 59;
				*day = days - (*month * 59 + 1) / 2;
			}
		else if (size_of_year % 10 < 4 && days > 87) /* short kislev */
			{
				*month = (days + 1) * 2 / 59;
				*day = days - (*month * 59 + 1) / 2 + 2;
			}
		else /* regular months */
			{
				*month = days * 2 / 59;
				*day = days - (*month * 59 + 1) / 2 + 1;
			}
			
		*month = *month + 1;
	}
	
	/* return the 1 of tishrey julians */
	if (jd_tishrey1 && jd_tishrey1_next_year)
	{
		*jd_tishrey1 = internal_jd_tishrey1;
		*jd_tishrey1_next_year = internal_jd_tishrey1_next_year;
	}
	
	return;
}

/********************************************************************************/
/********************************************************************************/

/**
 @brief compute date structure from the Gregorian date

 @param d Day of month 1..31
 @param m Month 1..12 ,  if m or d is 0 return current date.
 @param y Year in 4 digits e.g. 2001
 */
hdate_struct *
hdate_set_gdate (hdate_struct * h, int d, int m, int y)
{
	int jd;
	int jd_tishrey1, jd_tishrey1_next_year;
	
	if (!h) return NULL;
	
	/* check for null dates (kobi) */
	if ((d == 0) || (m == 0))
	{
		struct tm *tm;
		long t;
		/* FIXME: day start at 6:00 or 12:00 like in Gregorian cal. ? */
		t = time (0);
		tm = localtime (&t);
		d = tm->tm_mday;
		m = tm->tm_mon + 1;
		y = tm->tm_year + 1900;
	}
	
	h->gd_day = d;
	h->gd_mon = m;
	h->gd_year = y;
	
	jd = hdate_gdate_to_jd (d, m, y);
	hdate_jd_to_hdate (jd, &(h->hd_day), &(h->hd_mon), &(h->hd_year), &jd_tishrey1, &jd_tishrey1_next_year);
	
	h->hd_dw = (jd + 1) % 7 + 1;
	h->hd_size_of_year = jd_tishrey1_next_year - jd_tishrey1;
	h->hd_new_year_dw = (jd_tishrey1 + 1) % 7 + 1;
	h->hd_year_type = hdate_get_year_type (h->hd_size_of_year , h->hd_new_year_dw);
	h->hd_jd = jd;
	h->hd_days = jd - jd_tishrey1 + 1;
	h->hd_weeks = ((h->hd_days - 1) + (h->hd_new_year_dw - 1)) / 7 + 1;
	
	return (h);
}

/**
 @brief compute date structure from the Hebrew date

 @param d Day of month 1..31
 @param m Month 1..14 ,  if m or d is 0 return current date.
 @param y Year in 4 digits e.g. 5731
 */
hdate_struct *
hdate_set_hdate (hdate_struct * h, int d, int m, int y)
{
	int jd;
	int jd_tishrey1, jd_tishrey1_next_year;
	
	if (!h) return NULL;
	
	h->hd_day = d;
	h->hd_mon = m;
	h->hd_year = y;
	
	jd = hdate_hdate_to_jd (d, m, y, &jd_tishrey1, &jd_tishrey1_next_year);
	hdate_jd_to_gdate (jd, &(h->gd_day), &(h->gd_mon), &(h->gd_year));
	
	h->hd_dw = (jd + 1) % 7 + 1;
	h->hd_size_of_year = jd_tishrey1_next_year - jd_tishrey1;
	h->hd_new_year_dw = (jd_tishrey1 + 1) % 7 + 1;
	h->hd_year_type = hdate_get_year_type (h->hd_size_of_year , h->hd_new_year_dw);
	h->hd_jd = jd;
	h->hd_days = jd - jd_tishrey1 + 1;
	h->hd_weeks = ((h->hd_days - 1) + (h->hd_new_year_dw - 1)) / 7 + 1;
	
	return (h);
}

/**
 @brief compute date structure from julian day

 @param jd the julian day number.
 */
hdate_struct *
hdate_set_jd (hdate_struct * h, int jd)
{
	int jd_tishrey1, jd_tishrey1_next_year;
	
	if (!h) return NULL;
	
	hdate_jd_to_gdate (jd, &(h->gd_day), &(h->gd_mon), &(h->gd_year));
	hdate_jd_to_hdate (jd, &(h->hd_day), &(h->hd_mon), &(h->hd_year), &jd_tishrey1, &jd_tishrey1_next_year);
	
	h->hd_dw = (jd + 1) % 7 + 1;
	h->hd_size_of_year = jd_tishrey1_next_year - jd_tishrey1;
	h->hd_new_year_dw = (jd_tishrey1 + 1) % 7 + 1;
	h->hd_year_type = hdate_get_year_type (h->hd_size_of_year , h->hd_new_year_dw);
	h->hd_jd = jd;
	h->hd_days = jd - jd_tishrey1 + 1;
	h->hd_weeks = ((h->hd_days - 1) + (h->hd_new_year_dw - 1)) / 7 + 1;
	
	return (h);
}

/********************************************************************************/
/********************************************************************************/

/**
 @brief get the Gregorian day of the month

 @param h pointer this hdate struct.
 @return the Gregorian day of the month, 1..31.
 */
int
hdate_get_gday (hdate_struct const * h)
{
	return h->gd_day;
}

/**
 @brief get the Gregorian month

 @param h pointer this hdate struct.
 @return the Gregorian month, jan = 1.
 */
int
hdate_get_gmonth (hdate_struct const * h)
{
	return h->gd_mon;
}

/**
 @brief get the Gregorian year

 @param h pointer this hdate struct.
 @return the Gregorian year.
 */
int
hdate_get_gyear (hdate_struct const * h)
{
	return h->gd_year;
}

/**
 @brief get the Hebrew day of the month

 @param h pointer this hdate struct.
 @return the Hebrew day of the month, 1..30.
 */
int
hdate_get_hday (hdate_struct const * h)
{
	return h->hd_day;
}

/**
 @brief get the Hebrew month

 @param h pointer this hdate struct.
 @return the Hebrew month, Tishery = 1 .. Adar I =13, Adar II = 14.
 */
int
hdate_get_hmonth (hdate_struct const * h)
{
	return h->hd_mon;
}

/**
 @brief get the Hebrew year

 @param h pointer this hdate struct.
 @return the Hebrew year.
 */
int
hdate_get_hyear (hdate_struct const * h)
{
	return h->hd_year;
}

/**
 @brief get the day of the week

 @param h pointer this hdate struct.
 @return the the day of the week.
 */
int
hdate_get_day_of_the_week (hdate_struct const * h)
{
	return h->hd_dw;
}

/**
 @brief get the size of the hebrew year

 @param h pointer this hdate struct.
 @return the the size of the hebrew year.
 */
int
hdate_get_size_of_year (hdate_struct const * h)
{
	return h->hd_size_of_year;
}

/**
 @brief get the new year day of the week

 @param h pointer this hdate struct.
 @return the the new year day of the week.
 */
int
hdate_get_new_year_day_of_the_week (hdate_struct const * h)
{
	return h->hd_new_year_dw;
}

/**
 @brief get the Julian day number

 @param h pointer this hdate struct.
 @return the Julian day number.
 */
int
hdate_get_julian (hdate_struct const * h)
{
	return h->hd_jd;
}

/**
 @brief get the number of days passed since 1 tishrey

 @param h pointer this hdate struct.
 @return the number of days passed since 1 tishrey.
 */
int
hdate_get_days (hdate_struct const * h)
{
	return h->hd_days;
}

/**
 @brief get the number of weeks passed since 1 tishrey

 @param h pointer this hdate struct.
 @return the number of weeks passed since 1 tishrey.
 */
int
hdate_get_weeks (hdate_struct const * h)
{
	return h->hd_weeks;
}

/********************************************************************************/
/********************************************************************************/

/**
 @brief creat a new hdate struct object, must be deleted using delete_hdate.

 @return a new hdate object
 */
hdate_struct *
new_hdate ()
{
	/* allocate memory for a new hdate object */
	hdate_struct *h = (hdate_struct *) malloc (sizeof (hdate_struct));
	
	/* check for out of memory */
	if (!h)
		return NULL;
	
	/* get todays date */
	hdate_set_gdate (h, 0, 0, 0);
	
	return h;
}

/**
 @brief delete an hdate struct object.

 @param h pointer this hdate struct.
 */
hdate_struct *
delete_hdate (hdate_struct *h)
{
	/* if h exist delete it */
	if (h)
	{
		free (h);
		h = NULL;
	}

	return h;
}

