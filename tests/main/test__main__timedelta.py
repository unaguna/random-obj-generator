import datetime
import re
import sys
from unittest.mock import patch

import pytest

import randog.__main__
from randog import timedelta_util


def test__main__timedelta__without_min_max(capfd):
    args = ["randog", "timedelta"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert re.match(
            r"(?:\d+d)?(?:\d+h)?(?:\d+m)?(?:\d+s)?(?:\d+ms)?(?:\d+us)?\n", out
        )
        assert err == ""


@pytest.mark.parametrize(
    "expected",
    ["1d", "20h", "1h30m"],
)
def test__main__timedelta__min_max(capfd, expected):
    args = ["randog", "timedelta", str(expected), str(expected)]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "minimum",
    ["0.1", "a", "-"],
)
def test__main__timedelta__error_when_illegal_min(capfd, minimum):
    args = ["randog", "timedelta", minimum, "1d"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "timedelta: error: argument MINIMUM: invalid timedelta value: " in err


@pytest.mark.parametrize(
    "maximum",
    ["0.1", "a", "-"],
)
def test__main__timedelta__error_when_illegal_max(capfd, maximum):
    args = ["randog", "timedelta", "1d", maximum]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "timedelta: error: argument MAXIMUM: invalid timedelta value: " in err


def test__main__timedelta__error_when_max_lt_min(capfd):
    args = ["randog", "timedelta", "1h", "59m"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "timedelta: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("unit", "minimum", "maximum", "unit_expected"),
    [
        ("1d", "0s", "10d", datetime.timedelta(days=1)),
        ("12h", "0s", "10d", datetime.timedelta(hours=12)),
        ("1s", "0s", "10d", datetime.timedelta(seconds=1)),
        ("10s", "21s", "31s", datetime.timedelta(seconds=10)),
    ],
)
def test__main__timedelta__unit(capfd, unit, minimum, maximum, unit_expected):
    args = ["randog", "timedelta", minimum, maximum, "--unit", unit]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert timedelta_util.from_str(
            out.strip()
        ) % unit_expected == datetime.timedelta(0)
        assert err == ""


@pytest.mark.parametrize(
    "unit",
    ["0.1", "a", "-", '"-1s"', "0s"],
)
def test__main__timedelta__error_when_illegal_unit(capfd, unit):
    args = ["randog", "timedelta", "--unit", unit]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "timedelta: error: argument --unit: invalid positive_timedelta value: "
            in err
        )


@pytest.mark.parametrize(
    ("unit", "minimum", "maximum"),
    [
        ("1d", "1s", "10s"),
        ("1h", "1s", "10s"),
    ],
)
def test__main__timedelta__error_unit_unfit_to_min_max(capfd, unit, minimum, maximum):
    args = ["randog", "timedelta", minimum, maximum, "--unit", unit]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "timedelta: error: argument --unit: there is no multiple of the unit value between MINIMUM and MAXIMUM"
            in err
        )


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("1d", "datetime.timedelta(days=1)"),
        ("1h20m", "datetime.timedelta(seconds=4800)"),
        ("20d1h20m", "datetime.timedelta(days=20, seconds=4800)"),
        ("1s20ms", "datetime.timedelta(seconds=1, microseconds=20000)"),
        ("1s20ms500us", "datetime.timedelta(seconds=1, microseconds=20500)"),
    ],
)
def test__main__timedelta__option_repr(capfd, arg, expected):
    args = ["randog", "timedelta", arg, arg, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("1d", '"1d"'),
        ("1h20m", '"1h20m"'),
        ("20d1h20m", '"20d1h20m"'),
        ("1s20ms", '"1s20ms"'),
        ("1s20ms500us", '"1s20ms500us"'),
    ],
)
def test__main__timedelta__option_json(capfd, arg, expected):
    args = ["randog", "timedelta", arg, arg, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "options", "expected"),
    [
        ("1h20m", ["--iso"], "PT1H20M"),
        ("1d1h20m", ["--iso"], "P1DT1H20M"),
        ("1h20m", ["--fmt", "%H:%M:%S"], "01:20:00"),
        ("10d1h20m", ["--fmt", "%tH:%M:%S"], "241:20:00"),
        ("10d1h20m", ["--fmt", "%D %H:%M:%S"], "10 01:20:00"),
        ("1h20m40ms", ["--fmt", "%H:%M:%S.%f"], "01:20:00.040000"),
        ("1h20m", ["--iso", "--json"], '"PT1H20M"'),
        ("10d1h20m", ["--fmt", "%tH:%M:%S", "--json"], '"241:20:00"'),
    ],
)
def test__main__timedelta__option_datetime_fmt(capfd, arg, options, expected):
    args = ["randog", "timedelta", arg, arg, *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "expected",
    ["1d", "20h", "1h30m"],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__timedelta__option_repeat(capfd, resources, expected, option, count):
    args = [
        "randog",
        "timedelta",
        str(expected),
        str(expected),
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
def test__main__timedelta__error_with_negative_repeat(capfd, resources, option, length):
    expected = "1h"
    args = [
        "randog",
        "timedelta",
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
            f"timedelta: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("1d", datetime.timedelta(days=1)),
        ("20h", datetime.timedelta(hours=20)),
        ("1h30m", datetime.timedelta(hours=1, minutes=30)),
    ],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__timedelta__option_list(capfd, resources, arg, expected, option, length):
    args = [
        "randog",
        "timedelta",
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
def test__main__timedelta__error_with_negative_list(capfd, resources, option, length):
    expected = "1h"
    args = [
        "randog",
        "timedelta",
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
            f"timedelta: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__timedelta__option_output(capfd, tmp_path, resources):
    expected = "1h"
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "timedelta",
        str(expected),
        str(expected),
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


def test__main__timedelta__option_output__option_repeat(capfd, tmp_path, resources):
    expected = "1h20m"
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "timedelta",
        str(expected),
        str(expected),
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


def test__main__timedelta__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    expected = "1h20m"
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "timedelta",
        str(expected),
        str(expected),
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
        (["--fmt", "%tH:%M:%S", "--repr"],),
        (["--fmt", "%tH:%M:%S", "--iso"],),
        (["--fmt", "%tH:%M:%S", "--iso", "--repr"],),
    ],
)
def test__main__timedelta__error_duplicate_format(capfd, resources, options):
    args = ["randog", "timedelta", "1d", "1d", *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


def test__main__timedelta__help(capfd):
    args = ["randog", "timedelta", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: python -m randog timedelta")
        assert err == ""
