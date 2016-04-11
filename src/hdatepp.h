/*  libhdate - Hebrew calendar library
 *
 *  Copyright (C) 2011-2012 Boruch Baum  <boruch-baum@users.sourceforge.net>
 *                2004-2007 Yaacov Zamir <kzamir@walla.co.il>
 *                1984-2003 Amos Shapir
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

/** @file hdatepp.h
    @brief libhdate C++ language header.
    
    libhdate - Hebrew calendar library, the C++ language header file.
*/

#ifndef __HDATE_PP_H__
#define __HDATE_PP_H__

#include <hdate.h>

/**
 @brief the libhdate namespace.
 */
namespace hdate 
{
		
	/**
	 @brief Hdate class.
	
	 class for Hebrew/Gregorian date conversions
	 */
	class Hdate
	{
		
	public:
		////////////////////////////////////////
		////////////////////////////////////////
		
		/**
		 @brief Hdate constructor.
		 */
		Hdate()
		{
			/* default is this day */
			h = new_hdate();
			
			/* default is in israel */
			diaspora = HDATE_ISRAEL_FLAG;
			
			/* default localeconv is Tel-Aviv winter time */
			latitude = 32.0;
			longitude = -34.0;
			tz = 2;
		}
		
		/**
		 @brief Hdate destructor.
		 */
		~Hdate()
		{
			delete_hdate(h);
		}
		
		////////////////////////////////////////
		////////////////////////////////////////
		
		/**
		 @brief compute date structure from the Gregorian date
		
		 @param d Day of month 1..31
		 @param m Month 1..12 ,  if m or d is 0 return current date.
		 @param y Year in 4 digits e.g. 2001
		 */
		void
		set_gdate (int d, int m, int y)
		{
			hdate_set_gdate (h, d, m, y);
		}
		
		/**
		 @brief compute date structure from the Hebrew date
		
		 @param d Day of month 1..31
		 @param m Month 1..14 ,  if m or d is 0 return current date.
		 @param y Year in 4 digits e.g. 5731
		 */
		void
		set_hdate (int d, int m, int y)
		{
			hdate_set_hdate (h, d, m, y);
		}
		
		/**
		 @brief compute date structure from the Julian day
		
		 @param jd the julian day number.
		 */
		void
		set_jd (int jd)
		{
			hdate_set_jd (h, jd);
		}
		
		////////////////////////////////////////
		////////////////////////////////////////
		
