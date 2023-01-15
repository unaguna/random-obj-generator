import pytest

import ranog
import ranog.factory
from ranog.exceptions import FactoryConstructionError


def test__from_example__int_type():
    factory = ranog.factory.from_example(int)
    value = factory.next()
    assert isinstance(value, int)


@pytest.mark.parametrize("obj", (-1, 0, 1))
def test__from_example__int_value(obj):
    factory = ranog.factory.from_example(obj)
    value = factory.next()
    assert isinstance(value, int)


def test__from_example__str_type():
    factory = ranog.factory.from_example(str)
    value = factory.next()
    assert isinstance(value, str)


@pytest.mark.parametrize("obj", ("a", "bc", "xyz"))
def test__from_example__str_value(obj):
    factory = ranog.factory.from_example(obj)
    value = factory.next()
    assert isinstance(value, str)


def test__from_example__dict_type():
    factory = ranog.factory.from_example(dict)
    value = factory.next()
    assert isinstance(value, dict)


@pytest.mark.parametrize("obj", (type, pytest.mark))
def test__from_example__error_when_unsupported_obj(obj):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.from_example(obj)
    e = e_ctx.value

    assert e.message.startswith("cannot construct factory for unsupported type: ")


def test__from_example__union_type():
    factory = ranog.factory.from_example(ranog.Example(int, str))
    values = set(map(lambda x: factory.next(), range(200)))
    value_types = set(map(type, values))
    assert value_types == {int, str}
