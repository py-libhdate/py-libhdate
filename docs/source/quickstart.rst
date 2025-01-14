==========
Quickstart
==========

This document should talk you through everything you need to get started with ``hdate``.

-----------------------
Getting the Hebrew date
-----------------------

Suppose we want to get today's Hebrew date.

.. code:: python

    from datetime import date
    from hdate import HebrewDate

    today = date.today()
    heb_date = HebrewDate.from_gdate(today)
    print(heb_date)

Let's see how much time is left until Pesach 😧

.. code:: python

    from hdate import Months

    pesach = HebrewDate(0, Months.NISAN, 15)
    time_to_pesach = pesach - heb_date  # Returns a timedelta object
  
    print(time_to_pesach.days)

Better start cleaning 😉

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

    rosh_hashana = HebrewDate(5786, Months.TISHREI, 1)
    gdate = rosh_hashana.to_gdate()

We can also know what the day of the week is:

.. code:: python

    day_of_week = rosh_hashana.dow()


------------------------------------------------
Getting the string value in a different language
------------------------------------------------

All classes and enums in ``hdate`` can have their language changed by calling the
``set_language()`` method.
Currently supported are Hebrew, English and French.

.. code:: python

    >>> day_of_week.set_language("hebrew")
    >>> print(str(day_of_week))
    ... יום שלישי
    >>> day_of_week.set_language("french")
    >>> print(str(day_of_week))
    ... Mardi

-----------------------------------------
Zmanim - getting the times of a given day
-----------------------------------------

To get the times of a given day, we'll need first to define a location.
The location requires a name, latitude, longitude, timezone and elevation.

.. code:: python

    from hdate import Location

    location = Location("Home", 32.09, 34.89, "Asia/Jerusalem", 54)

Now we can go ahead and ask ``hdate`` for the **Halachic times** for a given date.

.. code:: python

    from hdate import Zmanim

    zmanim = Zmanim(date.today(), location)