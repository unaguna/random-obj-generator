from random import Random
from unittest.mock import MagicMock, DEFAULT

import randog.factory
from randog.factory._from_example import ContextFactory


def test__from_example_context():
    custom_func = lambda *args, **kwargs: randog.factory.const(0)
    rnd = Random()

    context = ContextFactory.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )

    assert len(context.custom_funcs) == 1
    assert context.custom_funcs[0] is custom_func
    assert context.rnd is rnd
    assert context.custom_chain_length == 0
    assert len(context.path) == 0
    assert context.examples == ("example",)
    assert context.current_example == "example"
    assert context.signal_terminate_custom is False


def test__from_example_context__child():
    custom_func = lambda *args, **kwargs: randog.factory.const(0)
    rnd = Random()

    root_context = randog.factory._from_example.ContextFactory.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    assert len(context.custom_funcs) == 1
    assert context.custom_funcs[0] is custom_func
    assert context.rnd is rnd
    assert context.custom_chain_length == 0
    assert len(context.path) == 1
    assert context.path[0] == "key"
    assert context.examples == ("example", "child_example")
    assert context.current_example == "child_example"
    assert context.signal_terminate_custom is False


def test__from_example_context__customized():
    custom_func = lambda *args, **kwargs: randog.factory.const(0)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    assert context.custom_chain_length == 0

    context = ContextFactory.count_up_custom(context)

    assert len(context.custom_funcs) == 1
    assert context.custom_funcs[0] is custom_func
    assert context.rnd is rnd
    assert context.custom_chain_length == 1
    assert len(context.path) == 1
    assert context.path[0] == "key"
    assert context.examples == ("example", "child_example")
    assert context.current_example == "child_example"


def test__from_example_context__customized_by_list():
    custom_func1 = lambda *args, **kwargs: randog.factory.const(1)
    custom_func2 = lambda *args, **kwargs: randog.factory.const(2)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    assert context.custom_chain_length == 0

    context = ContextFactory.count_up_custom(context)

    assert len(context.custom_funcs) == 2
    assert context.custom_funcs[0] is custom_func1
    assert context.custom_funcs[1] is custom_func2
    assert context.rnd is rnd
    assert context.custom_chain_length == 1
    assert len(context.path) == 1
    assert context.path[0] == "key"
    assert context.examples == ("example", "child_example")
    assert context.current_example == "child_example"


def test__from_example_context__from_example():
    expected_example = 1
    expected_factory = randog.factory.ChoiceRandomFactory([2])
    custom_func = MagicMock(return_value=expected_factory)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = context.from_example(expected_example)

    assert result is expected_factory
    custom_func.assert_called_once()
    assert custom_func.call_args.kwargs["context"].path == ("key",)
    assert custom_func.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func.call_args.kwargs["context"].current_example == "child_example"


def test__from_example_context__from_example__multi_custom_func__first_factory():
    expected_example = 1
    expected_factory = randog.factory.ChoiceRandomFactory([2])
    custom_func1 = MagicMock(return_value=expected_factory)
    custom_func2 = MagicMock(return_value=0)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = context.from_example(expected_example)

    assert result is expected_factory
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key",)
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func1.call_args.kwargs["context"].current_example == "child_example"
    custom_func2.assert_not_called()


def test__from_example_context__from_example__multi_custom_func__first_customized_example():
    expected_example = 1
    custom_func1 = MagicMock(
        side_effect=lambda _, *, context, **kwargs: context.terminate_custom_chain()
        or DEFAULT,
        return_value="a",
    )
    custom_func2 = MagicMock(return_value=0)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    ctx = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = ctx.from_example(expected_example)

    assert isinstance(result, randog.factory.StrRandomFactory)
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key",)
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func1.call_args.kwargs["context"].current_example == "child_example"
    custom_func2.assert_not_called()


def test__from_example_context__from_example__multi_custom_func__second_factory():
    expected_example = 1
    expected_factory = randog.factory.ChoiceRandomFactory([2])
    custom_func1 = MagicMock(return_value=NotImplemented)
    custom_func2 = MagicMock(return_value=expected_factory)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = context.from_example(expected_example)

    assert result is expected_factory
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key",)
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func1.call_args.kwargs["context"].current_example == "child_example"
    custom_func2.assert_called_once()
    assert custom_func2.call_args.kwargs["context"].path == ("key",)
    assert custom_func2.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func2.call_args.kwargs["context"].current_example == "child_example"


