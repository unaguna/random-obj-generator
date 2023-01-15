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


def test__from_example__list_type():
    factory = ranog.factory.from_example(list)
    value = factory.next()
    assert isinstance(value, list)


def test__from_example__tuple_type():
    factory = ranog.factory.from_example(tuple)
    value = factory.next()
    assert isinstance(value, tuple)


def test__from_example__dict_type():
    factory = ranog.factory.from_example(dict)
    value = factory.next()
    assert isinstance(value, dict)


def test__from_example__dict_value():
    example = {
        "a": str,
        "b": -1000,
        "c": {"cc": 1},
        "d": ranog.DictItemExample(str, 1.0),
        "e": ranog.DictItemExample(int),
        "f": ranog.Example(1, str),
        "g": ranog.DictItemExample(ranog.Example(1, str)),
        "h": ranog.factory.randint(5, 5),
        "i": ranog.DictItemExample(ranog.factory.randint(5, 5)),
        "z": ranog.DictItemExample(int, 0.0),
    }
    factory = ranog.factory.from_example(example)
    value = factory.next()

    assert isinstance(value, dict)
    assert isinstance(value.get("a"), str)
    assert isinstance(value.get("b"), int) and value.get("b") != -1000
    assert isinstance(value.get("c"), dict) and isinstance(
        value.get("c").get("cc"), int
    )
    assert isinstance(value.get("d"), str)
    assert isinstance(value.get("e"), int)
    assert isinstance(value.get("f"), (int, str))
    assert isinstance(value.get("g"), (int, str))
    assert value.get("h") == 5
    assert value.get("i") == 5
    assert "z" not in value


@pytest.mark.parametrize(
    "input_factory",
    (
        ranog.factory.randint(1, 1),
        ranog.factory.randstr(),
    ),
)
def test__from_example__factory(input_factory):
    factory = ranog.factory.from_example(input_factory)
    assert factory is input_factory


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
