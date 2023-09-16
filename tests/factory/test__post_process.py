import pytest

import randog.factory


def test__post_process():
    factory = randog.factory.randint(10, 10).post_process(lambda x: str(x))
    generated = factory.next()

    assert generated == "10"


def test__post_process__none():
    factory = randog.factory.randint(10, 10).post_process(lambda x: str(x)).or_none(1.0)
    generated = factory.next()

    assert generated is None


def test__post_process__none2():
    factory = randog.factory.randint(10, 10).or_none(1.0).post_process(lambda x: str(x))
    generated = factory.next()

    assert generated == "None"


@pytest.mark.parametrize(
    ("default_process", "processes", "expected"),
    [
        # without default
        ([], {"key0": lambda x: f"P{x}"}, {"key0": "P0", "key1": 1, "key2": 2}),
        ([None], {"key0": lambda x: f"P{x}"}, {"key0": "P0", "key1": 1, "key2": 2}),
        (
            [],
            {"key0": lambda x: f"P{x}", "key1": lambda x: f"@{x}"},
            {"key0": "P0", "key1": "@1", "key2": 2},
        ),
        (
            [],
            {"key0": lambda x: f"P{x}", "keyX": lambda x: f"@{x}"},
            {"key0": "P0", "key1": 1, "key2": 2},
        ),
        # with default
        (
            [lambda x: f"p{x}"],
            {"key0": lambda x: f"P{x}"},
            {"key0": "P0", "key1": "p1", "key2": "p2"},
        ),
        (
            [lambda x: f"p{x}"],
            {"key0": lambda x: f"P{x}", "key1": lambda x: f"@{x}"},
            {"key0": "P0", "key1": "@1", "key2": "p2"},
        ),
    ],
)
def test__post_process_items(default_process, processes, expected):
    factory = randog.factory.randdict(
        key0=randog.factory.const(0),
        key1=randog.factory.const(1),
        key2=randog.factory.const(2),
    ).post_process_items(
        *default_process,
        **processes,
    )

    generated = factory.next()

    assert generated == expected


@pytest.mark.parametrize(
    ("default_process", "processes"),
    [
        # without default
        ([], {"key0": lambda x: f"P{x}"}),
        ([None], {"key0": lambda x: f"P{x}"}),
        # with default
        ([lambda x: f"p{x}"], {"key0": lambda x: f"P{x}"}),
    ],
)
@pytest.mark.parametrize("expected", [None, True, 1, "a", [1]])
def test__post_process_items__non_dict(default_process, processes, expected):
    factory = randog.factory.const(expected).post_process_items(
        *default_process, **processes
    )

    generated = factory.next()

    assert generated == expected
