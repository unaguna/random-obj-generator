from decimal import Decimal
import typing as t
from random import Random

from . import (
    DictItem,
    Factory,
    randdecimal,
    randdict,
    randfloat,
    randlist,
    randint,
    randstr,
    union,
)
from ..exceptions import FactoryConstructionError

import ranog


_FACTORY_CONSTRUCTOR: t.Dict[type, t.Callable[[t.Optional[Random]], Factory]] = {
    int: lambda rnd: randint(0, 100, rnd=rnd),
    float: lambda rnd: randfloat(0, 1.0, rnd=rnd),
    Decimal: lambda rnd: randdecimal(0, 1.0, rnd=rnd),
    str: lambda rnd: randstr(rnd=rnd),
    list: lambda rnd: randlist(randstr(), rnd=rnd),
    tuple: lambda rnd: randlist(randstr(), type=tuple, rnd=rnd),
    dict: lambda rnd: randdict({"key": randint(0, 100, rnd=rnd)}, rnd=rnd),
}


class FromExampleContext:
    _path: t.Tuple[t.Any, ...]

    def __init__(self, path: t.Tuple[t.Any, ...]):
        self._path = path

    @property
    def path(self) -> t.Sequence[t.Any]:
        return self._path

    @classmethod
    def root(cls) -> "FromExampleContext":
        return FromExampleContext(
            path=tuple(),
        )

    def child(self, key: t.Any) -> "FromExampleContext":
        return FromExampleContext(
            path=(*self._path, key),
        )


class _CustomFunc(t.Protocol):
    def __call__(
        self,
        example: t.Any,
        *,
        custom_func: "_CustomFunc",
        rnd: t.Optional[Random],
        context: FromExampleContext,
    ) -> t.Any:
        ...


def _dict_item(obj, *, _recursive) -> DictItem:
    if isinstance(obj, ranog.DictItemExample):
        return DictItem(_recursive(obj.example), obj.prop_exists)
    else:
        return DictItem(_recursive(obj))


def _list_item(item: t.Tuple[int, t.Any], *, _recursive_child) -> Factory:
    index, obj = item
    return _recursive_child(obj, index)


def from_example(
    example: t.Any,
    *,
    custom_func: t.Optional[_CustomFunc] = None,
    rnd: t.Optional[Random] = None,
    context: t.Optional[FromExampleContext] = None,
) -> Factory:
    """Returns a factory generating value like specified example or type.

    Parameters
    ----------
    example : Any
        the type or the example
    custom_func : Callable
        If specified, this function is executed first and its return value is used as a new example.
        If it returns a factory, it is used as is.
        The same arguments are passed to this function as those passed to from_example.
        It is recommended that `custom_func` receives `**kwargs` to allow for more keyword arguments in future updates.
        This process is also used to create factories for child elements of dict and list.
    rnd : Random, optional
        random number generator to be used
    context : FromExampleContext, optional
        the context of generation. Normally, you should not specify it.

    Raises
    ------
    FactoryConstructionError
        When the specified example or type is not supported.
    """
    if context is None:
        context = FromExampleContext.root()

    def _recursive(child: t.Any) -> Factory:
        return from_example(child, custom_func=custom_func, rnd=rnd, context=context)

    def _recursive_child(child: t.Any, key: t.Any) -> Factory:
        new_context = context.child(
            key=key,
        )
        return from_example(
            child, custom_func=custom_func, rnd=rnd, context=new_context
        )

    if custom_func is not None:
        custom_result = custom_func(
            example, custom_func=custom_func, rnd=rnd, context=context
        )
        if custom_result is not NotImplemented:
            example = custom_result

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
    elif isinstance(example, Decimal):
        return _from_decimal(example, rnd=rnd)
    elif isinstance(example, t.Mapping):
        return randdict(
            {
                k: _dict_item(v, _recursive=lambda exm: _recursive_child(exm, k))
                for k, v in example.items()
            }
        )
    elif isinstance(example, t.Sequence) and not isinstance(example, str):
        if isinstance(example, (tuple, list)):
            _type = type(example)
        else:
            _type = None
        return randlist(
            *map(
                lambda exm: _list_item(exm, _recursive_child=_recursive_child),
                enumerate(example),
            ),
            type=_type,
            rnd=rnd,
        )
    else:
        return _recursive(type(example))


def _from_decimal(example: Decimal, *, rnd: t.Optional[Random]) -> Factory[Decimal]:
    p_inf, n_inf, nan = 0.0, 0.0, 0.0
    decimal_len = None
    if example.is_infinite():
        if example > 0:
            p_inf = 1.0
        else:
            n_inf = 1.0
    elif example.is_nan():
        nan = 1.0
    else:
        decimal_len = -example.as_tuple()[2]
    return randdecimal(
        p_inf=p_inf, n_inf=n_inf, nan=nan, decimal_len=decimal_len, rnd=rnd
    )
