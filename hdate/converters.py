"""Methods for going back and forth between Gregorian date and Julian day."""

import datetime as dt

JDN_OFFSET = 1_721_425


def gdate_to_jdn(date_obj: dt.date | dt.datetime) -> int:
    """Compute Julian Day Number from Gregorian date using stdlib."""
    return date_obj.toordinal() + JDN_OFFSET


def jdn_to_gdate(jdn: int) -> dt.date:
    """Convert JDN to Gregorian date using stdlib."""
    return dt.date.fromordinal(jdn - JDN_OFFSET)
