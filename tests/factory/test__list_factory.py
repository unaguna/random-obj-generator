import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("length", (1, 2, 3))
def test__random_list(length):
    factory = randog.factory.randlist(
        randog.factory.randint(1, 1), randog.factory.randstr(length=0), length=length
    )

    # generator の実装の正しさの検証のため2回実行する
    for _ in range(2):
        value = factory.next()

        assert type(value) == list
        assert len(value) == length
        if length >= 1:
            assert value[0] == 1
        if length >= 2:
            assert value[1] == ""
        if length >= 3:
            assert value[2] == ""


@pytest.mark.parametrize("as_list", [True, False])
@pytest.mark.parametrize(
    "items",
    [
        [randog.factory.randint(1, 1), range(0, 10)],
        [randog.factory.randint(1, 1), lambda: None],
        [randog.factory.randint(1, 1), "const"],
    ],
)
def test__random_list__error_when_item_is_not_factory(as_list, items):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        if as_list:
            randog.factory.randlist(items_list=items)
        else:
            randog.factory.randlist(*items)
    e = e_ctx.value

    assert e.message.startswith("randlist received non-factory object for item")


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_list__with_random_length(length):
    length_factory = randog.factory.randint(length, length)
    factory = randog.factory.randlist(
        randog.factory.randint(1, 1),
        randog.factory.randstr(length=0),
        length=length_factory,
    )

    # generator の実装の正しさの検証のため2回実行する
    for _ in range(2):
        value = factory.next()

        assert type(value) == list
        assert len(value) == length
        if length >= 1:
            assert value[0] == 1
        if length >= 2:
            assert value[1] == ""
        if length >= 3:
            assert value[2] == ""


@pytest.mark.parametrize("length", (1, 2, 3))
def test__random_list__with_type(length):
    factory = randog.factory.randlist(
        randog.factory.randint(1, 1),
        randog.factory.randstr(length=0),
        length=length,
        type=tuple,
    )

    # generator の実装の正しさの検証のため2回実行する
    for _ in range(2):
        value = factory.next()

        assert type(value) == tuple
        assert len(value) == length
        if length >= 1:
            assert value[0] == 1
        if length >= 2:
            assert value[1] == ""
        if length >= 3:
            assert value[2] == ""


def test__random_list__without_length():
    factory = randog.factory.randlist(
        randog.factory.randint(1, 1), randog.factory.randstr(length=0)
    )

    for _ in range(100):
        value = factory.next()
        assert value == [1, ""]


def test__random_list__normal_with_no_factory_and_zero_length():
    factory = randog.factory.randlist(length=0)
    value = factory.next()
    assert value == []


def test__random_list__or_none():
    factory = randog.factory.randlist(length=0).or_none(0.5)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {list, type(None)}


def test__random_list__or_none_0():
    factory = randog.factory.randlist(length=0).or_none(0)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {list}


@pytest.mark.parametrize("length", (1, 2))
def test__random_list__error_with_no_factory_and_nonzero_length(length):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randlist(length=length)
    e = e_ctx.value

    assert (
        e.message
        == "the factory of element must be given to randlist() if length is positive"
    )


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_list__error_when_no_factory_and_random_length(length):
    length_factory = randog.factory.randint(length, length)
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randlist(length=length_factory)
    e = e_ctx.value

    assert (
        e.message
        == "the factory of element must be given to randlist() if length is at random"
    )


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
    ("args", "substantial_constant"),
    [
        ([randog.factory.const(0), randog.factory.const("a")], True),
    ],
)
def test__random_list__seed(rnd1, rnd2, expect_same_output, args, substantial_constant):
    repeat = 20
    factory1 = randog.factory.randlist(*args, **rnd1())
    factory2 = randog.factory.randlist(*args, **rnd2())

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if substantial_constant or expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
