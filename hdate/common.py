"""Small helper classes."""

from datetime import tzinfo

import pytz

from hdate.htables import Months


class BaseClass:
    """Implement basic functionality for all classes."""

    def __eq__(self, other):
        """Override equality operator."""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Override inequality operator."""
        return not self.__eq__(other)


class HebrewDate(BaseClass):  # pylint: disable=too-few-public-methods
    """Define a Hebrew date object."""

    def __init__(self, year, month, day):
        """Initialize the Hebrew date object."""
        self.year = year
        self.month = month if isinstance(month, Months) else Months(month)
        self.day = day


class Location(BaseClass):
    """Define a geolocation for Zmanim calculations."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name="Jerusalem",
        latitude=31.778,
        longitude=35.235,
        timezone="Asia/Jerusalem",
        altitude=754,
        diaspora=False,
    ):
        """Initialitze the location object."""
        self._timezone = None
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.altitude = altitude
        self.diaspora = diaspora

    def __repr__(self):
        """Return a representation of Location for programmatic use."""
        return (
            f"Location(name='{self.name}', latitude={self.latitude}, "
            f"longitude={self.longitude}, timezone='{self.timezone}', "
            f"altitude={self.altitude}, diaspora={self.diaspora})"
        )

    @property
    def timezone(self):
        """Return the timezone."""
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        """Set the timezone."""
        self._timezone = value if isinstance(value, tzinfo) else pytz.timezone(value)
