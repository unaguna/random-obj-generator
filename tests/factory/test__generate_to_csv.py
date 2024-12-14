import io
import os
import warnings
from itertools import count

import pytest

import randog
import randog.factory
from randog.exceptions import RandogWarning
from randog.factory import FactoryStopException


@pytest.mark.parametrize(
    ("csv_columns", "expected"),
    [
        (["a", "b"], "1,1\n1,2\n1,3\n"),
        (["b", "a"], "1,1\n2,1\n3,1\n"),
        (["b", lambda d: d["b"] ** 2], "1,1\n2,4\n3,9\n"),
    ],
)
def test__generate_to_csv__with_csv_columns(csv_columns, expected):
    line_num = 3
    factory = randog.factory.randdict(
        a=randog.factory.const(1),
        b=randog.factory.by_iterator(count(1)),
    )

    buffer = io.StringIO()
    with buffer:
        with warnings.catch_warnings():
            # assert no warnings
            warnings.simplefilter("error")

            randog.generate_to_csv(factory, line_num, buffer, csv_columns=csv_columns)
        actual_value = buffer.getvalue()

    assert actual_value == expected.replace("\n", os.linesep)


def test__generate_to_csv__without_csv_columns():
    line_num = 3
    expected = "1,1\n1,2\n1,3\n"
    expected_message = (
        "^Since csv_columns is None, "
        "the fields are inserted in the order returned by the dictionary; "
        "In this case, fields may not be aligned depending on the factory definition, "
        "so it is recommended to specify non-none csv_columns.$"
    )
    factory = randog.factory.randdict(
        a=randog.factory.const(1),
        b=randog.factory.by_iterator(count(1)),
    )

    buffer = io.StringIO()
    with buffer:
        with pytest.warns(RandogWarning, match=expected_message):
            randog.generate_to_csv(factory, line_num, buffer, csv_columns=None)

        actual_value = buffer.getvalue()

    assert actual_value == expected.replace("\n", os.linesep)


@pytest.mark.parametrize(
    ("csv_columns",),
    [
        (["a", "b"],),
        (["b", "a"],),
        (["b", lambda d: d["b"] ** 2],),
    ],
)
def test__generate_to_csv__scalar__with_csv_columns(csv_columns):
    line_num = 3
    expected = "a\na\na\n"
    expected_message = (
        "^CSV output is recommended for only collections "
        r"\(such as dict, list, tuple, etc.\); "
        "In CSV output, one generated value is treated as one row, "
        r"so the result is the same as iteration of 'print\(factory.next\(\)\)'; "
        "csv_columns specified as argument is ignored.$"
    )
    factory = randog.factory.const("a")

    buffer = io.StringIO()
    with buffer:
        with pytest.warns(RandogWarning, match=expected_message):
            randog.generate_to_csv(factory, line_num, buffer, csv_columns=csv_columns)

        actual_value = buffer.getvalue()

    assert actual_value == expected.replace("\n", os.linesep)


def test__generate_to_csv__scalar__without_csv_columns():
    line_num = 3
    expected = "a\na\na\n"
    expected_message = (
        "^CSV output is recommended for only collections "
        r"\(such as dict, list, tuple, etc.\); "
        "In CSV output, one generated value is treated as one row, "
        r"so the result is the same as iteration of 'print\(factory.next\(\)\)'.$"
    )
    factory = randog.factory.const("a")

    buffer = io.StringIO()
    with buffer:
        with pytest.warns(RandogWarning, match=expected_message):
            randog.generate_to_csv(factory, line_num, buffer, csv_columns=None)

        actual_value = buffer.getvalue()

    assert actual_value == expected.replace("\n", os.linesep)


@pytest.mark.parametrize(
    ("line_num", "expected"),
    [
        (3, "1,1\n1,2\n1,3\n"),
        (4, "1,1\n1,2\n1,3\n1,4\n"),
    ],
)
def test__generate_to_csv__line_num(line_num, expected):
    csv_columns = ["a", "b"]
    factory = randog.factory.randdict(
        a=randog.factory.const(1),
        b=randog.factory.by_iterator(count(1)),
    )

    buffer = io.StringIO()
    with buffer:
        with warnings.catch_warnings():
            # assert no warnings
            warnings.simplefilter("error")

            randog.generate_to_csv(factory, line_num, buffer, csv_columns=csv_columns)
        actual_value = buffer.getvalue()

    assert actual_value == expected.replace("\n", os.linesep)


def test__generate_to_csv__with_discard():
    line_num = 3
    csv_columns = ["a", "b"]
    factory = randog.factory.randdict(
        a=randog.factory.const(1),
        b=randog.factory.by_iterator(count(1)),
    )

    buffer = io.StringIO()
    with buffer:
        with warnings.catch_warnings():
            # assert no warnings
            warnings.simplefilter("error")

            randog.generate_to_csv(
                factory, line_num, buffer, csv_columns=csv_columns, discard=1.0
            )
        actual_value = buffer.getvalue()

    # assert that all rows are discarded
    assert actual_value == ""


def test__generate_to_csv__with_regenerate():
    line_num = 1
    csv_columns = ["a", "b"]

    def b_iter():
        yield 1
        while True:
            yield 2

    factory = randog.factory.randdict(
        a=randog.factory.const(1),
        b=randog.factory.by_iterator(b_iter()),
    )

    buffer = io.StringIO()
    with buffer:
        with warnings.catch_warnings():
            # assert no warnings
            warnings.simplefilter("error")

            randog.generate_to_csv(
                factory, line_num, buffer, csv_columns=csv_columns, regenerate=0.999
            )
        actual_value = buffer.getvalue()

    # assert that it discards first row "1,1" and regenerates row
    assert actual_value == "1,2\n".replace("\n", os.linesep)


def test__generate_to_csv__with_raise_on_factory_stopped():
    line_num = 3
    csv_columns = ["a", "b"]
    factory = randog.factory.randdict(
        a=randog.factory.const(1),
        # limited iterator
        b=randog.factory.by_iterator(iter(range(1, 3))),
    )

    buffer = io.StringIO()
    with buffer:
        with pytest.raises(FactoryStopException):
            with warnings.catch_warnings():
                # assert no warnings
                warnings.simplefilter("error")

                randog.generate_to_csv(
                    factory,
                    line_num,
                    buffer,
                    csv_columns=csv_columns,
                    raise_on_factory_stopped=True,
                )
        actual_value = buffer.getvalue()

    # assert that it outputs rows to the middle
    assert actual_value == "1,1\n1,2\n".replace("\n", os.linesep)


@pytest.mark.parametrize(
    ("linesep", "expected"),
    [
        (";", "1,1;1,2;1,3;"),
        ("\0", "1,1\x001,2\x001,3\x00"),
    ],
)
def test__generate_to_csv__with_linesep(linesep, expected):
    line_num = 3
    csv_columns = ["a", "b"]
    factory = randog.factory.randdict(
        a=randog.factory.const(1),
        b=randog.factory.by_iterator(count(1)),
    )

    buffer = io.StringIO()
    with buffer:
        with warnings.catch_warnings():
            # assert no warnings
            warnings.simplefilter("error")

            randog.generate_to_csv(
                factory,
                line_num,
                buffer,
                csv_columns=csv_columns,
                linesep=linesep,
            )
        actual_value = buffer.getvalue()

    assert actual_value == expected
