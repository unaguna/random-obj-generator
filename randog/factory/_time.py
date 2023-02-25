import datetime as dt
import typing as t
from random import Random

from ._base import Factory


def randtime(
    *,
    tzinfo: t.Optional[dt.tzinfo] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.time]:
    """Return a factory generating random time values.

    Parameters
    ----------
    tzinfo : tzinfo, optional
        the timezone information
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return TimeRandomFactory(
        tzinfo=tzinfo,
        rnd=rnd,
    )


class TimeRandomFactory(Factory[dt.time]):
    """factory generating random time values"""

    _random: Random
    _tzinfo: dt.tzinfo

    def __init__(
        self,
        *,
        tzinfo: t.Optional[dt.tzinfo] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random time values.

        Parameters
        ----------
        tzinfo : tzinfo, optional
            the timezone information
        rnd : Random, optional
            random number generator to be used
        """
        self._random = rnd
        self._tzinfo = tzinfo

    def next(self) -> dt.time:
        raise NotImplementedError()
