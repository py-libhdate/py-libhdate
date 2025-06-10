==========
User Guide
==========

******************************
The ``HolidayDatabase`` object
******************************

The ``HolidayDatabase`` is a database that holds all the needed information about
the Jewish holidays in a year.

Holidays include religious holidays, like *Pesach*, *Shavuot*, and *Sukkot*. Special
days, like *Rosh Chodesh* and *Chol Hamo'ed*, as well as secular official Israeli
holidays, like *Yom Ha'atsmaut*, *Yom Yerushalayim* and more.

A given date might have multiple holidays, like *Rosh Chodesh* and *Chanuka* or
*Shmini Atseret* and *Simchat Torah* in Israel.

Getting the holiday for a given date
------------------------------------

The ``lookup`` method is used to lookup the holiday for a given date. The result is a 
list of ``Holiday`` objects. If the given date is not a holiday the list will be empty.

.. code:: python
    
    >>> from hdate.holidays import HolidayDatabase
    >>> from hdate import HebrewDate, Months
    >>> db = HolidayDatabase(diaspora=False)
    >>> holidays = db.lookup(HebrewDate(5785, Months.ADAR, 14))
    >>> print(holidays[0])
    Purim
    >>> db.lookup(HebrewDate(5785, Months.TEVET, 26))
    []

An upcoming holiday
-------------------

We can also lookup the upcoming holiday, this will return a ``HebrewDate``, which in
turn can be translated to the Gregorian calendar, using the ``to_gdate()`` method.

When looking up an upcoming holiday, the request can be filtered according to 
``HolidayTypes``.

.. code:: python

    >>> today = HebrewDate(5785, Months.TEVET, 26)
    >>> rosh_chodesh = db.lookup_next_holiday(today)
    >>> print(rosh_chodesh)
    1 Sh'vat 5785
    >>> rosh_chodesh.to_gdate()
    datetime.date(2025, 1, 30)

    >>> from hdate.holidays import HolidayTypes

    >>> no_rosh_chodesh = [t for t in HolidayTypes if t != HolidayTypes.ROSH_CHODESH]
    >>> db.lookup_next_holiday(today, no_rosh_chodesh)
    HebrewDate(year=5785, month=<Months.SHVAT: 5>, day=15)
    >>> db.lookup_next_holiday(today, HolidayTypes.YOM_TOV)
    HebrewDate(year=5785, month=<Months.NISAN: 9>, day=15)

Getting the dates for all the holidays in a year
------------------------------------------------

To get all the holidays in a given year (incl. their dates), we can use the
``lookup_holidays_for_year`` method. This method accepts a ``HebrewDate`` to get the
year for which to lookup the holidays.

The result is a dictionary where for each given ``HebrewDate``, a list of ``Holiday``
objects is provided. Here to, we can filter based on ``HolidayTypes``.

.. code:: python
    
    >>> holidays = db.lookup_holidays_for_year(today)
    >>> for _date, _holidays in holidays.items():
    ...     print(f"{_date}: {', '.join(str(h) for h in _holidays)}")
    1 Tishrei 5785: Rosh Hashana I
    2 Tishrei 5785: Rosh Hashana II
    4 Tishrei 5785: Tzom Gedaliah
    9 Tishrei 5785: Erev Yom Kippur
    10 Tishrei 5785: Yom Kippur
    14 Tishrei 5785: Erev Sukkot
    15 Tishrei 5785: Sukkot
    16 Tishrei 5785: Hol hamoed Sukkot
    17 Tishrei 5785: Hol hamoed Sukkot
    18 Tishrei 5785: Hol hamoed Sukkot
    19 Tishrei 5785: Hol hamoed Sukkot
    20 Tishrei 5785: Hol hamoed Sukkot
    21 Tishrei 5785: Hoshana Raba
    22 Tishrei 5785: Shmini Atzeret, Simchat Torah
    30 Tishrei 5785: Rosh Chodesh
    1 Marcheshvan 5785: Rosh Chodesh
    11 Marcheshvan 5785: Yitzhak Rabin memorial day
    30 Marcheshvan 5785: Rosh Chodesh
    1 Kislev 5785: Rosh Chodesh
    25 Kislev 5785: Chanukah
    26 Kislev 5785: Chanukah
    27 Kislev 5785: Chanukah
    28 Kislev 5785: Chanukah
    29 Kislev 5785: Chanukah
    30 Kislev 5785: Chanukah, Rosh Chodesh
    1 Tevet 5785: Chanukah, Rosh Chodesh
    2 Tevet 5785: Chanukah
    10 Tevet 5785: Asara B'Tevet
    1 Sh'vat 5785: Rosh Chodesh
    15 Sh'vat 5785: Tu B'Shvat
    30 Sh'vat 5785: Rosh Chodesh, Family Day
    1 Adar 5785: Rosh Chodesh
    7 Adar 5785: Memorial day for fallen whose place of burial is unknown
    13 Adar 5785: Ta'anit Esther
    14 Adar 5785: Purim
    15 Adar 5785: Shushan Purim
    1 Nisan 5785: Rosh Chodesh
    14 Nisan 5785: Erev Pesach
    15 Nisan 5785: Pesach
    16 Nisan 5785: Hol hamoed Pesach
    17 Nisan 5785: Hol hamoed Pesach
    18 Nisan 5785: Hol hamoed Pesach
    19 Nisan 5785: Hol hamoed Pesach
    20 Nisan 5785: Hol hamoed Pesach
    21 Nisan 5785: Pesach VII
    26 Nisan 5785: Yom HaShoah
    30 Nisan 5785: Rosh Chodesh
    1 Iyyar 5785: Rosh Chodesh
    2 Iyyar 5785: Yom HaZikaron
    3 Iyyar 5785: Yom HaAtzma'ut
    18 Iyyar 5785: Lag B'Omer
    28 Iyyar 5785: Yom Yerushalayim
    1 Sivan 5785: Rosh Chodesh
    5 Sivan 5785: Erev Shavuot
    6 Sivan 5785: Shavuot
    30 Sivan 5785: Rosh Chodesh
    1 Tammuz 5785: Rosh Chodesh
    17 Tammuz 5785: Tzom Tammuz
    29 Tammuz 5785: Zeev Zhabotinsky day
    1 Av 5785: Rosh Chodesh
    9 Av 5785: Tish'a B'Av
    15 Av 5785: Tu B'Av
    30 Av 5785: Rosh Chodesh
    1 Elul 5785: Rosh Chodesh
    29 Elul 5785: Erev Rosh Hashana
