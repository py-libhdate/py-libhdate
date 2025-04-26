*****
hdate
*****

.. image:: https://img.shields.io/pypi/v/hdate
    :alt: PyPI - Version
    :target: https://pypi.org/project/hdate/
.. image:: https://readthedocs.org/projects/py-libhdate/badge/?version=latest
    :alt: Documentation Status
    :target: https://py-libhdate.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fpy-libhdate%2Fpy-libhdate%2Fmain%2Fpyproject.toml
    :alt: Python Version from PEP 621 TOML
    :target: https://github.com/py-libhdate/py-libhdate/blob/main/pyproject.toml#L17
.. image:: https://img.shields.io/pypi/l/hdate
    :alt: PyPI - License
    :target: https://github.com/py-libhdate/py-libhdate/blob/main/LICENSE
.. image:: https://codecov.io/gh/py-libhdate/py-libhdate/graph/badge.svg?token=JGBmTslA1S 
    :alt: Code coverage status
    :target: https://codecov.io/gh/py-libhdate/py-libhdate

The ``hdate`` Python library's purpose is to provide information about the Hebrew date and times.

Originally ported from the C version of `libhdate <http://libhdate.sourceforge.net/>`_ by
`Royi Reshef <https://github.com/royi1000>`_, it is currently maintained by
`Tsvi Mostovicz <https://github.com/tsvi>`_ and is the backend library for
`Home Assistant's <https://home-assistant.io>`_ Jewish Calendar integration.

===========

Installation using pip:
#######################

.. code :: shell

    $ pip install hdate

===========

Examples:
#########

Provide the times of the day in Hebrew...

.. code :: python

    >>> import hdate
    >>> import datetime
    >>> c = hdate.Location("פתח תקוה", 32.08707, 34.88747, "Asia/Jerusalem", 54)
    >>> z = hdate.Zmanim(date=datetime.date(2016, 4, 18), location=c)
    >>> print(z)
    עלות השחר - 04:52:00
    זמן טלית ותפילין - 05:18:00
    הנץ החמה - 06:08:00
    סוף זמן ק"ש מג"א - 08:46:00
    סוף זמן ק"ש גר"א - 09:23:00
    סוף זמן תפילה מג"א - 10:04:00
    סוף זמן תפילה גר"א - 10:28:00
    חצות היום - 12:40:00
    מנחה גדולה - 13:10:30
    מנחה גדולה 30 דק - 13:10:00
    מנחה קטנה - 16:25:30
    פלג המנחה - 17:50:45
    שקיעה - 19:12:00
    מוצאי צום - 19:40:00
    מוצאי שבת - 19:50:00
    צאת הכוכבים (18 דק) - 19:31:30
    לילה לרבנו תם - 20:30:00
    חצות הלילה - 00:40:00

... and in English.

.. code :: python

    >>> from hdate.translator import set_language
    >>> set_language("en")
    >>> z = hdate.Zmanim(date=datetime.date(2016, 4, 18), location=c)
    >>> print(z)
    Alot HaShachar - 04:52:00
    Talit & Tefilin's time - 05:18:00
    Sunrise - 06:08:00
    Shema EOT MG"A - 08:46:00
    Shema EOT GR"A - 09:23:00
    Tefila EOT MG"A - 10:04:00
    Tefila EOT GR"A - 10:28:00
    Midday - 12:40:00
    Big Mincha - 13:10:30
    Big Mincha 30 min - 13:10:00
    Small Mincha - 16:25:30
    Plag Mincha - 17:50:45
    Sunset - 19:12:00
    End of fast - 19:40:00
    End of Shabbat - 19:50:00
    Tset Hakochavim (18 minutes) - 19:31:30
    Night by Rabbeinu Tam - 20:30:00
    Midnight - 00:40:00

===========

Provide the full Hebrew date ...

.. code :: python

    >>> set_language("he")
    >>> h = hdate.HDateInfo(datetime.date(2016, 4, 26))
    >>> print(h)
    יום שלישי י"ח בניסן ה' תשע"ו ג' לעומר חול המועד פסח

... and in English.

.. code :: python

    >>> set_language("en")
    >>> h = hdate.HDateInfo(datetime.date(2016, 4, 18))
    >>> print(h)
    Monday 10 Nisan 5776
