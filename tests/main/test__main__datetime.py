import datetime
import re
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__datetime__without_min_max(capfd):
    args = ["randog", "datetime"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?\n?$", out)
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02T03:04:05", "2020-01-02 03:04:05"),
        ("2020-01-02 03:04:05", "2020-01-02 03:04:05"),
        ("2020-01-02", "2020-01-02 00:00:00"),
    ],
)
def test__main__datetime__min_max(capfd, arg, expected):
    args = ["randog", "datetime", arg, arg]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "minimum",
    ["1", "a", "-"],
)
def test__main__datetime__error_when_illegal_min(capfd, minimum):
    args = ["randog", "datetime", minimum, "2020-01-02T03:04:05"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "datetime: error: argument MINIMUM: invalid datetime value: " in err


@pytest.mark.parametrize(
    "maximum",
    ["1", "a", "-"],
)
def test__main__datetime__error_when_illegal_max(capfd, maximum):
    args = ["randog", "datetime", "2020-01-02T03:04:05", maximum]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "datetime: error: argument MAXIMUM: invalid datetime value: " in err


def test__main__datetime__error_when_max_lt_min(capfd):
    args = ["randog", "datetime", "2020-01-02T03:04:06", "2020-01-02T03:04:05"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "datetime: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02T03:04:05", "datetime.datetime(2020, 1, 2, 3, 4, 5)"),
        ("2020-01-02T00:00:00", "datetime.datetime(2020, 1, 2, 0, 0)"),
    ],
)
def test__main__datetime__option_repr(capfd, arg, expected):
    args = ["randog", "datetime", arg, arg, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02T03:04:05", '"2020-01-02 03:04:05"'),
        ("2020-01-02T00:00:00", '"2020-01-02 00:00:00"'),
    ],
)
def test__main__datetime__option_json(capfd, arg, expected):
    args = ["randog", "datetime", arg, arg, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02T03:04:05", "2020-01-02 03:04:05"),
        ("2020-01-02T00:00:00", "2020-01-02 00:00:00"),
    ],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__datetime__option_repeat(capfd, resources, arg, expected, option, count):
    args = [
        "randog",
        "datetime",
        arg,
        arg,
        option,
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__datetime__error_with_negative_repeat(capfd, resources, option, length):
    expected = "2020-01-02T03:04:05"
    args = [
        "randog",
        "datetime",
        expected,
        expected,
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            f"datetime: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02T03:04:05", datetime.datetime(2020, 1, 2, 3, 4, 5)),
        ("2020-01-02T00:00:00", datetime.datetime(2020, 1, 2)),
    ],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__datetime__option_list(capfd, resources, arg, expected, option, length):
    args = [
        "randog",
        "datetime",
        arg,
        arg,
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str([expected] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__datetime__error_with_negative_list(capfd, resources, option, length):
    expected = "2020-01-02T03:04:05"
    args = [
        "randog",
        "datetime",
        str(expected),
        str(expected),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            f"datetime: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__datetime__option_output(capfd, tmp_path, resources):
    expected = "2020-01-02 03:04:05"
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "datetime",
        expected,
        expected,
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == f"{expected}\n"
            assert out_fp.readline() == ""


def test__main__datetime__option_output__option_repeat(capfd, tmp_path, resources):
    expected = "2020-01-02 03:04:05"
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "datetime",
        expected,
        expected,
        "--output",
        str(output_path),
        "--repeat",
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            for _ in range(count):
                assert out_fp.readline() == f"{expected}\n"
            assert out_fp.readline() == ""


def test__main__datetime__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    expected = "2020-01-02 03:04:05"
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "datetime",
        expected,
        expected,
        "--output",
        str(output_fmt_path),
        "--repeat",
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        for i in range(count):
            with open(output_paths[i], mode="r") as out_fp:
                assert out_fp.readline() == f"{expected}\n"
                assert out_fp.readline() == ""


@pytest.mark.parametrize(
    ("options",),
    [
        (["--json", "--repr"],),
    ],
)
def test__main__datetime__error_duplicate_format(capfd, resources, options):
    args = [
        "randog",
        "datetime",
        "2020-01-02T03:04:05",
        "2020-01-02T03:04:05",
        *options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err
