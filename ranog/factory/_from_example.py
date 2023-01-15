import typing as t
from random import Random

from . import Factory, randint, randstr, union
from ..exceptions import FactoryConstructionError

import ranog


_FACTORY_CONSTRUCTOR: t.Dict[type, t.Callable[[t.Optional[Random]], Factory]] = {
    int: lambda rnd: randint(0, 100, rnd=rnd),
    str: lambda rnd: randstr(rnd=rnd),
}


def from_example(
    example: t.Any,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory:
    """Returns a factory generating value like specified example or type.

    Parameters
    ----------
    example : Any
        the type or the example
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified example or type is not supported.
    """
    if isinstance(example, ranog.Example):
        return union(*map(lambda x: from_example(x, rnd=rnd), example), rnd=rnd)
    elif isinstance(example, type):
        if example in _FACTORY_CONSTRUCTOR:
            return _FACTORY_CONSTRUCTOR[example](rnd)
        else:
            raise FactoryConstructionError(
                f"cannot construct factory for unsupported type: {example}"
            )
    else:
        return from_example(type(example), rnd=rnd)
