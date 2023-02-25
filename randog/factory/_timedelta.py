import datetime as dt
import typing as t
from random import Random

from ._base import Factory
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError


def randtimedelta(
    minimum: t.Optional[dt.timedelta] = None,
    maximum: t.Optional[dt.timedelta] = None,
    *,
    unit: t.Optional[dt.timedelta] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.timedelta]:
    """Return a factory generating random timedelta values.

    Parameters
    ----------
    minimum : timedelta, optional
        the minimum
    maximum : timedelta, optional
        the maximum
    unit : timedelta, optional
        the atomic unit
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return TimedeltaRandomFactory(
        minimum,
        maximum,
        unit=unit,
        rnd=rnd,
    )


class TimedeltaRandomFactory(Factory[dt.timedelta]):
    """factory generating random timedelta values"""

    _random: Random
    _min: dt.timedelta
    _max: dt.timedelta
    _unit: dt.timedelta

    def __init__(
        self,
        minimum: t.Optional[dt.timedelta] = None,
        maximum: t.Optional[dt.timedelta] = None,
        *,
        unit: t.Optional[dt.timedelta] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random timedelta values.

        Parameters
        ----------
        minimum : timedelta, optional
            the minimum
        maximum : timedelta, optional
            the maximum
        unit : timedelta, optional
            the atomic unit
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = dfor(rnd, Random())
        self._min, self._max, self._unit = self._normalize(minimum, maximum, unit)

        if self._min > self._max:
            raise FactoryConstructionError("the generating conditions are inconsistent")

    def next(self) -> dt.timedelta:
        raise NotImplementedError()

    @classmethod
    def _normalize(
        cls,
        minimum: t.Optional[dt.timedelta] = None,
        maximum: t.Optional[dt.timedelta] = None,
        unit: t.Optional[dt.timedelta] = None,
    ) -> t.Tuple[dt.timedelta, dt.timedelta, dt.timedelta]:
        # TODO: 実装
        return minimum, maximum, unit
