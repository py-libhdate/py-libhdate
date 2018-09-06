"""Helper functions for both Zmanim and HDate objects."""

import datetime


def set_date(date):
    """
    Check that the given date is valid.

    If no date is given set the date to today
    """
    if date is None:
        date = datetime.date.today()
    elif not isinstance(date, datetime.date):
        raise TypeError
    return date
