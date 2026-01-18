"""
Jewish calendrical times for a given location.

HDate calculates and generates a representation either in English or Hebrew
of the Jewish calendrical times for a given location.
"""

import datetime as dt
import logging
import math
from dataclasses import dataclass, field
from functools import cached_property
from typing import cast

from hdate.hebrew_date import is_shabbat
from hdate.holidays import is_yom_tov
from hdate.location import Location
from hdate.translator import TranslatorMixin

try:
    import astral
    import astral.sun

    _USE_ASTRAL = True
except ImportError:
    _USE_ASTRAL = False

MAX_LATITUDE_ASTRAL = 66.5
_LOGGER = logging.getLogger(__name__)


@dataclass
class Zman(TranslatorMixin):
    """A specific time."""

    name: str
    minutes: float
    date: dt.date
    timezone: dt.tzinfo

    def __post_init__(self) -> None:
        basetime = dt.datetime.combine(self.date, dt.time()).replace(
            tzinfo=dt.timezone.utc
        )
        self.utc = basetime + dt.timedelta(minutes=self.minutes)
        self.local = self.utc.astimezone(self.timezone)


@dataclass
class Zmanim(TranslatorMixin):  # pylint: disable=too-many-instance-attributes
    """Return Jewish day times.

    The Zmanim class returns times for the specified day ONLY. If you wish to
    obtain times for the interval of a multi-day holiday for example, you need
    to use Zmanim in conjunction with some of the iterative properties of
    HDate. Also, Zmanim are reported regardless of the current time. So the
    havdalah value is constant if the current time is before or after it.
    The current time is only used to report the "issur_melacha_in_effect"
    property.
    """

    date: dt.date = field(default_factory=dt.date.today)
    location: Location = field(default_factory=Location)
    candle_lighting_offset: int = 18
    havdalah_offset: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.date, dt.date):
            raise TypeError("date has to be of type datetime.date")
        tomorrow = self.date + dt.timedelta(days=1)
        self._today_is_shabbat = is_shabbat(self.date)
        self._tomorrow_is_shabbat = is_shabbat(tomorrow)
        self._today_is_yom_tov = is_yom_tov(self.date, self.location.diaspora)
        self._tomorrow_is_yom_tov = is_yom_tov(tomorrow, self.location.diaspora)

    def __str__(self) -> str:
        return "\n".join(
            [
                f"{zman} - {zman.local.strftime('%H:%M:%S')}"
                for _, zman in self.zmanim.items()
            ]
        )

    def __getattr__(self, name: str) -> Zman:
        if name in (zmanim := self.zmanim):
            return zmanim[name]
        raise AttributeError(f"{type(self).__name__} has no attribute {name}")

    def __dir__(self) -> list[str]:
        return [*super().__dir__(), *self.zmanim.keys()]

    @property
    def candle_lighting(self) -> dt.datetime | None:
        """Return the time for candle lighting, or None if not applicable."""
        # If today is a Yom Tov or Shabbat, and tomorrow is a Yom Tov or
        # Shabbat return the havdalah time as the candle lighting time.
        if (
            self._today_is_yom_tov or self._today_is_shabbat
        ) and self._tomorrow_is_yom_tov:
            return self._havdalah_datetime

        # Otherwise, if today is Friday or erev Yom Tov, return candle
        # lighting.
        if self._tomorrow_is_shabbat or self._tomorrow_is_yom_tov:
            return self.shkia.local - dt.timedelta(minutes=self.candle_lighting_offset)
        return None

    @property
    def _havdalah_datetime(self) -> dt.datetime:
        """Compute the havdalah time based on settings."""
        if self.havdalah_offset == 0:
            return self.tset_hakohavim_shabbat.local
        # Otherwise, use the offset.
        return self.shkia.local + dt.timedelta(minutes=self.havdalah_offset)

    @property
    def havdalah(self) -> dt.datetime | None:
        """Return the time for havdalah, or None if not applicable.

        If havdalah_offset is 0, uses the time for three_stars. Otherwise,
        adds the offset to the time of sunset and uses that.
        If it's currently a multi-day YomTov, and the end of the stretch is
        after today, the havdalah value is defined to be None (to avoid
        misleading the user that melacha is permitted).
        """
        # If today is Yom Tov or Shabbat, and tomorrow is Yom Tov or Shabbat,
        # then there is no havdalah value for today. Technically, there is
        # havdalah mikodesh l'kodesh, but that is represented in the
        # candle_lighting value to avoid misuse of the havdalah API.
        if self._today_is_shabbat or self._today_is_yom_tov:
            if self._tomorrow_is_shabbat or self._tomorrow_is_yom_tov:
                return None
            return self._havdalah_datetime
        return None

    def _timezone_aware(self, time: dt.datetime) -> dt.datetime:
        """Check if time is tz-naive and make it timezone-aware"""
        if time.tzinfo is None or time.tzinfo.utcoffset(time) is None:
            time = time.replace(tzinfo=cast(dt.tzinfo, self.location.timezone))
        return time

    def issur_melacha_in_effect(self, time: dt.datetime) -> bool:
        """At the given time, return whether issur melacha is in effect."""
        _time = self._timezone_aware(time)
        if (self._today_is_shabbat or self._today_is_yom_tov) and (
            self._tomorrow_is_shabbat or self._tomorrow_is_yom_tov
        ):
            return True
        if (
            (self._today_is_shabbat or self._today_is_yom_tov)
            and self.havdalah is not None
            and (_time < self.havdalah)
        ):
            return True
        if (
            (self._tomorrow_is_shabbat or self._tomorrow_is_yom_tov)
            and self.candle_lighting is not None
            and (_time >= self.candle_lighting)
        ):
            return True

        return False

    def erev_shabbat_chag(self, time: dt.datetime) -> bool:
        """At the given time, return whether erev shabbat or chag"""
        _time = self._timezone_aware(time)
        if self.candle_lighting is None:  # No need to check further
            return False

        if (
            (self._tomorrow_is_shabbat or self._tomorrow_is_yom_tov)
            and (not self._today_is_shabbat and not self._today_is_yom_tov)
            and (_time < self.candle_lighting)
        ):
            return True

        return False

    def motzei_shabbat_chag(self, time: dt.datetime) -> bool:
        """At the given time, return whether motzei shabbat or chag"""
        _time = self._timezone_aware(time)
        if self.havdalah is None:  # If there's no havdala, no need to check further
            return False

        if (self._today_is_shabbat or self._today_is_yom_tov) and (
            _time >= self.havdalah
        ):
            return True

        return False

    def _get_utc_sun_time_deg(self, deg: float) -> tuple[int | None, int | None]:
        # pylint: disable=too-many-locals
        """
        Return the times in minutes from 00:00 (utc) for a given sun altitude.

        Uses NOAA/Meeus astronomical algorithms for high precision.
        Returns (None, None) if the sun never reaches the specified altitude
        (e.g., White Nights in high latitudes).

        Args:
            deg: The altitude of the sun (90 - zenith).
                 0.833 for Sunrise/Sunset (geometric).
                 16.1 for Alot HaShachar, etc.
        """

        # Julian Day at 12:00 UTC (Meeus formula)
        def get_julian_day(date: dt.date) -> float:
            year, month, day = date.year, date.month, date.day
            if month <= 2:
                year -= 1
                month += 12
            a = math.floor(year / 100)
            b = 2 - a + math.floor(a / 4)
            return (
                math.floor(365.25 * (year + 4716))
                + math.floor(30.6001 * (month + 1))
                + day
                + b
                - 1524.5
            )

        # Time variables
        jd = get_julian_day(self.date)
        t = (jd - 2451545.0) / 36525.0  # Julian Century
        # Geometric Mean Longitude Sun (deg)
        geom_mean_long_sun = (280.46646 + 36000.76983 * t + 0.0003032 * t**2) % 360
        # Geometric Mean Anomaly Sun (deg)
        geom_mean_anom_sun = 357.52911 + 35999.05029 * t - 0.0001537 * t**2
        # Eccentricity Earth Orbit
        eccent_earth_orbit = 0.016708634 - 0.000042037 * t - 0.0000001267 * t**2
        # Sun Equation of Center
        sun_eq_of_ctr = (
            math.sin(math.radians(geom_mean_anom_sun))
            * (1.914602 - 0.004817 * t - 0.000014 * t**2)
            + math.sin(math.radians(2 * geom_mean_anom_sun)) * (0.019993 - 0.000101 * t)
            + math.sin(math.radians(3 * geom_mean_anom_sun)) * 0.000289
        )
        # Sun True Longitude (deg)
        sun_true_long = geom_mean_long_sun + sun_eq_of_ctr
        # Sun Apparent Longitude (deg)
        sun_app_long = (
            sun_true_long
            - 0.00569
            - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * t))
        )
        # Mean Obliquity Ecliptic (deg)
        mean_obliq_ecliptic = (
            23
            + (26 + (21.448 - 46.8150 * t - 0.00059 * t**2 + 0.001813 * t**3) / 60) / 60
        )
        # Obliquity Correction (deg)
        obliq_correction = mean_obliq_ecliptic + 0.00256 * math.cos(
            math.radians(125.04 - 1934.136 * t)
        )
        # Sun Declination (radians)
        sun_decl_rad = math.asin(
            math.sin(math.radians(obliq_correction))
            * math.sin(math.radians(sun_app_long))
        )
        # Equation of Time (minutes)
        var_y = math.tan(math.radians(obliq_correction / 2)) ** 2

        eq_time = 4 * math.degrees(
            var_y * math.sin(math.radians(2 * geom_mean_long_sun))
            - 2 * eccent_earth_orbit * math.sin(math.radians(geom_mean_anom_sun))
            + 4
            * eccent_earth_orbit
            * var_y
            * math.sin(math.radians(geom_mean_anom_sun))
            * math.cos(math.radians(2 * geom_mean_long_sun))
            - 0.5 * var_y * var_y * math.sin(math.radians(4 * geom_mean_long_sun))
            - 1.25
            * eccent_earth_orbit**2
            * math.sin(math.radians(2 * geom_mean_anom_sun))
        )

        # Hour Angle
        # deg input is Altitude (90-Zenith).
        # We need Zenith for the formula.
        # But for compatibility with legacy input:
        # Standard usage implies we pass the target zenith angle.
        # We assume 'deg' here is the ZENITH angle (90 + depression).
        zenith_rad = math.radians(deg)
        lat_rad = math.radians(self.location.latitude)

        try:
            cos_ha = (
                math.cos(zenith_rad) - (math.sin(lat_rad) * math.sin(sun_decl_rad))
            ) / (math.cos(lat_rad) * math.cos(sun_decl_rad))

            # Check for White Nights (Sun never goes below horizon) or Polar Night
            if cos_ha > 1.0 or cos_ha < -1.0:
                return None, None

            ha_deg = math.degrees(math.acos(cos_ha))

            # UTC Minutes
            # Solar Noon = 720 - 4*Longitude - EqTime
            solar_noon = 720 - (4 * self.location.longitude) - eq_time

            return (
                int(solar_noon - 4 * ha_deg),
                int(solar_noon + 4 * ha_deg),
            )

        except ValueError:
            return None, None

    def _datetime_to_minutes_offset(self, time: dt.datetime) -> int:
        """Return minutes offset from self.date at 00:00."""
        anchor = dt.datetime.combine(self.date, dt.time.min, tzinfo=time.tzinfo)
        delta_seconds = (time - anchor).total_seconds()
        return int(delta_seconds / 60 + 0.5)

    def _get_utc_time_of_transit(self, zenith: float, rising: bool) -> int:
        """
        Return the time in minutes from 00:00 (utc) for a given sun altitude via Astral.
        """
        astral_observer = astral.Observer(
            latitude=self.location.latitude,
            longitude=self.location.longitude,
        )
        return self._datetime_to_minutes_offset(
            astral.sun.time_of_transit(
                astral_observer,
                self.date,
                zenith,
                astral.SunDirection.RISING if rising else astral.SunDirection.SETTING,
            )
        )

    def _get_safe_sun_time(
        self, degrees: float, rising: bool, midnight_fallback: float
    ) -> float:
        """
        Retrieve solar time.
        If the sun does not reach the required angle (e.g. White Night),
        fall back to Solar Midnight (the deepest part of the night).
        """
        # If using Astral and configured (Legacy path)
        if _USE_ASTRAL and abs(self.location.latitude) <= 50.0:
            return self._get_utc_time_of_transit(degrees, rising)

        # Native High-Precision Path
        rise, set_ = self._get_utc_sun_time_deg(degrees)

        if rise is not None and set_ is not None:
            return float(rise if rising else set_)

        # Fallback for High Latitudes (White Nights)
        # If we can't find Alot/Tzeit, we use Solar Midnight (lowest sun point).
        return midnight_fallback

    @cached_property
    def zmanim(self) -> dict[str, Zman]:
        # pylint: disable=too-many-locals
        """Return a list of Jewish times for the given location."""

        # Calculate Base Sun Times (Sunrise/Sunset)
        # We must have a valid sunrise/sunset for the day to exist halachically.
        sunrise_raw, sunset_raw = self._get_utc_sun_time_deg(90.833)

        if sunrise_raw is None or sunset_raw is None:
            # Logic for Polar Day/Night could go here.
            # For now, we default to 6:00/18:00 or raise, but let's assume valid day.
            # If we are here, we are > 66.5 deg or edge case.
            sunrise, sunset = 360.0, 1080.0  # Emergency fallback 6am/6pm
        else:
            sunrise, sunset = float(sunrise_raw), float(sunset_raw)

        # Solar Midday and Midnight
        midday = (sunset + sunrise) / 2
        midnight = (midday + 720) % 1440

        # Calculate Twilight Times with Fallbacks
        # If degrees are not reached (White Night), use midnight.
        first_light = self._get_safe_sun_time(106.1, True, midnight)
        talit = self._get_safe_sun_time(101.0, True, midnight)
        first_stars = self._get_safe_sun_time(96.45, False, midnight)
        three_stars = self._get_safe_sun_time(98.5, False, midnight)

        # Shaot Zmaniot
        sun_hour = (sunset - sunrise) / 12
        mga_sunhour = (midday - first_light) / 6

        def make_zman(key: str, time: float) -> Zman:
            timezone = cast(dt.tzinfo, self.location.timezone)
            zman = Zman(key, time, self.date, timezone)
            return zman

        _zmanim = {
            "alot_hashachar": first_light,
            "talit_and_tefillin": talit,
            "netz_hachama": sunrise,
            "sof_zman_shema_mga": first_light + mga_sunhour * 3.0,
            "sof_zman_shema_gra": sunrise + sun_hour * 3.0,
            "sof_zman_tfilla_mga": first_light + mga_sunhour * 4.0,
            "sof_zman_tfilla_gra": sunrise + sun_hour * 4.0,
            "chatzot_hayom": midday,
            "mincha_gedola": sunrise + 6.5 * sun_hour,
            "mincha_gedola_30min": midday + 30,
            "mincha_ketana": sunrise + 9.5 * sun_hour,
            "plag_hamincha": sunset - 1.25 * sun_hour,
            "shkia": sunset,
            "tset_hakohavim_tsom": first_stars,
            "tset_hakohavim_shabbat": three_stars,
            "tset_hakohavim": sunset + 18.0 * sun_hour / 60.0,
            "tset_hakohavim_rabeinu_tam": sunset + sun_hour * 1.2,
            "chatzot_halayla": midday + 12 * 60.0,
        }

        return {key: make_zman(key, time) for key, time in _zmanim.items()}
