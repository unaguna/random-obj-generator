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

    assert e.message == "the generating conditions are inconsistent"


@pytest.mark.parametrize("length", (0, 1, 2, 3))
def test__random_list__error_when_no_factory_and_random_length(length):
    length_factory = randog.factory.randint(length, length)
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randlist(length=length_factory)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
