"""Location data for HDate - used by Zmanim."""

from dataclasses import dataclass
from datetime import tzinfo
from typing import Union
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
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
            object.__setattr__(self, "timezone", ZoneInfo(self.timezone))
