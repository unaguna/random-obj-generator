import pytest

import ranog.factory
from ranog.exceptions import FactoryConstructionError


@pytest.mark.parametrize("length", (1, 2, 3))
def test__random_list(length):
    factory = ranog.factory.randlist(
        ranog.factory.randint(1, 1), ranog.factory.randstr(length=0), length=length
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
    factory = ranog.factory.randlist(
        ranog.factory.randint(1, 1),
        ranog.factory.randstr(length=0),
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
    factory = ranog.factory.randlist(
        ranog.factory.randint(1, 1), ranog.factory.randstr(length=0)
    )

    for _ in range(100):
        value = factory.next()
        assert value == [1, ""]


def test__random_list__normal_with_no_factory_and_zero_length():
    factory = ranog.factory.randlist(length=0)
    value = factory.next()
    assert value == []


def test__random_list__or_none():
    factory = ranog.factory.randlist(length=0).or_none(0.5)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {list, type(None)}


def test__random_list__or_none_0():
    factory = ranog.factory.randlist(length=0).or_none(0)

    values = set(map(lambda x: type(factory.next()), range(200)))

    assert values == {list}


@pytest.mark.parametrize("length", (1, 2))
def test__random_str__error_with_no_factory_and_nonzero_length(length):
    with pytest.raises(FactoryConstructionError) as e_ctx:
        ranog.factory.randlist(length=length)
    e = e_ctx.value

    assert e.message == "the generating conditions are inconsistent"
