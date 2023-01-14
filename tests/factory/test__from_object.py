import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


def test__from_object__int_type():
    factory = ranog.factory.from_object(int)
    value = factory.next()
    assert isinstance(value, int)


@pytest.mark.parametrize("obj", (-1, 0, 1))
def test__from_object__int_value(obj):
    factory = ranog.factory.from_object(obj)
    value = factory.next()
    assert isinstance(value, int)


def test__from_object__str_type():
    factory = ranog.factory.from_object(str)
    value = factory.next()
    assert isinstance(value, str)


@pytest.mark.parametrize("obj", ("a", "bc", "xyz"))
def test__from_object__str_value(obj):
    factory = ranog.factory.from_object(obj)
    value = factory.next()
    assert isinstance(value, str)


@pytest.mark.parametrize("obj", (type, pytest.mark))
def test__from_object__error_when_unsupported_obj(obj):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.from_object(obj)
    e = e_ctx.value

    assert e.message.startswith("cannot construct factory for unsupported type: ")
