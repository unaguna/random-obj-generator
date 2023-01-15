import typing as t
from random import Random

from . import Factory, randint, randstr, union
from ..exceptions import FactoryConstructionError

import ranog


_FACTORY_CONSTRUCTOR: t.Dict[type, t.Callable[[t.Optional[Random]], Factory]] = {
    int: lambda rnd: randint(0, 100, rnd=rnd),
    str: lambda rnd: randstr(rnd=rnd),
}


def from_object(
    obj: t.Any,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory:
    """Returns a factory generating value like specified example or type.

    Parameters
    ----------
    obj : int
        the type or the example
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified example or type is not supported.
    """
    if isinstance(obj, ranog.Example):
        return union(*map(lambda x: from_object(x, rnd=rnd), obj), rnd=rnd)
    elif isinstance(obj, type):
        if obj in _FACTORY_CONSTRUCTOR:
            return _FACTORY_CONSTRUCTOR[obj](rnd)
        else:
            raise FactoryConstructionError(
                f"cannot construct factory for unsupported type: {obj}"
            )
    else:
        return from_object(type(obj), rnd=rnd)
