import datetime as dt
import typing as t
from random import Random

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randdatetime(
    a: t.Optional[dt.datetime] = None,
    b: t.Optional[dt.datetime] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.datetime]:
    """Return a factory generating random datetime values.

    Parameters
    ----------
    a : datetime, optional
        the minimum
    b : datetime, optional
        the maximum
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return DatetimeRandomFactory(a, b, rnd=rnd)


class DatetimeRandomFactory(Factory[dt.datetime]):
    """factory generating random datetime values"""

    _random: Random
    _min: dt.datetime
    _max: dt.datetime
    _range: dt.timedelta

    def __init__(
        self,
        minimum: t.Optional[dt.datetime] = None,
        maximum: t.Optional[dt.datetime] = None,
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random datetime values.

        Parameters
        ----------
        minimum : datetime, optional
            the minimum
        maximum : datetime, optional
            the maximum
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = dfor(rnd, Random())
        self._min, self._max = self._normalize(minimum, maximum)

        if (self._min.tzinfo is None and self._max.tzinfo is not None) or (
            self._min.tzinfo is not None and self._max.tzinfo is None
        ):
            raise FactoryConstructionError("the generating conditions are inconsistent")
        if self._min > self._max:
            raise FactoryConstructionError("the generating conditions are inconsistent")

        self._range = self._max - self._min

    def next(self) -> dt.datetime:
        weight = self._random.random()

        return self._min + self._range * weight

    @classmethod
    def _normalize(
        cls,
        minimum: t.Optional[dt.datetime],
        maximum: t.Optional[dt.datetime],
    ) -> t.Tuple[dt.datetime, dt.datetime]:
        if minimum is not None and maximum is not None:
            return minimum, maximum
        elif minimum is not None:
            return minimum, minimum + dt.timedelta(days=1)
        elif maximum is not None:
            return maximum - dt.timedelta(days=1), maximum
        else:
            now = dt.datetime.utcnow()
            return now - dt.timedelta(hours=12), now + dt.timedelta(hours=12)
