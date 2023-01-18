import typing as t
from random import Random

from . import DictItem, Factory, randdict, randfloat, randlist, randint, randstr, union
from ..exceptions import FactoryConstructionError

import ranog


_FACTORY_CONSTRUCTOR: t.Dict[type, t.Callable[[t.Optional[Random]], Factory]] = {
    int: lambda rnd: randint(0, 100, rnd=rnd),
    float: lambda rnd: randfloat(0, 1.0, rnd=rnd),
    str: lambda rnd: randstr(rnd=rnd),
    list: lambda rnd: randlist(randstr(), rnd=rnd),
    tuple: lambda rnd: randlist(randstr(), type=tuple, rnd=rnd),
    dict: lambda rnd: randdict({"key": randint(0, 100, rnd=rnd)}, rnd=rnd),
}


def _dict_item(obj, *, _recursive) -> DictItem:
    if isinstance(obj, ranog.DictItemExample):
        return DictItem(_recursive(obj.example), obj.prop_exists)
    else:
        return DictItem(_recursive(obj))


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

    def _recursive(child: t.Any) -> Factory:
        return from_example(child, rnd=rnd)

    if isinstance(example, ranog.Example):
        return union(*map(_recursive, example), rnd=rnd)
    elif isinstance(example, Factory):
        return example
    elif isinstance(example, type):
        if example in _FACTORY_CONSTRUCTOR:
            return _FACTORY_CONSTRUCTOR[example](rnd)
        else:
            raise FactoryConstructionError(
                f"cannot construct factory for unsupported type: {example}"
            )
    elif isinstance(example, t.Mapping):
        return randdict(
            {k: _dict_item(v, _recursive=_recursive) for k, v in example.items()}
        )
    elif isinstance(example, t.Sequence) and not isinstance(example, str):
        if isinstance(example, (tuple, list)):
            _type = type(example)
        else:
            _type = None
        return randlist(*map(_recursive, example), type=_type, rnd=rnd)
    else:
        return _recursive(type(example))
