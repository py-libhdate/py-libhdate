"""
Jewish calendrical times for a given location.

HDate calculates and generates a representation either in English or Hebrew
of the Jewish calendrical times for a given location
"""

import datetime as dt
import logging
import math
from dataclasses import dataclass, field
from typing import Optional, cast

from hdate.date import HDate
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
    utc_zman: dt.datetime = dt.datetime.now()
    local_zman: dt.datetime = dt.datetime.now()

    def __post_init__(self) -> None:
        basetime = dt.datetime.combine(self.date, dt.time()).replace(
            tzinfo=dt.timezone.utc
        )
        self.utc_zman = basetime + dt.timedelta(minutes=self.minutes)
        self.local_zman = self.utc_zman.astimezone(self.timezone)


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
    language: str = "hebrew"
    candle_lighting_offset: int = 18
    havdalah_offset: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.date, dt.date):
            raise TypeError("date has to be of type datetime.date")
        self.set_language(self.language)
        self.today = HDate(gdate=self.date, diaspora=self.location.diaspora)
        self.tomorrow = HDate(
            gdate=self.date + dt.timedelta(days=1), diaspora=self.location.diaspora
        )

        if _USE_ASTRAL and (abs(self.location.latitude) <= MAX_LATITUDE_ASTRAL):
            self.astral_observer = astral.Observer(
                latitude=self.location.latitude, longitude=self.location.longitude
            )
            self.astral_sun = astral.sun.sun(self.astral_observer, self.date)

    def __str__(self) -> str:
        """Return a string representation of Zmanim in the selected language."""
        return "\n".join(
            [
                f"{zman} - {zman.local_zman.time()}"
                for zman in self.get_utc_sun_time_full()
            ]
        )

    @property
    def zmanim(self) -> dict[str, dt.datetime]:
        """Return a dictionary of the zmanim the object represents."""
        return {zman.name: zman.local_zman for zman in self.get_utc_sun_time_full()}

    @property
    def candle_lighting(self) -> Optional[dt.datetime]:
        """Return the time for candle lighting, or None if not applicable."""
        # If today is a Yom Tov or Shabbat, and tomorrow is a Yom Tov or
        # Shabbat return the havdalah time as the candle lighting time.
        if (
            self.today.is_yom_tov or self.today.is_shabbat
        ) and self.tomorrow.is_yom_tov:
            return self._havdalah_datetime

        # Otherwise, if today is Friday or erev Yom Tov, return candle
        # lighting.
        if self.tomorrow.is_shabbat or self.tomorrow.is_yom_tov:
            return self.zmanim["sunset"] - dt.timedelta(
                minutes=self.candle_lighting_offset
            )
        return None

    @property
    def _havdalah_datetime(self) -> dt.datetime:
        """Compute the havdalah time based on settings."""
        if self.havdalah_offset == 0:
            return self.zmanim["three_stars"]
        # Otherwise, use the offset.
        return self.zmanim["sunset"] + dt.timedelta(minutes=self.havdalah_offset)

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
        if self.today.is_shabbat or self.today.is_yom_tov:
            if self.tomorrow.is_shabbat or self.tomorrow.is_yom_tov:
                return None
            return self._havdalah_datetime
        return None

    def _timezone_aware(self, time: dt.datetime) -> dt.datetime:
        """Check if time is tz-naive and make it timezone-aware"""
        if time.tzinfo is None or time.tzinfo.utcoffset(time) is None:
            time = time.replace(tzinfo=cast(dt.tzinfo, self.location.timezone))
        return time

    def issur_melacha_in_effect(self, time: dt.datetime = dt.datetime.now()) -> bool:
        """At the given time, return whether issur melacha is in effect."""
        _time = self._timezone_aware(time)
        if (self.today.is_shabbat or self.today.is_yom_tov) and (
            self.tomorrow.is_shabbat or self.tomorrow.is_yom_tov
        ):
            return True
        if (
            (self.today.is_shabbat or self.today.is_yom_tov)
            and self.havdalah is not None
            and (_time < self.havdalah)
        ):
            return True
        if (
            (self.tomorrow.is_shabbat or self.tomorrow.is_yom_tov)
            and self.candle_lighting is not None
            and (_time >= self.candle_lighting)
        ):
            return True

        return False

    def erev_shabbat_chag(self, time: dt.datetime = dt.datetime.now()) -> bool:
        """At the given time, return whether erev shabbat or chag"""
        _time = self._timezone_aware(time)
        if self.candle_lighting is None:  # No need to check further
            return False

        if (
            (self.tomorrow.is_shabbat or self.tomorrow.is_yom_tov)
            and (not self.today.is_shabbat and not self.today.is_yom_tov)
            and (_time < self.candle_lighting)
        ):
            return True

        return False

    def motzei_shabbat_chag(self, time: dt.datetime = dt.datetime.now()) -> bool:
        """At the given time, return whether motzei shabbat or chag"""
        _time = self._timezone_aware(time)
        if self.havdalah is None:  # If there's no havdala, no need to check further
            return False

        if (self.today.is_shabbat or self.today.is_yom_tov) and (
            self.tomorrow.is_shabbat or self.tomorrow.is_yom_tov
        ):
            return False
        if (self.today.is_shabbat or self.today.is_yom_tov) and (_time > self.havdalah):
            return True

        return False

    def gday_of_year(self) -> int:
        """Return the number of days since January 1 of the given year."""
        return (self.date - dt.date(self.date.year, 1, 1)).days

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
        http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html
        The low accuracy solar position equations are used.
        These routines are based on Jean Meeus's book Astronomical Algorithms.
        """
        gama = 0.0  # location of sun in yearly cycle in radians
        eqtime = 0.0  # difference betwen sun noon and clock noon
        decl = 0.0  # sun declanation
        hour_angle = 0.0  # solar hour angle
        sunrise_angle = math.pi * deg / 180.0  # sun angle at sunrise/set

        # get the day of year
        day_of_year = float(self.gday_of_year())

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

        # we use radians, ratio is 2pi/360
        latitude = math.pi * self.location.latitude / 180.0

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
        return self._datetime_to_minutes_offest(
            astral.sun.time_of_transit(
                self.astral_observer,
                self.date,
                zenith,
                astral.SunDirection.RISING if rising else astral.SunDirection.SETTING,
            )
        )

    def get_utc_sun_time_full(self) -> tuple[Zman, ...]:
        """Return a list of Jewish times for the given location."""
        if (not _USE_ASTRAL) or (abs(self.location.latitude) > MAX_LATITUDE_ASTRAL):
            sunrise, sunset = self._get_utc_sun_time_deg(90.833)
            first_light, _ = self._get_utc_sun_time_deg(106.1)
            talit, _ = self._get_utc_sun_time_deg(101.0)
            _, first_stars = self._get_utc_sun_time_deg(96.45)
            _, three_stars = self._get_utc_sun_time_deg(98.5)
        else:
            sunrise = self._datetime_to_minutes_offest(self.astral_sun["sunrise"])
            sunset = self._datetime_to_minutes_offest(self.astral_sun["sunset"])
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
            zman.set_language(self._language)
            return zman

        zmanim = (
            make_zman("alot_hashachar", first_light),
            make_zman("talit_tefilins_time", talit),
            make_zman("sunrise", sunrise),
            make_zman("shema_eot_mga", first_light + mga_sunhour * 3.0),
            make_zman("shema_eot_gra", sunrise + sun_hour * 3.0),
            make_zman("tefila_eot_mga", first_light + mga_sunhour * 4.0),
            make_zman("tefila_eot_gra", sunrise + sun_hour * 4.0),
            make_zman("midday", midday),
            make_zman("big_mincha", sunrise + 6.5 * sun_hour),
            make_zman("big_mincha_min", midday + 30),
            make_zman("small_mincha", sunrise + 9.5 * sun_hour),
            make_zman("plag_mincha", sunset - 1.25 * sun_hour),
            make_zman("sunset", sunset),
            make_zman("first_stars", first_stars),
            make_zman("three_stars", three_stars),
            make_zman("stars_out", sunset + 18.0 * sun_hour / 60.0),
            make_zman("night_by_rabbeinu_tam", sunset + sun_hour * 1.2),
            make_zman("midnight", midday + 12 * 60.0),
        )

        return zmanim
