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