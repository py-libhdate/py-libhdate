***********
py-libhdate
***********

Jewish/Hebrew date and Zmanim in native python 2.7/3.x

Originally ported from libhdate, see http://libhdate.sourceforge.net/ for more details (including license)

===========

Installation using pip:
#######################

.. code :: shell

    $ pip install hdate

===========

Examples:
#########

base code to provide times of the day in hebrew:

.. code :: python

    >>> import hdate
    >>> import datetime
    >>> c = hdate.Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
    >>> z = hdate.Zmanim(date=datetime.date(2016, 4, 18), location=c, hebrew=True)
    >>> print(z)

::

    עלות השחר - 04:52:00
    זמן טלית ותפילין - 05:18:00
    הנץ החמה - 06:08:00
    סוף זמן ק"ש מג"א - 08:46:00
    סוף זמן ק"ש גר"א - 09:23:00
    סוף זמן תפילה מג"א - 10:04:00
    סוף זמן תפילה גר"א - 10:28:00
    חצות היום - 12:40:00
    מנחה גדולה - 13:10:30
    מנחה קטנה - 16:25:30
    פלג המנחה - 17:50:45
    שקיעה - 19:12:00
    צאת הכוכבים - 19:38:00
    חצות הלילה - 00:40:00

and in english:

.. code :: python

    >>> z = hdate.Zmanim(date=datetime.date(2016, 4, 18), location=c, hebrew=False)
    >>> print(z)

::

    Alot HaShachar - 04:52:00
    Talit & Tefilin's time - 05:18:00
    Sunrise - 06:08:00
    Shema EOT MG"A - 08:46:00
    Shema EOT GR"A - 09:23:00
    Tefila EOT MG"A - 10:04:40
    Tefila EOT GR"A - 10:28:00
    Midday - 12:40:00
    Big Mincha - 13:10:30
    Small Mincha - 16:25:30
    Plag Mincha - 17:50:45
    Sunset - 19:12:00
    First stars - 19:38:00
    Midnight - 00:40:00

===========

to provide the full hebrew date:

.. code :: python

    >>> h = hdate.HDate(datetime.date(2016, 4, 26), hebrew=True)
    >>> print(h)

::

    יום שלישי י"ח בניסן התשע"ו ג' בעומר חול המועד פסח

and in english:

.. code :: python

    >>> h = hdate.HDate(datetime.date(2016, 4, 18), hebrew=False)
    >>> print(h)

::

    Monday 10 Nisan