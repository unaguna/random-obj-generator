import enum
import random

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


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        ([MyEnum], {}),
        (
            [MyEnum],
            {"weights": lambda x: x.value / sum(map(lambda y: y.value, MyEnum))},
        ),
    ],
)
def test__random_enum__seed(rnd1, rnd2, expect_same_output, args, kwargs):
    repeat = 100
    factory1 = randog.factory.randenum(*args, **rnd1(), **kwargs)
    factory2 = randog.factory.randenum(*args, **rnd2(), **kwargs)

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
