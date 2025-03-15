import filecmp
from datetime import datetime, timedelta
import re
import sys
from unittest import mock
from unittest.mock import patch

import pytest

import randog.__main__
from randog import timedelta_util
from tests.testtools.trickobj import AnyObject


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
    [
        "1",
        "a",
        "-",
        "2020-01-02T03:04:05+a",
        "now1h",
        "2h",
        "now0",
        "0",
    ],
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
    [
        "1",
        "a",
        "-",
        "2020-01-02T03:04:05+a",
        "now1h",
        "2h",
        "now0",
        "0",
    ],
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
    ("arg", "options", "expected"),
    [
        ("2020-01-02T03:04:05", ["--iso"], "2020-01-02T03:04:05"),
        ("2020-01-02T00:00:00", ["--iso"], "2020-01-02T00:00:00"),
        ("2020-01-02T03:04:05", ["--fmt", "%Y/%m/%d %H:%M:%S"], "2020/01/02 03:04:05"),
        (
            "2020-01-02T03:04:05",
            ["--fmt", "%Y/%m/%d %H:%M:%S.%f"],
            "2020/01/02 03:04:05.000000",
        ),
        ("2020-01-02T03:04:05", ["--fmt", "%m/%d/%Y"], "01/02/2020"),
        # with --list
        (
            "2020-01-02T03:04:05",
            ["--list=2", "--iso"],
            "['2020-01-02T03:04:05', '2020-01-02T03:04:05']",
        ),
        (
            "2020-01-02T03:04:05",
            ["--list=1", "--fmt", "%Y/%m/%d %H:%M:%S"],
            "['2020/01/02 03:04:05']",
        ),
        # with --list and --json
        (
            "2020-01-02T03:04:05",
            ["--list=2", "--json", "--iso"],
            '["2020-01-02T03:04:05", "2020-01-02T03:04:05"]',
        ),
        (
            "2020-01-02T03:04:05",
            ["--list=1", "--json", "--fmt", "%Y/%m/%d %H:%M:%S"],
            '["2020/01/02 03:04:05"]',
        ),
    ],
)
def test__main__datetime__option_datetime_fmt(capfd, arg, options, expected):
    args = ["randog", "datetime", arg, arg, *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02T03:04:05", '"2020-01-02T03:04:05"'),
        ("2020-01-02T00:00:00", '"2020-01-02T00:00:00"'),
    ],
)
def test__main__datetime__option_json_iso(capfd, arg, expected):
    args = ["randog", "datetime", arg, arg, "--json", "--iso"]
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
            "datetime: error: argument --repeat/-r: invalid positive_int value: "
            f"'{length}'" in err
        )


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("2020-01-02T03:04:05", datetime(2020, 1, 2, 3, 4, 5)),
        ("2020-01-02T00:00:00", datetime(2020, 1, 2)),
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
            "datetime: error: argument --list/-L: invalid positive_int value: "
            f"'{length}'" in err
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
        (["--iso", "--repr"],),
        (["--fmt", "%Y/%m/%d", "--repr"],),
        (["--fmt", "%Y/%m/%d", "--iso"],),
        (["--fmt", "%Y/%m/%d", "--iso", "--repr"],),
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


class _FuzzyNow:
    radius: timedelta
    shift: timedelta

    def __init__(self, *, shift=timedelta(0), radius=timedelta(seconds=1)):
        self.radius = radius
        self.shift = shift

        if radius < timedelta(0):
            raise ValueError("radius must not be negative")

    def __repr__(self):
        result = "now"

        if self.shift != timedelta(0):
            result += timedelta_util.to_str(self.shift, explicit_sign=True)
        if self.radius != timedelta(0):
            result += " +- " + timedelta_util.to_str(self.radius)

        return f"Fuzzy({result})"

    def __eq__(self, other):
        now = datetime.now()
        self_as_dt = now + self.shift
        return -self.radius <= self_as_dt - other <= self.radius

    def __add__(self, other):
        if isinstance(other, timedelta):
            return _FuzzyNow(shift=self.shift + other, radius=self.radius)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self + (-other)
        else:
            return NotImplemented


