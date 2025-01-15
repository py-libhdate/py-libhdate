==========
Quickstart
==========

This document should walk you through everything you need to get started with ``hdate``.

-----------------------
Getting the Hebrew date
-----------------------

Suppose we want to get today's Hebrew date.

.. code:: python

    >>> from datetime import date
    >>> from hdate import HebrewDate

    >>> today = date.today()
    >>> heb_date = HebrewDate.from_gdate(today)
    >>> print(heb_date)
    15 Tevet 5785

Let's see how much time is left until Pesach 😧

.. code:: python

    >>> from hdate import Months

    >>> pesach = HebrewDate(0, Months.NISAN, 15)
    >>> time_to_pesach = pesach - heb_date  # Returns a timedelta object
  
    >>> print(time_to_pesach.days)
    88

Better start cleaning 😉

The ``HebrewDate`` object is similar to Python's built-in ``datetime.date`` object.
It's responsibility is to represent a Hebrew date and allow date comparisons and calculations.
To get more information about a specific date, have a look at the ``HDate`` object.

.. note::

  By setting the ``year`` value to 0, the ``HebrewDate`` is considered to be relative.
  All calculations and comparisons are done on the assumption that both objects use the
  same year value.

  See more on that later for special cases of leap years and possible non-existing days.


--------------------------
Getting the Gregorian date
--------------------------

We want to know when is *Rosh Hashana* for the upcoming year (5786).

.. code:: python

    >>> rosh_hashana = HebrewDate(5786, Months.TISHREI, 1)
    >>> gdate = rosh_hashana.to_gdate()
    >>> print(gdate)
    2025-09-23

We can also know what the day of the week is:

.. code:: python

    >>> day_of_week = rosh_hashana.dow()
    >>> print(day_of_week)
    Tuesday


------------------------------------------------
Getting the string value in a different language
------------------------------------------------

All classes and enums in ``hdate`` can have their language changed by calling the
``set_language()`` method.
Currently supported are Hebrew, English and French.

.. code:: python

    >>> day_of_week.set_language("hebrew")
    >>> print(str(day_of_week))
    יום שלישי
    >>> day_of_week.set_language("french")
    >>> print(str(day_of_week))
    Mardi

-----------------------------------------
Zmanim - getting the times of a given day
-----------------------------------------

To get the times of a given day, we'll need first to define a location.
The location requires a name, latitude, longitude, timezone and elevation.

.. code:: python

    >>> from hdate import Location

    >>> location = Location("Home", 32.09, 34.89, "Asia/Jerusalem", 54)

Now we can go ahead and ask ``hdate`` for the **Halachic times** for a given date.

.. code:: python

    >>> from hdate import Zmanim

    >>> zmanim = Zmanim(date.today(), location)
    >>> zmanim.alot_hashachar.local
    datetime.datetime(2025, 1, 15, 5, 25, tzinfo=zoneinfo.ZoneInfo(key='Asia/Jerusalem'))

To get a list of the supported zmanim, you'll want to inspect the keys returned by the
``zmanim`` property.

.. code:: python

    >>> zmanim.zmanim.keys()
    dict_keys(['alot_hashachar', 'talit_tefilins_time', 'sunrise', 'shema_eot_mga', 
    'shema_eot_gra', 'tefila_eot_mga', 'tefila_eot_gra', 'midday', 'big_mincha', 
    'big_mincha_min', 'small_mincha', 'plag_mincha', 'sunset', 'first_stars', 
    'three_stars', 'stars_out', 'night_by_rabbeinu_tam', 'midnight'])

You can also get a nice printout by calling ``str`` on the ``Zmanim`` object.

.. warning::

    Although we try as much as possible to be correct with our code trying to calculate
    the **Halachic times**, we do not take ANY responsibility whatsoever for the reliance
    on these calculations.
    When in doubt, please contact your local Halachic authority.

--------------------
The ``HDate`` object
--------------------

If you want more information on a specific date like **Parshat Hashavua**, Holidays, the **Daf Yomi**, or the current **Omer** count, you'll want to initialize a ``HDate`` object.

The ``HDate`` object, accepts a date (either Gregorian or Hebrew), a boolean that specifies whether the information should be calculated according to diaspora or not, and language (defaults to Hebrew).

.. code:: python

    >>> from hdate import HDate
    >>> today = HDate(today, diaspora=True, language="english")
    >>> today.parasha
    Shemot
    >>> today.is_holiday
    False

