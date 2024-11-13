"""Location data for HDate - used by Zmanim."""

from dataclasses import dataclass
from datetime import tzinfo
from typing import Union
from zoneinfo import ZoneInfo


@dataclass
class Location:
    """Define a geolocation for Zmanim calculations."""

    name: str = "Jerusalem"
    latitude: float = 31.778
    longitude: float = 35.235
    timezone: Union[str, tzinfo] = ZoneInfo("Asia/Jerusalem")
    altitude: float = 754
    diaspora: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.timezone, str):
            self.timezone = ZoneInfo(self.timezone)

    def __repr__(self) -> str:
        """Return a representation of Location for programmatic use."""
        return (
            f"Location(name={self.name!r}, latitude={self.latitude}, "
            f"longitude={self.longitude}, timezone={self.timezone!r}, "
            f"altitude={self.altitude}, diaspora={self.diaspora})"
        )
