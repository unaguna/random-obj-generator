import abc
import inspect
import typing as t
from random import Random

from .._logging import logger
from ..._utils.comp import ANYWAY_MAXIMUM, ANYWAY_MINIMUM
from .._base import Factory, T as F_T
from ...exceptions import FactoryConstructionError

S = t.TypeVar("S")


class Iterrange(Factory[F_T], abc.ABC, t.Generic[F_T, S]):
    initial_value: F_T
    minimum: F_T
    maximum: F_T
    step: S
    cyclic: bool
    resume_value: F_T
    next_value: F_T
    _impl_iterator: t.Iterator[F_T]

    def __init__(
        self,
        initial_value: F_T,
        maximum: t.Optional[F_T],
        step: t.Optional[S],
        cyclic: bool,
        rnd: t.Optional[Random] = None,
    ):
        if initial_value is not None:
            self.initial_value = initial_value
        else:
            self.initial_value = self.default_initial_value()
        if step is not None:
            self.step = step
        else:
            self.step = self.default_step()
        self.cyclic = cyclic

        if self.step_sign() < 0:
            minimum = maximum
            maximum = None
        else:
            minimum = None
        if maximum is None:
            maximum = ANYWAY_MAXIMUM
        if minimum is None:
            minimum = ANYWAY_MINIMUM
        self.minimum = minimum
        self.maximum = maximum

        self.resume_value = self.initial_value

        arg_info = inspect.getargvalues(inspect.currentframe())
        self.validate_args(**{key: arg_info.locals[key] for key in arg_info.args[1:]})

        self._impl_iterator = self._iterator()

    @abc.abstractmethod
    def default_initial_value(self) -> F_T:
        pass

    @abc.abstractmethod
    def default_step(self) -> S:
        pass

    @abc.abstractmethod
    def step_sign(self) -> t.Literal[-1, 0, 1]:
        pass

    def validate_args(self, **kwargs):
        if self.step_sign() >= 0:
            if not (self.initial_value <= self.maximum):
                raise FactoryConstructionError(
                    "arguments of iterrange(initial_value, maximum) must satisfy "
                    "initial_value <= maximum"
                )
        else:
            if not (self.initial_value >= self.minimum):
                raise FactoryConstructionError(
                    "arguments of iterrange(initial_value, maximum) must satisfy "
                    "maximum <= initial_value if step < 0"
                )

    def _next(self) -> F_T:
        return next(self._impl_iterator)

    def _iterator(self) -> t.Iterator[F_T]:
        next_value = self.initial_value
        while True:
            yield next_value
            next_value += self.step

            if next_value > self.maximum or next_value < self.minimum:
                if self.cyclic:
                    logger.debug(
                        "iterrange() has reached its maximum value and resumes "
                        f"from {self.resume_value}"
                    )
                    next_value = self.resume_value
                else:
                    logger.debug(
                        "iterrange() has reached its maximum value. "
                        "This factory no longer generates values."
                    )
                    break


def _iterrange(
    initial_value, minimum, maximum, step, resume_value, *, cyclic: bool
) -> t.Iterator:
    next_value = initial_value
    while True:
        yield next_value
        next_value += step

        if next_value > maximum or next_value < minimum:
            if cyclic:
                logger.debug(
                    "iterrange() has reached its maximum value and resumes "
                    f"from {resume_value}"
                )
                next_value = resume_value
            else:
                logger.debug(
                    "iterrange() has reached its maximum value. "
                    "This factory no longer generates values."
                )
                break