		/**
		 @brief Return a string, with the hebrew date.
		
		 @return NULL pointer upon failure or, upon success, a pointer to a
		 string containing the short ( e.g. "1 Tishrey" ) or long (e.g. "Tuesday
		 18 Tishrey 5763 Hol hamoed Sukot" ) formated date. You must free() the
		 pointer after use.
		
		 @param h The hdate_struct of the date to print.
		 @param diaspora if true give diaspora holydays
		 @param short_format A short flag (true - returns a short string, false returns a long string).
		
		 @warning This was originally written using a local static string,
		          calling for output to be copied away.

		*/
		char *
		get_format_date (int s)
		{
			return hdate_get_format_date (h, diaspora, s);
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
		get_day_of_week_string (int short_form)
		{
			//return hdate_get_day_string (h->hd_dw, s);
			return hdate_string( HDATE_STRING_HMONTH, h->hd_dw, short_form, HDATE_STRING_LOCAL);	
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
		get_month_string (int short_form)
		{
			//return hdate_get_month_string (h->gd_mon, s);
			return hdate_string( HDATE_STRING_GMONTH, h->gd_mon, short_form, HDATE_STRING_LOCAL);	
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
		get_hebrew_month_string (int short_form)
		{
			//return hdate_get_hebrew_month_string (h->hd_mon, s);
			return hdate_string( HDATE_STRING_HMONTH, h->hd_mon, short_form, HDATE_STRING_LOCAL);	
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
		get_holyday_string (int s)
		{
			int holiday;
			
			holiday = hdate_get_holyday (h, diaspora);
			//return hdate_get_holyday_string (holyday, s);
			return hdate_string( HDATE_STRING_HOLIDAY, holiday, HDATE_STRING_LONG, HDATE_STRING_LOCAL);	

		}
		
		/**
		 @brief get the day of the omer
		
		 @return return The day in the omer, starting from 1 (or 0 if not in sfirat ha omer)
		*/
		int
		get_omer_day ()
		{
			return hdate_get_omer_day (h);
		}
		
		/**
		 @brief get the hebrew holiday type.
		
		 @return the holiday type 
		*/
		int
		get_holyday_type ()
		{
			int holyday;
			
			holyday = hdate_get_holyday (h, diaspora);
			return hdate_get_holyday_type (holyday);
		}
		
		/**
		 @brief Name of Parasha
		
		 @param parasha The Number of Parasha 1-Bereshit
			(55 trow 61 are joined strings e.g. Vayakhel Pekudei)
		 @param short_form A short flag. 0=true, !0 = false
		 @warning DEPRECATION: This function is now just a wrapper for
		          hdate_string, and is subject to deprecation.
				  [deprecation date 2011-12-28]
		*/
		char *
		get_parasha_string (int s)
		{
			int parasha;
			
			parasha = hdate_get_parasha (h, diaspora);
			//return hdate_get_parasha_string (parasha, s);
			return hdate_string( HDATE_STRING_PARASHA, parasha, HDATE_STRING_LONG, HDATE_STRING_LOCAL);	

		}
		
		/**
		 @brief get name hebrew year.

		 @param n The int to convert ( 0 < n < 11000)
		 @return a string of the hebrew number UTF-8 (logical)
		 @warning DEPRECATION: This function is now just a wrapper for
		          hdate_string, and is subject to deprecation.
				  Callers to this function must free() after using the memory
				  pointed to by the return value.
		          The original function outputted to a local static string,
		          and suggested that the caller copied it away.
				  [deprecation date 2011-12-28]
		*/
		char *
		get_hebrew_year_string ()
		{
			//return hdate_get_int_string (h->hd_year);
			return hdate_string( HDATE_STRING_INT, h->hd_year, HDATE_STRING_LONG, HDATE_STRING_LOCAL);	

		}
		
		/**
		 @brief get name hebrew hebrew day of the month
		
		 @param n The int to convert ( 0 < n < 11000)
		 @return a string of the hebrew number UTF-8 (logical)
		 @warning DEPRECATION: This function is now just a wrapper for
		          hdate_string, and is subject to deprecation.
				  Callers to this function must free() after using the memory
				  pointed to by the return value.
		          The original function outputted to a local static string,
		          and suggested that the caller copied it away.
   				  [deprecation date 2011-12-28]

		*/
		char *
		get_hebrew_day_string ()
		{
			// return hdate_get_int_string (h->hd_day);
			return hdate_string( HDATE_STRING_HMONTH, h->hd_day, HDATE_STRING_LONG, HDATE_STRING_LOCAL);	
		}

		/**
		 @brief   Return string values for hdate information
		 @return  a pointer to a string containing the information. In the cases
		          integers and omer, the strings will NOT be static, and the
		          caller must free() them after use. Returns a null pointer
		          upon failure.
		 @param type_of_string 	0 = integer, 1 = day of week, 2 = parshaot,
								3 = hmonth, 4 = gmonth, 5 = holiday, 6 = omer
		 @param index			integer		( 0 < n < 11000)
								day of week ( 0 < n <  8 )
								parshaot	( 0 , n < 62 )
								hmonth		( 0 < n < 15 )
								gmonth		( 0 < n < 13 )
								holiday		( 0 < n < 37 )
								omer		( 0 < n < 50 )
		 @param short_form   0 = short format
		 @param hebrew_form  0 = not hebrew (native/embedded)
		*/
		char* get_string()
		{
			return hdate_string( type_of_string, index, short_form, hebrew_form);		
		}
		////////////////////////////////////////
		////////////////////////////////////////
		
		/**
		 @brief get parash number

		@return the hebrew parasha number
		*/
		int
		get_parasha ()
		{
			return hdate_get_parasha (h, diaspora);
		}
		
		/**
		 @brief get holiday number
		 @return the hebrew holiday number
		*/
		int
		get_holyday ()
		{
			return hdate_get_holyday (h, diaspora);
		}
		
		/**
		 @brief get Gregorian day of the month
		
		 @return the Gregorian day of the month
		*/
		int
		get_gday ()
		{
			return hdate_get_gday (h);
		}
		
		/**
		 @brief get Gregorian month
		
		 @return the Gregorian month
		*/
		int
		get_gmonth ()
		{
			return hdate_get_gmonth (h);
		}
		
		/**
		 @brief get Gregorian year
		
		 @return the Gregorian year
		*/
		int
		get_gyear ()
		{
			return hdate_get_gyear (h);
		}
		
		/**
		 @brief get Hebrew day of the month
		
		 @return the Hebrew day of the month
		*/
		int
		get_hday ()
		{
			return hdate_get_hday (h);
		}
		
		/**
		 @brief get Hebrew month
		
		 @return the Hebrew month
		*/
		int
		get_hmonth ()
		{
			return hdate_get_hmonth (h);
		}
		
		/**
		 @brief get Hebrew year
		
		 @return the Hebrew year
		*/
		int
		get_hyear ()
		{
			return hdate_get_hyear (h);
		}
		
		/**
		 @brief get the day of the week
		
		 @return the day of the week
		*/
		int
		get_day_of_the_week ()
		{
			return hdate_get_day_of_the_week (h);
		}
		
		/**
		 @brief get the size of the Hebrew year in days
		
		 @return the size of the Hebrew year in days
		*/
		int
		get_size_of_year ()
		{
			return hdate_get_size_of_year (h);
		}
		
		/**
		 @brief get the day of the week of hebrew new years
		
		 @return the day of the week of hebrew new years
		*/
		int
		get_new_year_day_of_the_week ()
		{
			return hdate_get_new_year_day_of_the_week (h);
		}
		
		/**
		 @brief get the Julian day number
		
		 @return the Julian day number
		*/
		int
		get_julian ()
		{
			return hdate_get_julian (h);
		}
		
		/**
		 @brief get the number of days sice Tishrey I
		
		 @return the the number of days sice Tishrey I
		*/
		int
		get_days ()
		{
			return hdate_get_days (h);
		}
		
		/**
		 @brief get the number of weeks sice Tishrey I
		
		 @return the the number of weeks sice Tishrey I
		*/
		int
		get_weeks ()
		{
			return hdate_get_weeks (h);
		}
		
		////////////////////////////////////////
		////////////////////////////////////////
		
		/**
		 @brief set location
		
		 @param in_longitude longitude to use in calculations
			degrees, negative values are east
		 @param in_latitude latitude to use in calculations
			degrees, negative values are south
		 @param in_tz time zone
		 */
		void
		set_location (double in_latitude, double in_longitude, int in_tz)
		{
			latitude = in_latitude;
			longitude = in_longitude;
			tz = in_tz;
		}
		
		/**
		 @brief sunrise time
		
		 @return sunrise in minutes after midnight (00:00)
		 */
		int
		get_sunrise ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude, 
				&sunrise, &sunset);
			
			return sunrise + tz * 60;
		}
		
		/**
		 @brief sunset time
		
		 @return sunset in minutes after midnight (00:00)
		 */
		int
		get_sunset ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude, 
				&sunrise, &sunset);
			
			return sunset + tz * 60;
		}
		
