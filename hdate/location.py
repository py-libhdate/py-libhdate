"""Location data for HDate - used by Zmanim."""

from dataclasses import dataclass
from datetime import tzinfo
from typing import Union

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
        name: str = "Jerusalem",
        latitude: float = 31.778,
        longitude: float = 35.235,
        timezone: Union[ZoneInfo, str] = "Asia/Jerusalem",
        altitude: int = 754,
        diaspora: bool = False,
    ) -> None:
        """Initialitze the location object."""
        self._timezone = None
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.altitude = altitude
        self.diaspora = diaspora

    def __repr__(self) -> str:
        """Return a representation of Location for programmatic use."""
        return (
            f"Location(name='{self.name}', latitude={self.latitude}, "
            f"longitude={self.longitude}, timezone='{self.timezone}', "
            f"altitude={self.altitude}, diaspora={self.diaspora})"
        )

    @property
    def timezone(self) -> ZoneInfo:
        """Return the timezone."""
        return self._timezone

    @timezone.setter
    def timezone(self, value: Union[str, ZoneInfo]) -> None:
        """Set the timezone."""
        self._timezone = value if isinstance(value, tzinfo) else ZoneInfo(value)