def test__from_example_context__from_example__multi_custom_func__second_customized_example():
    expected_example = 1
    custom_func1 = MagicMock(return_value=NotImplemented)
    custom_func2 = MagicMock(
        side_effect=lambda _, *, context, **kwargs: context.terminate_custom_chain()
        or DEFAULT,
        return_value="a",
    )
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    ctx = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = ctx.from_example(expected_example)

    assert isinstance(result, randog.factory.StrRandomFactory)
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key",)
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func1.call_args.kwargs["context"].current_example == "child_example"
    custom_func2.assert_called_once()
    assert custom_func2.call_args.kwargs["context"].path == ("key",)
    assert custom_func2.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
    )
    assert custom_func2.call_args.kwargs["context"].current_example == "child_example"


def test__from_example_context__recursive():
    expected_example = 1
    expected_factory = randog.factory.ChoiceRandomFactory([2])
    custom_func = MagicMock(return_value=expected_factory)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=custom_func,
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

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


def test__from_example_context__recursive__multi_custom_func__first_factory():
    expected_example = 1
    expected_factory = randog.factory.ChoiceRandomFactory([2])
    custom_func1 = MagicMock(return_value=expected_factory)
    custom_func2 = MagicMock(return_value=0)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = context.recursive(expected_example, "key2")

    assert result is expected_factory
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key", "key2")
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
        expected_example,
    )
    assert custom_func1.call_args.kwargs["context"].current_example == expected_example
    custom_func2.assert_not_called()


def test__from_example_context__recursive__multi_custom_func__first_customized_example():
    expected_example = 1
    custom_func1 = MagicMock(
        side_effect=lambda _, *, context, **kwargs: context.terminate_custom_chain()
        or DEFAULT,
        return_value="a",
    )
    custom_func2 = MagicMock(return_value=0)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    ctx = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = ctx.recursive(expected_example, "key2")

    assert isinstance(result, randog.factory.StrRandomFactory)
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key", "key2")
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
        expected_example,
    )
    assert custom_func1.call_args.kwargs["context"].current_example == expected_example
    custom_func2.assert_not_called()


def test__from_example_context__recursive__multi_custom_func__second_factory():
    expected_example = 1
    expected_factory = randog.factory.ChoiceRandomFactory([2])
    custom_func1 = MagicMock(return_value=NotImplemented)
    custom_func2 = MagicMock(return_value=expected_factory)
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    context = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = context.recursive(expected_example, "key2")

    assert result is expected_factory
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key", "key2")
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
        expected_example,
    )
    assert custom_func1.call_args.kwargs["context"].current_example == expected_example
    custom_func2.assert_called_once()
    assert custom_func2.call_args.kwargs["context"].path == ("key", "key2")
    assert custom_func2.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
        expected_example,
    )
    assert custom_func2.call_args.kwargs["context"].current_example == expected_example


def test__from_example_context__recursive__multi_custom_func__second_customized_example():
    expected_example = 1
    custom_func1 = MagicMock(return_value=NotImplemented)
    custom_func2 = MagicMock(
        side_effect=lambda _, *, context, **kwargs: context.terminate_custom_chain()
        or DEFAULT,
        return_value="a",
    )
    rnd = Random()

    root_context = ContextFactory.root(
        custom_func=[custom_func1, custom_func2],
        rnd=rnd,
        example="example",
    )
    ctx = ContextFactory.child_of(root_context, key="key", example="child_example")

    result = ctx.recursive(expected_example, "key2")

    assert isinstance(result, randog.factory.StrRandomFactory)
    custom_func1.assert_called_once()
    assert custom_func1.call_args.kwargs["context"].path == ("key", "key2")
    assert custom_func1.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
        expected_example,
    )
    assert custom_func1.call_args.kwargs["context"].current_example == expected_example
    custom_func2.assert_called_once()
    assert custom_func2.call_args.kwargs["context"].path == ("key", "key2")
    assert custom_func2.call_args.kwargs["context"].examples == (
        "example",
        "child_example",
        expected_example,
    )
    assert custom_func2.call_args.kwargs["context"].current_example == expected_example