		/**
		 @brief first light time
		
		 @return first light in minutes after midnight (00:00)
		 */
		int
		get_first_light ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time_deg (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude, 106.01,
				&sunrise, &sunset);
			
			return sunrise + tz * 60;
		}
		
		/**
		 @brief talit time
		
		 @return talit time in minutes after midnight (00:00)
		 */
		int
		get_talit ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time_deg (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude, 101.0,
				&sunrise, &sunset);
			
			return sunrise + tz * 60;
		}
		
		/**
		 @brief first stars time
		
		 @return first stars in minutes after midnight (00:00)
		 */
		int
		get_first_stars ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time_deg (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude, 96.0,
				&sunrise, &sunset);
			
			return sunset + tz * 60;
		}
		
		/**
		 @brief three stars time
		
		 @return three stars in minutes after midnight (00:00)
		 */
		int
		get_three_stars ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time_deg (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude, 98.5,
				&sunrise, &sunset);
			
			return sunset + tz * 60;
		}
		
		/**
		 @brief sun light hour time
		
		 @return sun light hour in minutes
		 */
		int
		get_sun_hour ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude,
				&sunrise, &sunset);
			
			return (sunset - sunrise) / 12;
		}
		
		/**
		 @brief midday hour time
		
		 @return midday hour in minutes
		 */
		int
		get_midday ()
		{
			int sunrise;
			int sunset;
			
			hdate_get_utc_sun_time (h->gd_day, h->gd_mon, h->gd_year, 
				latitude, longitude,
				&sunrise, &sunset);
			
			return (sunset + sunrise) / 2;
		}
		
		////////////////////////////////////////
		////////////////////////////////////////
		
		/**
		 @brief name of translator
		
		 @return a static string with name of translator, or NULL if none
		*/
		char *
		get_translator_string ()
		{
			return hdate_get_translator_string ();
		}
		
		/**
		 @brief set this hdate object to use diaspora holidays and dates
		*/
		void
		set_diaspora ()
		{
			diaspora = HDATE_DIASPORA_FLAG;
		}
		
		/**
		 @brief set this hdate object to use israel holidays and dates
		*/
		void
		set_israel ()
		{
			diaspora = HDATE_ISRAEL_FLAG;
		}
		
	private:
		
		int diaspora;
		double latitude;
		double longitude;
		int tz;
		hdate_struct *h;
		int type_of_string;
		int index;
		int short_form;
		int hebrew_form;
	
	};
}
 // name space

#endif
