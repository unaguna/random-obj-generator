import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_dict():
    factory = randog.factory.randdict(
        a=randog.factory.randint(1, 1),
        b=(randog.factory.randint(2, 2), 1.0),
        c=(randog.factory.randint(26, 26), 0.0),
    )

    value = factory.next()

    assert isinstance(value, dict)
    assert value.get("a") == 1
    assert value.get("b") == 2
    assert "z" not in value


def test__random_dict__items_by_dict():
    factory = randog.factory.randdict(
        {
            "a": randog.factory.randint(1, 1),
            "b": (randog.factory.randint(2, 2), 1.0),
            "z": (randog.factory.randint(26, 26), 0.0),
        }
    )

    value = factory.next()

    assert isinstance(value, dict)
    assert value.get("a") == 1
    assert value.get("b") == 2
    assert "z" not in value


@pytest.mark.parametrize("as_dict", [True, False])
@pytest.mark.parametrize(
    "items",
    [
        {"a": randog.factory.randint(1, 1), "b": range(0, 10)},
        {"a": randog.factory.randint(1, 1), "b": lambda: None},
        {"a": randog.factory.randint(1, 1), "b": "const"},
    ],
)
def test__random_dict__error_when_item_is_not_factory(as_dict, items):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        if as_dict:
            randog.factory.randdict(items)
        else:
            randog.factory.randdict(**items)
    e = e_ctx.value

    assert e.message.startswith("randdict received non-factory object for item")


def test__random_dict__or_none():
    factory = randog.factory.randdict(
        a=randog.factory.randint(1, 1),
    ).or_none(0.5)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {dict, type(None)}


def test__random_dict__or_none_0():
    factory = randog.factory.randdict(
        a=randog.factory.randint(1, 1),
    ).or_none(0)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {dict}


@pytest.mark.parametrize(
    "args",
    [
        [
            {
                "a": randog.factory.const(1),
                "b": randog.factory.DictItem(randog.factory.const(2), 0.5),
            }
        ],
    ],
)
def test__random_dict__seed(args):
    seed = 12
    rnd1 = random.Random(seed)
    rnd2 = random.Random(seed)
    factory1 = randog.factory.randdict(*args, rnd=rnd1)
    factory2 = randog.factory.randdict(*args, rnd=rnd2)

    generated1 = list(factory1.iter(20))
    generated2 = list(factory2.iter(20))

    assert generated1 == generated2
