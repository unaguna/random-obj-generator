import math
import typing as t


class FloatInterval:
    _min: float
    _max: float

    def __init__(self, minimum: float, maximum: float):
        self._min = minimum
        self._max = maximum

    def __contains__(self, item):
        return self._min <= item <= self._max

    def __repr__(self):
        return f"interval({self._min}, {self._max})"

    def radius(self, radius: float) -> "FloatInterval":
        radius = abs(radius)
        return FloatInterval(self._min - radius, self._max + radius)

    def count_int(self) -> int:
        return int(math.floor(self._max) - math.ceil(self._min)) + 1

    def minmax(self) -> t.Iterable[float]:
        return self._min, self._max


class IntInterval(FloatInterval):
    _min: int
    _max: int

    def radius(self, radius: float) -> "FloatInterval":
        radius = abs(radius)
        if isinstance(radius, int):
            return IntInterval(self._min - radius, self._max + radius)
        else:
            return FloatInterval(self._min - radius, self._max + radius)

    def count_int(self) -> int:
        return self._max - self._min + 1


@t.overload
def interval(minimum: int, maximum: t.Optional[int] = None) -> IntInterval:
    pass


@t.overload
def interval(minimum: float, maximum: t.Optional[float] = None) -> FloatInterval:
    pass


def interval(minimum: float, maximum: t.Optional[float] = None) -> FloatInterval:
    if maximum is None:
        maximum = minimum

    if isinstance(minimum, int) and isinstance(maximum, int):
        return IntInterval(minimum, maximum)
    else:
        return FloatInterval(minimum, maximum)
