/*  libhdate - Hebrew calendar library: http://libhdate.sourceforge.net
 * 
 *  Copyright (C) 2011-2012 Boruch Baum <boruch-baum@users.sourceforge.net>
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

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef ENABLE_NLS
#include <locale.h>
#endif

#include "hdate.h"
#include "support.h"

/**
 @brief convert an integer to hebrew string UTF-8 (logical)
 
 @param n The int to convert ( 0 < n < 11000)
 
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  Callers to this function must free() after using the memory
		  pointed to by the return value.
		  [deprecation date 2011-12-28]
          The original function outputted to a local static string,
          and suggested that the caller copied it away.
*/
char *
hdate_get_int_string (int const n)
{
	char *dest;
	int hebrew_form = HDATE_STRING_HEBREW;

	if (!hdate_is_hebrew_locale()) hebrew_form = HDATE_STRING_LOCAL;
	return hdate_string( HDATE_STRING_INT, n, HDATE_STRING_SHORT, hebrew_form);
}


/**
 @brief Return a static string, with name of week day.

 @param day_of_week The number of the day 1..7 (1 - sun).
 @param short_form A short flag (true - sun; false - sunday).
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_day_string (int const day_of_week, int const short_form)
{
	return hdate_string( HDATE_STRING_DOW, day_of_week, short_form, HDATE_STRING_LOCAL);
}

/**
 @brief Return a static string, with name of month.

 @param month The number of the month 1..12 (1 - jan).
 @param short_form A short flag.
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_month_string (int const month, int const short_form)
{
	return hdate_string( HDATE_STRING_GMONTH, month, short_form, HDATE_STRING_LOCAL);
}

/**
 @brief Return a static string, with name of hebrew month.

 @param month The number of the month 1..14 (1 - tishre, 13 - adar 1, 14 - adar 2).
 @param short_form A short flag.
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_hebrew_month_string (int const month, int const short_form)
{
	return hdate_string( HDATE_STRING_HMONTH, month, short_form, HDATE_STRING_LOCAL);
}

/**
 @brief Name of hebrew holiday.

 @param holiday The holiday number.
 @param short_text A short flag. 0=true, !0=false
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_holyday_string (int const holiday, int const short_text)
{
	return hdate_string( HDATE_STRING_HOLIDAY, holiday, short_text, HDATE_STRING_LOCAL);
}

/**
 @brief Name of Parasha

 @param parasha The Number of Parasha 1-Bereshit
	(55 through 61 are joined strings e.g. Vayakhel Pekudei)
 @param short_form A short flag. 0=true, !0 = false
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_parasha_string (int const parasha, int const short_form)
{
	return hdate_string( HDATE_STRING_PARASHA, parasha, short_form, HDATE_STRING_LOCAL);
}

/**
 @brief Return a string, with the day in the omer

 @param omer day The day in the omer.
 @return a pointer to a string with the day in the omer. The caller
         must free() the pointer after use.
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
 @attention The prior version of this function returned a pointer to a
          static string buffer. The current version returns a pointer to
          a malloc()ed buffer and needs to be free()d after use.
*/
char *
hdate_get_omer_string (int const omer_day)
{
	return hdate_string(	HDATE_STRING_OMER,
							omer_day,
							HDATE_STRING_LONG,
							HDATE_STRING_LOCAL);
							
}
