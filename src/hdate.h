/*  libhdate - Hebrew calendar library: http://libhdate.sourceforge.net
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

/** @file hdate.h
    @brief libhdate C language header.
    
    libhdate - Hebrew calendar library, the C language header file.
*/

#ifndef __HDATE_H__
#define __HDATE_H__

#ifdef __cplusplus
extern "C"
{
#endif

/** @def HDATE_DIASPORA_FLAG
  @brief use diaspora dates and holydays flag
*/
#define HDATE_DIASPORA_FLAG -1
	
/** @def HDATE_ISRAEL_FLAG
  @brief use israel dates and holydays flag
*/
#define HDATE_ISRAEL_FLAG 0
	
/** @def HDATE_SHORT_FLAG
  @brief use short strings flag
*/
#define HDATE_SHORT_FLAG -1
	
/** @def HDATE_LONG_FLAG
  @brief use long strings flag
*/
#define HDATE_LONG_FLAG 0

/** @def HEBREW_NUMBER_BUFFER_SIZE
  @brief for hdate_get_int_string_ and hdate_get_int_wstring
  @note
  How large should the buffer be? Hebrew year 10,999 would
  be י'תתקצ"ט, eight characters, each two bytes, plus an
  end-of-string delimiter, equals 17. This could effectively
  yield a range extending to Hebrew year 11,899, י"א תתצ"ט,
  due to the extra ק needed for the '900' century. However,
  for readability, I would want a an extra space at that
  point between the millenium and the century...
*/
#define HEBREW_NUMBER_BUFFER_SIZE 17
#define HEBREW_WNUMBER_BUFFER_SIZE 9


/** @struct hdate_struct
  @brief libhdate Hebrew date struct
*/
typedef struct
{
	/** The number of day in the hebrew month (1..31). */
	int hd_day;
	/** The number of the hebrew month 1..14 (1 - tishre, 13 - adar 1, 14 - adar 2). */
	int hd_mon;
	/** The number of the hebrew year. */
	int hd_year;
	/** The number of the day in the month. (1..31) */
	int gd_day;
	/** The number of the month 1..12 (1 - jan). */
	int gd_mon;
	/** The number of the year. */
	int gd_year;
	/** The day of the week 1..7 (1 - sunday). */
	int hd_dw;
	/** The length of the year in days. */
	int hd_size_of_year;
	/** The week day of Hebrew new year. */
	int hd_new_year_dw;
	/** The number type of year. */
	int hd_year_type;
	/** The Julian day number */
	int hd_jd;
	/** The number of days passed since 1 tishrey */
	int hd_days;
	/** The number of weeks passed since 1 tishrey */
	int hd_weeks;
} hdate_struct;

/*************************************************************/
/*************************************************************/

/**
 @brief compute date structure from the Gregorian date

 @param h pointer this hdate struct.
 @param d Day of month 1..31
 @param m Month 1..12
	if m or d is 0 return current date.
 @param y Year in 4 digits e.g. 2001
 @return pointer to this hdate struct
 */
hdate_struct *
hdate_set_gdate (hdate_struct *h, int d, int m, int y);

/**
 @brief compute date structure from the Hebrew date

 @param h pointer this hdate struct.
 @param d Day of month 1..31
 @param m Month 1..14 ,(13 - Adar 1, 14 - Adar 2)
 	if m or d is 0 return current date.
 @param y Year in 4 digits e.g. 5731
 @return pointer to this hdate struct
 */
hdate_struct *
hdate_set_hdate (hdate_struct *h, int d, int m, int y);

/**
 @brief compute date structure from the Julian day

 @param h pointer this hdate struct.
 @param jd the julian day number.
 @return pointer to this hdate struct
 */
hdate_struct *
hdate_set_jd (hdate_struct *h, int jd);

/*************************************************************/
/*************************************************************/

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
hdate_get_format_date (hdate_struct const * h, int diaspora, int s);

/**
 @brief get the number of hebrew parasha.

 @param h pointer this hdate struct.
 @param diaspora if true give diaspora readings
 @return the number of parasha 1. Bereshit etc..
   (55 through 61 are joined strings e.g. Vayakhel Pekudei)
*/
int
hdate_get_parasha (hdate_struct const * h, int diaspora);

/**
 @brief get the number of hebrew holiday.

 @param h pointer this hdate struct.
 @param diaspora if true give diaspora holidays
 @return the number of holiday.
*/
int
hdate_get_holyday (hdate_struct const * h, int diaspora);

/*************************************************************/
/*************************************************************/

/**
 @brief convert an integer to hebrew string. 
 
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
hdate_get_int_string (int n);


/**
 @brief Return a static string, with name of week day.

 @param day_of_week The number of the day 1..7 (1 - sun).
 @param short_form A short flag (true - sun; false - sunday).
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_day_string (int day, int s);

/**
 @brief Return a static string, with name of month.

 @param month The number of the month 1..12 (1 - jan).
 @param short_form A short flag.
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_month_string (int month, int s);

/**
 @brief Return a static string, with name of hebrew month.

 @param month The number of the month 1..14 (1 - tishre, 13 - adar 1, 14 - adar 2).
 @param short_form A short flag.
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_hebrew_month_string (int month, int s);

/**
 @brief Name of hebrew holiday.

 @param holiday The holiday number.
 @param short_text A short flag. 0=true, !0=false
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_holyday_string (int holyday, int s);

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
hdate_get_parasha_string (int parasha, int s);

/**
 @brief Return a static string, with the day in the omer

 @param omer day The day in the omer.
 @return a pointer to a string with the day in the omer. The caller
         must free() the pointer after use.
 @warning DEPRECATION: This function is now just a wrapper for
          hdate_string, and is subject to deprecation.
 @attention The prior version of this function returned a pointer to a
          static string buffer. The current version returns a pointer to
          a malloc()ed buffer and needs to be free()d after use.
		  [deprecation date 2011-12-28]
*/
char *
hdate_get_omer_string (int omer_day);

/*************************************************************/
/*************************************************************/

/**
 @brief Return the day in the omer of the given date

 @param h The hdate_struct of the date to use.
 @return The day in the omer, starting from 1 (or 0 if not in sfirat ha omer)
*/
int
hdate_get_omer_day(hdate_struct const * h);

/**
 @brief Return number of hebrew holyday type.

  Holiday types:
    0 - Regular day
    1 - Yom tov (plus yom kippor)
    2 - Erev yom kippur
    3 - Hol hamoed
    4 - Hanuka and purim
    5 - Tzomot
    6 - Independance day and Yom yerushalaim
    7 - Lag baomer ,Tu beav, Tu beshvat
    8 - Tzahal and Holocaust memorial days
    9 - National days
    
 @param holyday the holyday number
 @return the number of holyday type.
*/
int
hdate_get_holyday_type (int holyday);

/**
 @brief size of hebrew year in days.
 
 @param hebrew_year the hebrew year.
 @return size of Hebrew year
*/
int
hdate_get_size_of_hebrew_year (int hebrew_year);

/*************************************************************/
/*************************************************************/

/**
 @brief Days since Tishrey 3744
 
 @author Amos Shapir 1984 (rev. 1985, 1992) Yaacov Zamir 2003-2005 
 
 @param hebrew_year The Hebrew year
 @return Number of days since 3,1,3744
*/
int
hdate_days_from_3744 (int hebrew_year);

/**
 @brief Return Hebrew year type based on size and first week day of year.
 
 @param size_of_year Length of year in days
 @param new_year_dw First week day of year
 @return the number for year type (1..14)
*/
int
hdate_get_year_type (int size_of_year, int new_year_dw);

/**
 @brief Compute Julian day from Gregorian date

 @author Yaacov Zamir (algorithm from Henry F. Fliegel and Thomas C. Van Flandern ,1968)

 @param day Day of month 1..31
 @param month Month 1..12
 @param year Year in 4 digits e.g. 2001
 @return the julian day number
 */
int
hdate_gdate_to_jd (int day, int month, int year);

/**
 @brief Compute Julian day from Hebrew day, month and year
 
 @author Amos Shapir 1984 (rev. 1985, 1992) Yaacov Zamir 2003-2005

 @param day Day of month 1..31
 @param month Month 1..14 (13 - Adar 1, 14 - Adar 2)
 @param year Hebrew year in 4 digits e.g. 5753
 @param jd_tishrey1 return the julian number of 1 Tishrey this year
 @param jd_tishrey1_next_year return the julian number of 1 Tishrey next year
 @return the julian day number
 */
int
hdate_hdate_to_jd (int day, int month, int year, int *jd_tishrey1, int *jd_tishrey1_next_year);

/**
 @brief Converting from the Julian day to the Gregorian date
 
 @author Yaacov Zamir (Algorithm, Henry F. Fliegel and Thomas C. Van Flandern ,1968)

 @param jd Julian day
 @param day return Day of month 1..31
 @param month return Month 1..12
 @param year return Year in 4 digits e.g. 2001
 */
void
hdate_jd_to_gdate (int jd, int *day, int *month, int *year);

/**
 @brief Converting from the Julian day to the Hebrew day
 
 @author Yaacov Zamir 2005

 @param jd Julian day
 @param day return Day of month 1..31
 @param month return Month 1..14 (13 - Adar 1, 14 - Adar 2)
 @param year return Year in 4 digits e.g. 2001
 @param jd_tishrey1 return the julian number of 1 Tishrey this year
 @param jd_tishrey1_next_year return the julian number of 1 Tishrey next year
 */
void
hdate_jd_to_hdate (int jd, int *day, int *month, int *year, int *jd_tishrey1, int *jd_tishrey1_next_year);

/*************************************************************/
/*************************************************************/

/**
 @brief days from 1 january
  
 @param day this day of month
 @param month this month
 @param year this year
 @return the days from 1 jan
*/
int
hdate_get_day_of_year (int day, int month, int year);

/**
 @brief utc sun times for altitude at a gregorian date

 Returns the sunset and sunrise times in minutes from 00:00 (utc time)
 if sun altitude in sunrise is deg degries.
 This function only works for altitudes sun realy is.
 If the sun never get to this altitude, the returned sunset and sunrise values 
 will be negative. This can happen in low altitude when latitude is 
 nearing the pols in winter times, the sun never goes very high in 
 the sky there.

 @param day this day of month
 @param month this month
 @param year this year
 @param longitude longitude to use in calculations
 @param latitude latitude to use in calculations
 @param deg degrees of sun's altitude (0 -  Zenith .. 90 - Horizon)
 @param sunrise return the utc sunrise in minutes
 @param sunset return the utc sunset in minutes
*/
void
hdate_get_utc_sun_time_deg (int day, int month, int year, 
	double latitude, double longitude, double deg, int *sunrise, int *sunset);

/**
 @brief utc sunrise/set time for a gregorian date
  
 @param day this day of month
 @param month this month
 @param year this year
 @param longitude longitude to use in calculations
	degrees, negative values are east
 @param latitude latitude to use in calculations
	degrees, negative values are south
 @param sunrise return the utc sunrise in minutes after midnight (00:00)
 @param sunset return the utc sunset in minutes after midnight (00:00)
*/
void
hdate_get_utc_sun_time (int day, int month, int year, 
	double latitude, double longitude, int *sunrise, int *sunset);

/**
 @brief utc sunrise/set time for a gregorian date
  
 @param day this day of month
 @param month this month
 @param year this year
 @param longitude longitude to use in calculations
 @param latitude latitude to use in calculations
 @param sun_hour return the length of shaa zaminit in minutes
 @param first_light return the utc alut ha-shachar in minutes
 @param talit return the utc tphilin and talit in minutes
 @param sunrise return the utc sunrise in minutes
 @param midday return the utc midday in minutes
 @param sunset return the utc sunset in minutes
 @param first_stars return the utc tzeit hacochavim in minutes
 @param three_stars return the utc shlosha cochavim in minutes
*/
void
hdate_get_utc_sun_time_full (int day, int month, int year, double latitude, double longitude, 
	int *sun_hour, int *first_light, int *talit, int *sunrise,
	int *midday, int *sunset, int *first_stars, int *three_stars);

/*************************************************************/
/*************************************************************/

/**
 @brief get the Gregorian day of the month

 @param h pointer this hdate struct.
 @return the Gregorian day of the month, 1..31.
 */
int
hdate_get_gday (hdate_struct const * h);

/**
 @brief get the Gregorian month

 @param h pointer this hdate struct.
 @return the Gregorian month, jan = 1.
 */
int
hdate_get_gmonth (hdate_struct const * h);

/**
 @brief get the Gregorian year

 @param h pointer this hdate struct.
 @return the Gregorian year.
 */
int
hdate_get_gyear (hdate_struct const * h);

/**
 @brief get the Hebrew day of the month

 @param h pointer this hdate struct.
 @return the Hebrew day of the month, 1..30.
 */
int
hdate_get_hday (hdate_struct const * h);

/**
 @brief get the Hebrew month

 @param h pointer this hdate struct.
 @return the Hebrew month, Tishery = 1 .. Adar I =13, Adar II = 14.
 */
int
hdate_get_hmonth (hdate_struct const * h);

/**
 @brief get the Hebrew year

 @param h pointer this hdate struct.
 @return the Hebrew year.
 */
int
hdate_get_hyear (hdate_struct const * h);

/**
 @brief get the day of the week

 @param h pointer this hdate struct.
 @return the the day of the week.
 */
int
hdate_get_day_of_the_week (hdate_struct const * h);

/**
 @brief get the size of the hebrew year

 @param h pointer this hdate struct.
 @return the the size of the hebrew year.
 */
int
hdate_get_size_of_year (hdate_struct const * h);

/**
 @brief get the new year day of the week

 @param h pointer this hdate struct.
 @return the the new year day of the week.
 */
int
hdate_get_new_year_day_of_the_week (hdate_struct const * h);

/**
 @brief get the Julian day number

 @param h pointer this hdate struct.
 @return the Julian day number.
 */
int
hdate_get_julian (hdate_struct const * h);

/**
 @brief get the number of days passed since 1 tishrey

 @param h pointer this hdate struct.
 @return the number of days passed since 1 tishrey.
 */
int
hdate_get_days (hdate_struct const * h);

/**
 @brief get the number of weeks passed since 1 tishrey

 @param h pointer this hdate struct.
 @return the number of weeks passed since 1 tishrey.
 */
int
hdate_get_weeks (hdate_struct const * h);

/*************************************************************/
/*************************************************************/

/**
 @brief creat a new hdate struct object, must be deleted using delete_hdate.

 @return a new hdate object
 */
hdate_struct *
new_hdate ();

/**
 @brief delete an hdate struct object.

 @param h pointer this hdate struct.
 */
hdate_struct *
delete_hdate (hdate_struct *h);

/*************************************************************/
/*************************************************************/

/**
 @brief Return a static string, with the package name and version

 @return a static string, with the package name and version
*/
char *
hdate_get_version_string ();

/**
 @brief name of translator

 @return a static string with name of translator, or NULL if none.
*/
char *
hdate_get_translator_string ();

/**
 @brief helper function to find hebrew locale
 
 @return 0 - latin locale, -1 - hebrew locale
*/
int
hdate_is_hebrew_locale();

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
char* hdate_string( int type_of_string, int index, int short_form, int hebrew_form);

/** @def HDATE_STRING_INT
  @brief for function hdate_string: identifies string type: integer
*/
#define HDATE_STRING_INT     0

/** @def HDATE_STRING_DOW
  @brief for function hdate_string: identifies string type: day of week 
*/
#define HDATE_STRING_DOW       1

/** @def HDATE_STRING_PARASHA
  @brief for function hdate_string: identifies string type: parasha
*/
#define HDATE_STRING_PARASHA   2

/** @def HDATE_STRING_HMONTH
  @brief for function hdate_string: identifies string type: hebrew_month
*/
#define HDATE_STRING_HMONTH    3

/** @def HDATE_STRING_GMONTH
  @brief for function hdate_string: identifies string type: gregorian_month
*/
#define HDATE_STRING_GMONTH    4

/** @def HDATE_STRING_HOLIDAY
  @brief for function hdate_string: identifies string type: holiday
*/
#define HDATE_STRING_HOLIDAY   5

/** @def HDATE_STRING_HOLIDAY
  @brief for function hdate_string: identifies string type: holiday
*/
#define HDATE_STRING_OMER      6

/** @def HDATE_STRING_SHORT
  @brief for function hdate_string: use short form, if one exists
*/
#define HDATE_STRING_SHORT   1

/** @def HDATE_STRING_LONG
  @brief for function hdate_string: use long form
*/
#define HDATE_STRING_LONG    0

/** @def HDATE_STRING_HEBREW
  @brief for function hdate_string: use embedded hebrew string
*/
#define HDATE_STRING_HEBREW  1

/** @def HDATE_STRING_LOCAL
  @brief for function hdate_string: use local locale string
*/
#define HDATE_STRING_LOCAL   0



#ifdef __cplusplus
}
#endif

#endif
