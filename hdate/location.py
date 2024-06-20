"""Location data for HDate - used by Zmanim."""

from dataclasses import dataclass
from datetime import tzinfo

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


@dataclass
class Location:
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
        self._timezone = value if isinstance(value, tzinfo) else ZoneInfo(value)
