libhdate_la_CFLAGS = $(libhdate_CFLAGS)

lib_LTLIBRARIES = libhdate.la

libhdate_la_SOURCES = \
	deprecated.c\
	hdate_strings.c\
	hdate_julian.c\
	hdate_holyday.c\
	hdate_parasha.c\
	hdate_sun_time.c\
	hdate.h\
	support.h

libhdate_la_LDFLAGS = $(libhdate_LDFLAGS) -version-info $(VERSION_INFO)

libhdate_la_LIBADD = 

include_HEADERS = hdate.h hdatepp.h

