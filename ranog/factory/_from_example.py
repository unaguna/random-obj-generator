import typing as t
from random import Random

from . import DictItem, Factory, randdict, randint, randstr, union
from ..exceptions import FactoryConstructionError

import ranog


_FACTORY_CONSTRUCTOR: t.Dict[type, t.Callable[[t.Optional[Random]], Factory]] = {
    int: lambda rnd: randint(0, 100, rnd=rnd),
    str: lambda rnd: randstr(rnd=rnd),
    dict: lambda rnd: randdict({"key": randint(0, 100, rnd=rnd)}, rnd=rnd),
}


def _dict_item(obj, *, rnd: t.Optional[Random]) -> DictItem:
    if isinstance(obj, ranog.DictItemExample):
        return DictItem(from_example(obj.example, rnd=rnd), obj.prop_exists)
    else:
        return DictItem(from_example(obj, rnd=rnd))


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
    elif isinstance(example, t.Mapping):
        return randdict({k: _dict_item(v, rnd=rnd) for k, v in example.items()})
    else:
        return from_example(type(example), rnd=rnd)
