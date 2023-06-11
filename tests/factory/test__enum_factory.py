import enum

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3


def test__random_enum__uses_each_value():
    factory = randog.factory.randenum(MyEnum)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {MyEnum.one, MyEnum.two, MyEnum.three}


def test__random_enum__one_value():
    class LocalEnum(enum.Enum):
        single = "s"

    factory = randog.factory.randenum(LocalEnum)

    value = factory.next()

    assert value == LocalEnum.single


def test__random_enum__weights():
    def weights(value):
        if value == MyEnum.one:
            return 0.8
        elif value == MyEnum.two:
            return 0.2
        else:
            return 0

    factory = randog.factory.randenum(MyEnum, weights=weights)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {MyEnum.one, MyEnum.two}


def test__random_enum__or_none():
    factory = randog.factory.randenum(MyEnum).or_none(0.5)

    values = set(map(lambda x: factory.next(), range(400)))

    assert values == {MyEnum.one, MyEnum.two, MyEnum.three, None}


def test__random_enum__or_none_0():
    factory = randog.factory.randenum(MyEnum).or_none(0)

    values = set(map(lambda x: factory.next(), range(200)))

    assert values == {MyEnum.one, MyEnum.two, MyEnum.three}


@pytest.mark.parametrize("dummy_value", (None, NotImplemented, "1", False, True))
def test__random_enum__error_when_weights_does_not_match(dummy_value):
    def weights(value):
        if value == MyEnum.one:
            return 0.8
        elif value == MyEnum.two:
            return 0.2
        elif value == MyEnum.three:
            return dummy_value
        else:
            return 0

    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randenum(
            MyEnum,
            weights=weights,
        )
    e = e_ctx.value

    assert e.message == "the weights must serve weight for each enum value"