@pytest.mark.parametrize(
    ("params", "expected_start", "expected_end"),
    [
        (["2022-01-01", "2022-01-02"], datetime(2022, 1, 1), datetime(2022, 1, 2)),
        (
            ["2022-01-01T10:00:00", "2022-01-02T10:00:00"],
            datetime(2022, 1, 1, 10),
            datetime(2022, 1, 2, 10),
        ),
        (
            ["2022-01-01T10:00:00.123", "2022-01-02T10:00:00.123"],
            datetime(2022, 1, 1, 10, 0, 0, 123000),
            datetime(2022, 1, 2, 10, 0, 0, 123000),
        ),
        (
            ["2022-01-01T10:00:00.000123", "2022-01-02T10:00:00.000123"],
            datetime(2022, 1, 1, 10, 0, 0, 123),
            datetime(2022, 1, 2, 10, 0, 0, 123),
        ),
        (["now", "now"], _FuzzyNow(), _FuzzyNow()),
        (["now-0", "now+0"], _FuzzyNow(), _FuzzyNow()),
        (
            ["now-1h", "now+1h"],
            _FuzzyNow() - timedelta(hours=1),
            _FuzzyNow() + timedelta(hours=1),
        ),
        (
            ["now-1h2m", "now+1h2m"],
            _FuzzyNow() - timedelta(hours=1, minutes=2),
            _FuzzyNow() + timedelta(hours=1, minutes=2),
        ),
        (
            ["now-1h+2m", "now+1h+2m"],
            _FuzzyNow() - timedelta(minutes=58),
            _FuzzyNow() + timedelta(hours=1, minutes=2),
        ),
        (
            ["2022-01-01T10:00:00-1h", "2022-01-01T10:00:00+1h"],
            datetime(2022, 1, 1, 9),
            datetime(2022, 1, 1, 11),
        ),
        (
            ["2022-01-01T10:00:00.120-1h2m", "2022-01-01T10:00:00.120+1h2m"],
            datetime(2022, 1, 1, 8, 58, 0, 120000),
            datetime(2022, 1, 1, 11, 2, 0, 120000),
        ),
        (
            ["2022-01-01T10:00:00.000001-1h+2m", "2022-01-01T10:00:00.000001+1h+2m"],
            datetime(2022, 1, 1, 9, 2, 0, 1),
            datetime(2022, 1, 1, 11, 2, 0, 1),
        ),
        (
            ["+1h"],
            _FuzzyNow(),
            _FuzzyNow() + timedelta(hours=1),
        ),
        (
            ["--", "-1h30m"],
            _FuzzyNow() - timedelta(hours=1, minutes=30),
            _FuzzyNow(),
        ),
        (
            ["2022-01-01T10:00:00", "+1h"],
            datetime(2022, 1, 1, 10),
            datetime(2022, 1, 1, 11),
        ),
        (
            ["now-2h", "+1h"],
            _FuzzyNow() - timedelta(hours=2),
            _FuzzyNow() - timedelta(hours=2) + timedelta(hours=1),
        ),
        (
            ["--", "-1h30m", "2022-01-01T10:00:00"],
            datetime(2022, 1, 1, 8, 30),
            datetime(2022, 1, 1, 10),
        ),
        (
            ["--", "-1h30m", "now+2h"],
            _FuzzyNow() + timedelta(hours=2) - timedelta(hours=1, minutes=30),
            _FuzzyNow() + timedelta(hours=2),
        ),
        (
            ["--", "-2h30m", "+1h30m"],
            _FuzzyNow() - timedelta(hours=2, minutes=30),
            _FuzzyNow() + timedelta(hours=1, minutes=30),
        ),
    ],
)
@patch("randog.factory.randdatetime", side_effect=randog.factory.randdatetime)
def test__main__datetime__suger(
    mock_func: mock.MagicMock,
    capfd,
    params,
    expected_start,
    expected_end,
):
    args = ["randog", "datetime", *params]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        mock_func.assert_called_once_with(expected_start, expected_end, rnd=AnyObject())

        out, err = capfd.readouterr()
        assert re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{6})?\n$", out)
        assert err == ""


@pytest.mark.parametrize(
    ("params",),
    [
        (["2020-01-02T03:04:06", "2020-01-02T03:04:05"],),
        (["--", "2020-01-02T03:04:06", "-1s"],),
        (["+1s", "2020-01-02T03:04:05"],),
        (["--", "+1s", "-1s"],),
    ],
)
def test__main__datetime__suger__error_by_inverse_range(
    capfd,
    params,
):
    args = ["randog", "datetime", *params]

    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "datetime: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
def test__main__datetime__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "datetime", "2022-01-01", "2022-12-31", "--repeat=50"]
    args0 = [*args_base, *seed0, "--output", str(output_path0)]
    args1 = [*args_base, *seed1, "--output", str(output_path1)]

    with patch.object(sys, "argv", args0):
        randog.__main__.main()
    with patch.object(sys, "argv", args1):
        randog.__main__.main()

    if expect_same_output:
        assert filecmp.cmp(output_path0, output_path1, shallow=False)
    else:
        assert not filecmp.cmp(output_path0, output_path1, shallow=False)

    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""


def test__main__datetime__help(capfd):
    args = ["randog", "datetime", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog datetime")
        assert err == ""
