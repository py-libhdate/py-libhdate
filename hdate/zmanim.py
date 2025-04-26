"""
Jewish calendrical times for a given location.

HDate calculates and generates a representation either in English or Hebrew
of the Jewish calendrical times for a given location
"""

import datetime as dt
import logging
import math
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, cast

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

MAX_LATITUDE_ASTRAL = 50.0
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
            [f"{zman} - {zman.local.time()}" for _, zman in self.zmanim.items()]
        )

    def __getattr__(self, name: str) -> Zman:
        if name in (zmanim := self.zmanim):
            return zmanim[name]
        raise AttributeError(f"{type(self).__name__} has no attribute {name}")

    def __dir__(self) -> list[str]:
        return [*super().__dir__(), *self.zmanim.keys()]

    @property
    def candle_lighting(self) -> Optional[dt.datetime]:
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
    def havdalah(self) -> Optional[dt.datetime]:
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

    def _get_utc_sun_time_deg(self, deg: float) -> tuple[int, int]:
        """
        Return the times in minutes from 00:00 (utc) for a given sun altitude.

        This is done for a given sun altitude in sunrise `deg` degrees
        This function only works for altitudes sun really is.
        If the sun never gets to this altitude, the returned sunset and sunrise
        values will be negative. This can happen in low altitude when latitude
        is nearing the poles in winter times, the sun never goes very high in
        the sky there.

        Algorithm from
        https://gml.noaa.gov/grad/solcalc/solareqns.PDF
        The low accuracy solar position equations are used.
        These routines are based on Jean Meeus's book Astronomical Algorithms.
        """

        def gday_of_year(date: dt.date) -> int:
            """Return the number of days since January 1 of the given year."""
            return (date - dt.date(date.year, 1, 1)).days

        gama = 0.0  # location of sun in yearly cycle in radians
        eqtime = 0.0  # difference betwen sun noon and clock noon
        decl = 0.0  # sun declanation
        hour_angle = 0.0  # solar hour angle
        sunrise_angle = math.radians(deg)  # sun angle at sunrise/set

        # get the day of year
        day_of_year = float(gday_of_year(self.date))

        # get radians of sun orbit around earth =)
        gama = 2.0 * math.pi * ((day_of_year - 1) / 365.0)

        # get the diff betwen suns clock and wall clock in minutes
        eqtime = 229.18 * (
            0.000075
            + 0.001868 * math.cos(gama)
            - 0.032077 * math.sin(gama)
            - 0.014615 * math.cos(2.0 * gama)
            - 0.040849 * math.sin(2.0 * gama)
        )

        # calculate suns declanation at the equater in radians
        decl = (
            0.006918
            - 0.399912 * math.cos(gama)
            + 0.070257 * math.sin(gama)
            - 0.006758 * math.cos(2.0 * gama)
            + 0.000907 * math.sin(2.0 * gama)
            - 0.002697 * math.cos(3.0 * gama)
            + 0.00148 * math.sin(3.0 * gama)
        )

        latitude = math.radians(self.location.latitude)

        # the sun real time diff from noon at sunset/rise in radians
        try:
            hour_angle = math.acos(
                math.cos(sunrise_angle) / (math.cos(latitude) * math.cos(decl))
                - math.tan(latitude) * math.tan(decl)
            )
        # check for too high altitudes and return negative values
        except ValueError:
            return -720, -720

        # we use minutes, ratio is 1440min/2pi
        hour_angle = 720.0 * hour_angle / math.pi

        # get sunset/rise times in utc wall clock in minutes from 00:00 time
        # sunrise / sunset
        longitude = self.location.longitude
        return (
            int(720.0 - 4.0 * longitude - hour_angle - eqtime),
            int(720.0 - 4.0 * longitude + hour_angle - eqtime),
        )

    def _datetime_to_minutes_offest(self, time: dt.datetime) -> int:
        """Return the time in minutes from 00:00 (utc) for a given time."""
        return (
            time.hour * 60
            + time.minute
            + (1 if time.second >= 30 else 0)
            + int((time.date() - self.date).total_seconds() // 60)
        )

    def _get_utc_time_of_transit(self, zenith: float, rising: bool) -> int:
        """Return the time in minutes from 00:00 (utc) for a given sun altitude."""
        astral_observer = astral.Observer(
            latitude=self.location.latitude,
            longitude=self.location.longitude,
        )
        return self._datetime_to_minutes_offest(
            astral.sun.time_of_transit(
                astral_observer,
                self.date,
                zenith,
                astral.SunDirection.RISING if rising else astral.SunDirection.SETTING,
            )
        )

    @cached_property
    def zmanim(self) -> dict[str, Zman]:
        """Return a list of Jewish times for the given location."""
        if (not _USE_ASTRAL) or (abs(self.location.latitude) > MAX_LATITUDE_ASTRAL):
            sunrise, sunset = self._get_utc_sun_time_deg(90.833)
            first_light, _ = self._get_utc_sun_time_deg(106.1)
            talit, _ = self._get_utc_sun_time_deg(101.0)
            _, first_stars = self._get_utc_sun_time_deg(96.45)
            _, three_stars = self._get_utc_sun_time_deg(98.5)
        else:
            sunrise = self._get_utc_time_of_transit(
                90.0 + astral.sun.SUN_APPARENT_RADIUS, True
            )
            sunset = self._get_utc_time_of_transit(
                90.0 + astral.sun.SUN_APPARENT_RADIUS, False
            )
            first_light = self._get_utc_time_of_transit(106.1, True)
            talit = self._get_utc_time_of_transit(101.0, True)
            first_stars = self._get_utc_time_of_transit(96.45, False)
            three_stars = self._get_utc_time_of_transit(98.5, False)

        # shaa zmanit by gara, 1/12 of light time
        sun_hour = (sunset - sunrise) // 12
        midday = (sunset + sunrise) // 2
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
