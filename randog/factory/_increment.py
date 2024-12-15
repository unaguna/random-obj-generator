import datetime as dt
from random import Random
import typing as t

from ._logging import logger
from .._utils.comp import ANYWAY_MAXIMUM
from ._base import Factory
from ._by_iterator import by_iterator
from ..exceptions import FactoryConstructionError


@t.overload
def increment(
    initial_value: t.Optional[int] = None,
    maximum: t.Optional[int] = None,
    step: t.Optional[int] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[int]: ...


@t.overload
def increment(
    initial_value: dt.datetime,
    maximum: t.Optional[dt.datetime] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.datetime]: ...


@t.overload
def increment(
    initial_value: dt.date,
    maximum: t.Optional[dt.date] = None,
    step: t.Optional[dt.timedelta] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.date]: ...


def increment(
    initial_value: t.Optional[t.Any] = None,
    maximum: t.Optional[t.Any] = None,
    step: t.Optional[t.Any] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory which returns sequential numbers.

    Parameters
    ----------
    initial_value : optional
        the first value
    maximum : optional
        the maximum value. If the generated value reaches the maximum value,
        1 is generated next.
        If the maximum value is not specified, it is not reset to 1.
    step : optional
        difference between generated values
    rnd : Random, optional
        It is not normally used, but it can be accepted as an argument
        to match other Factory construction functions.

    Raises
    ------
    FactoryConstructionError
        if it is not satisfied `initial_value <= maximum`
    """
    if initial_value is None:
        initial_value = 1
    if maximum is None:
        maximum = ANYWAY_MAXIMUM
    if step is None:
        if isinstance(initial_value, dt.datetime):
            step = dt.timedelta(seconds=1)
        elif isinstance(initial_value, dt.date):
            step = dt.timedelta(days=1)
        else:
            step = 1
    if isinstance(initial_value, (dt.datetime, dt.date)):
        resume_value = initial_value
    else:
        resume_value = 1

    if not (initial_value <= maximum):
        raise FactoryConstructionError(
            "arguments of increment(initial_value, maximum) must satisfy "
            "initial_value <= maximum"
        )
    if (
        isinstance(initial_value, dt.date)
        and not isinstance(initial_value, dt.datetime)
        and step.microseconds + step.seconds > 0
    ):
        raise FactoryConstructionError(
            "step must be a day/days if initial_value is date"
        )

    return by_iterator(_increment(initial_value, maximum, step, resume_value))


def _increment(initial_value, maximum, step, resume_value) -> t.Iterator:
    next_value = initial_value
    while True:
        yield next_value
        next_value += step

        if next_value > maximum:
            logger.debug(
                "increment() has reached its maximum value and resumes "
                f"from {resume_value}"
            )
            next_value = resume_value
