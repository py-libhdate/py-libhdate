py-libhdate
===========

Jewish/Hebrew date and Zmanim in native python 2.7/3.x

Originally ported from libhdate, see http://libhdate.sourceforge.net/ for more details (including license)

.. code :: python

    >>> import hdate
    >>> import datetime
    >>> from collections import namedtuple
    >>> City = namedtuple("City", ["name", "latitude", "longitude", "timezone", "elevation"])
    >>> c = City("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
    >>> z = hdate.Zmanim(date=datetime.date(2016, 4, 18),
                         latitude=c.latitude, longitude=c.longitude,
                         timezone=c.timezone)
    >>> print z

::

    עלות השחר - 04:53
    זמן טלית ותפילין - 05:19
    הנץ החמה - 06:09
    סוף זמן ק"ש מג"א - 08:46
    סוף זמן ק"ש הגר"א - 09:24
    סוף זמן תפילה מג"א - 10:03
    סוף זמן תפילה גר"א - 10:29
    חצות היום - 12:39
    מנחה גדולה - 13:11
    מנחה קטנה - 16:26
    פלג מנחה - 17:48
    שקיעה - 19:10
    צאת הככבים - 19:35
    חצות הלילה - 00:39

.. code :: python

    z = hdate.Zmanim(date=datetime.date(2016, 4, 18),
                     latitude=c.latitude, longitude=c.longitude,
                     timezone=c.timezone, hebrew=False)

    >>> print z

::

    Alot HaShachar - 04:53
    Talit & Tefilin's time - 05:19
    Sunrise - 06:09
    Shema EOT MG"A - 08:46
    Shema EOT GR"A - 09:24
    Tefila EOT MG"A - 10:03
    Tefila EOT GR"A - 10:29
    Midday - 12:39
    Big Mincha - 13:11
    Small Mincha - 16:26
    Plag Mincha - 17:48
    Sunset - 19:10
    First stars - 19:35
    Midnight - 00:39

.. code :: python

    >>> h=hdate.HDate(datetime.date(2016, 4, 18), hebrew=False)
    >>> print h

::

    Monday 10 Nisan 5776

.. code :: python

    >>> h=hdate.HDate(datetime.date(2016, 4, 26), hebrew=True)
    >>> print h

::

    יום שלישי י"ח בניסן התשע"ו ג' בעומר חול המועד פסח
