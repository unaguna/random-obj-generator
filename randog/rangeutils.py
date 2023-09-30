import typing as t


class FloatRange:
    _min: float
    _max: float

    def __init__(self, minimum: float, maximum: float):
        self._min = minimum
        self._max = maximum

    def __contains__(self, item):
        return self._min <= item <= self._max

    def __repr__(self):
        return f"frange({self._min}, {self._max})"

    def radius(self, radius: float) -> "FloatRange":
        radius = abs(radius)
        return FloatRange(self._min - radius, self._max + radius)


def frange(minimum: float, maximum: t.Optional[float] = None) -> FloatRange:
    return FloatRange(minimum, maximum if maximum is not None else minimum)
