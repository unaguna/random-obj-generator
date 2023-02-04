from random import Random
from unittest.mock import MagicMock

import ranog.factory


def test__from_example_context():
    custom_func = lambda *args, **kwargs: ranog.factory.const(0)
    rnd = Random()

    context = ranog.factory.FromExampleContext.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )

    assert context.custom_func is custom_func
    assert context.rnd is rnd
    assert context.example_is_customized is False
    assert len(context.path) == 0
    assert context.examples == ("example",)
    assert context.current_example == "example"


def test__from_example_context__child():
    custom_func = lambda *args, **kwargs: ranog.factory.const(0)
    rnd = Random()

    root_context = ranog.factory.FromExampleContext.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = root_context.child("key", example="child_example")

    assert context.custom_func is custom_func
    assert context.rnd is rnd
    assert context.example_is_customized is False
    assert len(context.path) == 1
    assert context.path[0] == "key"
    assert context.examples == ("example", "child_example")
    assert context.current_example == "child_example"


def test__from_example_context__customized():
    custom_func = lambda *args, **kwargs: ranog.factory.const(0)
    rnd = Random()

    root_context = ranog.factory.FromExampleContext.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = root_context.child("key", example="child_example")

    assert context.example_is_customized is False

    context = context.customized()

    assert context.custom_func is custom_func
    assert context.rnd is rnd
    assert context.example_is_customized is True
    assert len(context.path) == 1
    assert context.path[0] == "key"
    assert context.examples == ("example", "child_example")
    assert context.current_example == "child_example"


def test__from_example_context__from_example():
    expected_example = 1
    expected_factory = ranog.factory.ChoiceRandomFactory([2])
    custom_func = MagicMock(return_value=expected_factory)
    rnd = Random()

    root_context = ranog.factory.FromExampleContext.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = root_context.child("key", example="child_example")

    result = context.from_example(expected_example)

    assert result is expected_factory
    custom_func.assert_called_once()
    assert custom_func.call_args.kwargs["context"].path == ("key",)
    assert custom_func.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func.call_args.kwargs["context"].current_example == "child_example"


def test__from_example_context__recursive():
    expected_example = 1
    expected_factory = ranog.factory.ChoiceRandomFactory([2])
    custom_func = MagicMock(return_value=expected_factory)
    rnd = Random()

    root_context = ranog.factory.FromExampleContext.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = root_context.child("key", "child_example")

    result = context.recursive(expected_example, "key2")

    assert result is expected_factory
    custom_func.assert_called_once()
    assert custom_func.call_args.kwargs["context"].path == ("key", "key2")
    assert custom_func.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
        expected_example,
    )
    assert custom_func.call_args.kwargs["context"].current_example == expected_example
