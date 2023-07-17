import datetime as dt
import re
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__time__without_min_max(capfd):
    args = ["randog", "time"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert re.match(r"^\d{2}:\d{2}:\d{2}(\.\d+)?\n?$", out)
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("03:04:05", "03:04:05"),
        ("03:04", "03:04:00"),
        ("03:04:05.600000", "03:04:05.600000"),
    ],
)
def test__main__time__min_max(capfd, arg, expected):
    args = ["randog", "time", arg, arg]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("minimum", "maximum", "expected_condition"),
    [
        ("10:00:00", "11:00:00", lambda v: dt.time(10) <= v <= dt.time(11)),
        ("13:00:00", "13:00:01", lambda v: dt.time(13, 0, 0) <= v <= dt.time(13, 0, 1)),
        ("11:00:00", "10:00:00", lambda v: v <= dt.time(10) or dt.time(11) <= v),
    ],
)
def test__main__time__min_max__range(capfd, minimum, maximum, expected_condition):
    args = ["randog", "time", minimum, maximum]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert expected_condition(dt.time.fromisoformat(out.strip()))
        assert err == ""


@pytest.mark.parametrize(
    "minimum",
    ["1", "a", "-"],
)
def test__main__time__error_when_illegal_min(capfd, minimum):
    args = ["randog", "time", minimum, "03:04:05"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "time: error: argument MINIMUM: invalid time value: " in err


@pytest.mark.parametrize(
    "maximum",
    ["1", "a", "-"],
)
def test__main__time__error_when_illegal_max(capfd, maximum):
    args = ["randog", "time", "03:04:05", maximum]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "time: error: argument MAXIMUM: invalid time value: " in err


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("03:04:05", "datetime.time(3, 4, 5)"),
        ("00:00", "datetime.time(0, 0)"),
    ],
)
def test__main__time__option_repr(capfd, arg, expected):
    args = ["randog", "time", arg, arg, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("03:04:05", '"03:04:05"'),
        ("00:00", '"00:00:00"'),
    ],
)
def test__main__time__option_json(capfd, arg, expected):
    args = ["randog", "time", arg, arg, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "options", "expected"),
    [
        ("03:04:05", ["--iso"], "03:04:05"),
        ("00:00", ["--iso"], "00:00:00"),
        ("03:04:05", ["--fmt", "%H:%M:%S"], "03:04:05"),
        ("03:04:05", ["--fmt", "%H:%M:%S.%f"], "03:04:05.000000"),
    ],
)
def test__main__time__option_time_fmt(capfd, arg, options, expected):
    args = ["randog", "time", arg, arg, *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("03:04:05", '"03:04:05"'),
        ("00:00:00", '"00:00:00"'),
    ],
)
def test__main__time__option_json_iso(capfd, arg, expected):
    args = ["randog", "time", arg, arg, "--json", "--iso"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("03:04:05", "03:04:05"),
        ("00:00", "00:00:00"),
    ],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__time__option_repeat(capfd, resources, arg, expected, option, count):
    args = [
        "randog",
        "time",
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
def test__main__time__error_with_negative_repeat(capfd, resources, option, length):
    expected = "03:04:05"
    args = [
        "randog",
        "time",
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
            f"time: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("03:04:05", dt.time(3, 4, 5)),
        ("00:00", dt.time(0, 0)),
    ],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__time__option_list(capfd, resources, arg, expected, option, length):
    args = [
        "randog",
        "time",
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
def test__main__time__error_with_negative_list(capfd, resources, option, length):
    expected = "03:04:05"
    args = [
        "randog",
        "time",
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
            f"time: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__time__option_output(capfd, tmp_path, resources):
    expected = "03:04:05"
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "time",
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


def test__main__time__option_output__option_repeat(capfd, tmp_path, resources):
    expected = "03:04:05"
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "time",
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


def test__main__time__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    expected = "03:04:05"
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "time",
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
def test__main__time__error_duplicate_format(capfd, resources, options):
    args = [
        "randog",
        "time",
        "03:04:05",
        "03:04:05",
        *options,
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


def test__main__time__help(capfd):
    args = ["randog", "time", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: python -m randog time")
        assert err == ""
