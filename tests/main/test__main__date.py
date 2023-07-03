import datetime
import re
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__date__without_min_max(capfd):
    args = ["randog", "date"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert re.match(r"^\d{4}-\d{2}-\d{2}\n?$", out)
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02", "2020-01-02"),
        ("2020-02-20", "2020-02-20"),
    ],
)
def test__main__date__min_max(capfd, arg, expected):
    args = ["randog", "date", arg, arg]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "minimum",
    ["1", "a", "-"],
)
def test__main__date__error_when_illegal_min(capfd, minimum):
    args = ["randog", "date", minimum, "2020-01-02"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "date: error: argument MINIMUM: invalid date value: " in err


@pytest.mark.parametrize(
    "maximum",
    ["1", "a", "-"],
)
def test__main__date__error_when_illegal_max(capfd, maximum):
    args = ["randog", "date", "2020-01-02", maximum]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "date: error: argument MAXIMUM: invalid date value: " in err


def test__main__date__error_when_max_lt_min(capfd):
    args = ["randog", "date", "2020-01-02", "2020-01-01"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "date: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02", "datetime.date(2020, 1, 2)"),
    ],
)
def test__main__date__option_repr(capfd, arg, expected):
    args = ["randog", "date", arg, arg, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02", '"2020-01-02"'),
    ],
)
def test__main__date__option_json(capfd, arg, expected):
    args = ["randog", "date", arg, arg, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "options", "expected"),
    [
        ("2020-01-02", ["--iso"], "2020-01-02"),
        ("2020-01-02", ["--fmt", "%Y/%m/%d"], "2020/01/02"),
        ("2020-01-03", ["--fmt", "%m/%d/%Y"], "01/03/2020"),
    ],
)
def test__main__date__option_date_fmt(capfd, arg, options, expected):
    args = ["randog", "date", arg, arg, *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02", '"2020-01-02"'),
    ],
)
def test__main__date__option_json_iso(capfd, arg, expected):
    args = ["randog", "date", arg, arg, "--json", "--iso"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02", "2020-01-02"),
    ],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__date__option_repeat(capfd, resources, arg, expected, option, count):
    args = [
        "randog",
        "date",
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
def test__main__date__error_with_negative_repeat(capfd, resources, option, length):
    expected = "2020-01-02"
    args = [
        "randog",
        "date",
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
            f"date: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02", datetime.date(2020, 1, 2)),
    ],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__date__option_list(capfd, resources, arg, expected, option, length):
    args = [
        "randog",
        "date",
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
def test__main__date__error_with_negative_list(capfd, resources, option, length):
    expected = "2020-01-02"
    args = [
        "randog",
        "date",
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
            f"date: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__date__option_output(capfd, tmp_path, resources):
    expected = "2020-01-02"
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "date",
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


def test__main__date__option_output__option_repeat(capfd, tmp_path, resources):
    expected = "2020-01-02"
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "date",
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


def test__main__date__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    expected = "2020-01-02"
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "date",
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
        (["--iso", "--repr"],),
        (["--fmt", "%Y/%m/%d", "--repr"],),
        (["--fmt", "%Y/%m/%d", "--iso"],),
        (["--fmt", "%Y/%m/%d", "--iso", "--repr"],),
    ],
)
def test__main__date__error_duplicate_format(capfd, resources, options):
    args = [
        "randog",
        "date",
        "2020-01-02",
        "2020-01-02",
        *options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


def test__main__date__help(capfd):
    args = ["randog", "date", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: python -m randog date")
        assert err == ""