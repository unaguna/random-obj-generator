import datetime as dt
from decimal import Decimal
import typing as t
from random import Random

from . import (
    by_callable,
    DictItem,
    Factory,
    randbool,
    randdatetime,
    randdecimal,
    randdict,
    randfloat,
    randlist,
    randint,
    randstr,
    union,
    const,
)
from ..exceptions import FactoryConstructionError

import randog


_FACTORY_CONSTRUCTOR: t.Dict[type, t.Callable[[t.Optional[Random]], Factory]] = {
    bool: lambda rnd: randbool(rnd=rnd),
    int: lambda rnd: randint(0, 100, rnd=rnd),
    float: lambda rnd: randfloat(0, 1.0, rnd=rnd),
    Decimal: lambda rnd: randdecimal(0, 1.0, rnd=rnd),
    str: lambda rnd: randstr(rnd=rnd),
    dt.datetime: lambda rnd: randdatetime(rnd=rnd),
    list: lambda rnd: randlist(randstr(), rnd=rnd),
    tuple: lambda rnd: randlist(randstr(), type=tuple, rnd=rnd),
    dict: lambda rnd: randdict({"key": randint(0, 100, rnd=rnd)}, rnd=rnd),
}


class FromExampleContext:
    _path: t.Tuple[t.Any, ...]
    _custom_func: t.Optional["_CustomFunc"]
    _rnd: t.Optional[Random]
    _example_is_customized: bool
    _examples_stack: t.Tuple[t.Any, ...]

    def __init__(
        self,
        path: t.Tuple[t.Any, ...],
        custom_func: t.Optional["_CustomFunc"],
        rnd: t.Optional[Random],
        example_is_customized: bool,
        examples_stack: t.Tuple[t.Any, ...],
    ):
        self._path = path
        self._custom_func = custom_func
        self._rnd = rnd
        self._example_is_customized = example_is_customized
        self._example_stacks = examples_stack

    @property
    def path(self) -> t.Sequence[t.Any]:
        return self._path

    @property
    def example_is_customized(self) -> bool:
        return self._example_is_customized

    @property
    def rnd(self) -> t.Optional[Random]:
        return self._rnd

    @property
    def custom_func(self) -> t.Optional["_CustomFunc"]:
        return self._custom_func

    @property
    def examples(self) -> t.Tuple[t.Any, ...]:
        return self._example_stacks

    @property
    def current_example(self) -> t.Any:
        if len(self._example_stacks) <= 0:
            return None
        else:
            return self._example_stacks[-1]

    @classmethod
    def root(
        cls,
        custom_func: t.Optional["_CustomFunc"],
        rnd: t.Optional[Random],
        example: t.Any,
    ) -> "FromExampleContext":
        return FromExampleContext(
            path=tuple(),
            custom_func=custom_func,
            rnd=rnd,
            example_is_customized=False,
            examples_stack=(example,),
        )

    def child(
        self,
        key: t.Any,
        example: t.Any,
    ) -> "FromExampleContext":
        return FromExampleContext(
            path=(*self._path, key),
            custom_func=self._custom_func,
            rnd=self._rnd,
            example_is_customized=False,
            examples_stack=(*self._example_stacks, example),
        )

    def customized(self) -> "FromExampleContext":
        return FromExampleContext(
            path=self._path,
            custom_func=self._custom_func,
            rnd=self._rnd,
            example_is_customized=True,
            examples_stack=self._example_stacks,
        )

    def from_example(self, example: t.Any) -> Factory:
        return from_example(
            example,
            custom_func=self._custom_func,
            rnd=self._rnd,
            context=self,
        )

    def recursive(self, child: t.Any, key: t.Any) -> Factory:
        new_context = self.child(
            key=key,
            example=child,
        )
        return from_example(
            child,
            custom_func=self._custom_func,
            rnd=self._rnd,
            context=new_context,
        )


class _CustomFunc(t.Protocol):
    def __call__(
        self,
        example: t.Any,
        *,
        context: FromExampleContext,
    ) -> t.Any:
        ...


def _dict_item(obj, key, context: FromExampleContext) -> DictItem:
    if isinstance(obj, randog.DictItemExample):
        return DictItem(context.recursive(obj.example, key), obj.prop_exists)
    else:
        return DictItem(context.recursive(obj, key))


def _list_item(item: t.Tuple[int, t.Any], context: FromExampleContext) -> Factory:
    index, obj = item
    return context.recursive(obj, index)


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
        The context is passed to this function.
        It is recommended that `custom_func` receives `**kwargs` to allow for more keyword arguments in future updates.
        This process is also used to create factories for child elements of dict and list.
    rnd : Random, optional
        random number generator to be used
    context : FromExampleContext, optional
        the context of generation. Normally, you should not specify it.
        If specified, the context property takes precedence over other arguments.

    Raises
    ------
    FactoryConstructionError
        When the specified example or type is not supported.
    """
    if isinstance(example, Factory):
        return example
    if context is None:
        context = FromExampleContext.root(
            custom_func=custom_func,
            rnd=rnd,
            example=example,
        )

    if not context.example_is_customized and context.custom_func is not None:
        context = context.customized()
        custom_result = context.custom_func(
            example,
            context=context,
        )
        if isinstance(custom_result, Factory):
            return custom_result
        if custom_result is not NotImplemented:
            example = custom_result

    if isinstance(example, randog.Example):
        return union(*map(context.from_example, example), rnd=context.rnd)
    elif isinstance(example, type):
        if example in _FACTORY_CONSTRUCTOR:
            return _FACTORY_CONSTRUCTOR[example](context.rnd)
        else:
            raise FactoryConstructionError(
                f"cannot construct factory for unsupported type: {example}"
            )
    elif example is None:
        return const(None, rnd=context.rnd)
    elif isinstance(example, Decimal):
        return _from_decimal(example, rnd=context.rnd)
    elif isinstance(example, t.Mapping):
        return randdict({k: _dict_item(v, k, context) for k, v in example.items()})
    elif isinstance(example, t.Sequence) and not isinstance(example, str):
        if isinstance(example, (tuple, list)):
            _type = type(example)
        else:
            _type = None
        return randlist(
            type=_type,
            rnd=context.rnd,
            items_list=tuple(_list_item(exm, context) for exm in enumerate(example)),
        )
    elif isinstance(example, t.Callable):
        return by_callable(example)
    else:
        return context.from_example(type(example))


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
