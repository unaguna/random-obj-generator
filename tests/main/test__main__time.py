import base64
import datetime as dt
import filecmp
import pickle
import re
import sys
from unittest import mock
from unittest.mock import patch

import pytest

import randog.__main__
from randog import timedelta_util
from tests.testtools.trickobj import AnyObject


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
    [
        "1",
        "a",
        "-",
        "01:00:00+a",
        "now1h",
        "2h",
        "now0",
        "0",
    ],
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
    [
        "1",
        "a",
        "-",
        "01:00:00+a",
        "now1h",
        "2h",
        "now0",
        "0",
    ],
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
        # with --list
        ("03:04:05", ["--list=2", "--iso"], "['03:04:05', '03:04:05']"),
        ("03:04:05", ["--list=1", "--fmt", "a%H:%M:%S"], "['a03:04:05']"),
        # with --list and --json
        ("03:04:05", ["--list=2", "--json", "--iso"], '["03:04:05", "03:04:05"]'),
        ("03:04:05", ["--list=1", "--json", "--fmt", "a%H:%M:%S"], '["a03:04:05"]'),
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


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__time__pickle(capfd, tmp_path, repeat):
    expected_value = dt.time(3, 4, 5)
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "time",
        expected_value.isoformat(),
        expected_value.isoformat(),
        "--pickle",
        "--output",
        str(output_path),
        "--repeat",
        str(repeat),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

    with open(output_path, mode="br") as fp:
        values = [pickle.load(fp) for _ in range(repeat)]

    assert values == [expected_value] * repeat


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__time__pickle_base64(capfd, repeat):
    expected_value = dt.time(3, 4, 5)
    args = [
        "randog",
        "time",
        expected_value.isoformat(),
        expected_value.isoformat(),
        "--pickle",
        "--base64",
        "--repeat",
        str(repeat),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

    pickle_encoded = [
        base64.b64decode(s, validate=True) for s in out.split("\n") if s != ""
    ]
    values = [pickle.loads(b) for b in pickle_encoded]

    assert values == [expected_value] * repeat


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__time__pickle_fmt(capfd, tmp_path, repeat):
    expected_value = dt.time(3, 4, 5)
    args = [
        "randog",
        "time",
        expected_value.isoformat(),
        expected_value.isoformat(),
        "--pickle",
        "--fmt=x",
        "--repeat",
        str(repeat),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""

    pickle_encoded = [bytes.fromhex(s) for s in out.split("\n") if s != ""]
    values = [pickle.loads(b) for b in pickle_encoded]

    assert values == [expected_value] * repeat


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


class _FuzzyNow:
    radius: dt.timedelta
    shift: dt.timedelta

    def __init__(self, *, shift=dt.timedelta(0), radius=dt.timedelta(seconds=1)):
        self.radius = radius
        self.shift = shift

        if radius < dt.timedelta(0):
            raise ValueError("radius must not be negative")

    def __repr__(self):
        result = "now"

        if self.shift != dt.timedelta(0):
            result += timedelta_util.to_str(self.shift, explicit_sign=True)
        if self.radius != dt.timedelta(0):
            result += " +- " + timedelta_util.to_str(self.radius)

        return f"Fuzzy({result})"

    def __eq__(self, other):
        now = dt.datetime.now()
        self_as_dt = now + self.shift
        sub = self_as_dt - dt.datetime.combine(self_as_dt.date(), other)
        return -self.radius <= sub <= self.radius or (
            sub <= self.radius - dt.timedelta(days=1)
            or sub >= dt.timedelta(days=1) - self.radius
        )

    def __add__(self, other):
        if isinstance(other, dt.timedelta):
            return _FuzzyNow(shift=self.shift + other, radius=self.radius)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, dt.timedelta):
            return self + (-other)
        else:
            return NotImplemented


@pytest.mark.parametrize(
    ("params", "expected_start", "expected_end"),
    [
        (["01:00:00", "02:00:00"], dt.time(1), dt.time(2)),
        (["02:00:00", "01:00:00"], dt.time(2), dt.time(1)),
        (["now", "now"], _FuzzyNow(), _FuzzyNow()),
        (["now-0", "now+0"], _FuzzyNow(), _FuzzyNow()),
        (
            ["now-1h", "now+1h"],
            _FuzzyNow() - dt.timedelta(hours=1),
            _FuzzyNow() + dt.timedelta(hours=1),
        ),
        (
            ["now-1h2m", "now+1h2m"],
            _FuzzyNow() - dt.timedelta(hours=1, minutes=2),
            _FuzzyNow() + dt.timedelta(hours=1, minutes=2),
        ),
        (
            ["now-1h+2m", "now+1h+2m"],
            _FuzzyNow() - dt.timedelta(minutes=58),
            _FuzzyNow() + dt.timedelta(hours=1, minutes=2),
        ),
        (["10:00:00-1h", "10:00:00+1h"], dt.time(9), dt.time(11)),
        (
            ["10:00:00.120-1h2m", "10:00:00.120+1h2m"],
            dt.time(8, 58, 0, 120000),
            dt.time(11, 2, 0, 120000),
        ),
        (
            ["10:00:00.000001-1h+2m", "10:00:00.000001+1h+2m"],
            dt.time(9, 2, 0, 1),
            dt.time(11, 2, 0, 1),
        ),
        (
            ["+1h"],
            _FuzzyNow(),
            _FuzzyNow() + dt.timedelta(hours=1),
        ),
        (
            ["--", "-1h30m"],
            _FuzzyNow() - dt.timedelta(hours=1, minutes=30),
            _FuzzyNow(),
        ),
        (["10:00:00", "+1h"], dt.time(10), dt.time(11)),
        (["10:00:00", "+23h"], dt.time(10), dt.time(9)),
        (["--", "10:00:00", "-1h"], dt.time(10), dt.time(9)),
        (
            ["now-2h", "+1h"],
            _FuzzyNow() - dt.timedelta(hours=2),
            _FuzzyNow() - dt.timedelta(hours=2) + dt.timedelta(hours=1),
        ),
        (["--", "-1h30m", "10:00:00"], dt.time(8, 30), dt.time(10)),
        (["--", "+1h30m", "10:00:00"], dt.time(11, 30), dt.time(10)),
        (
            ["--", "-1h30m", "now+2h"],
            _FuzzyNow() + dt.timedelta(hours=2) - dt.timedelta(hours=1, minutes=30),
            _FuzzyNow() + dt.timedelta(hours=2),
        ),
        (
            ["--", "now+2h", "-1h30m"],
            _FuzzyNow() + dt.timedelta(hours=2),
            _FuzzyNow() + dt.timedelta(hours=2) - dt.timedelta(hours=1, minutes=30),
        ),
        (
            ["--", "-2h30m", "+1h30m"],
            _FuzzyNow() - dt.timedelta(hours=2, minutes=30),
            _FuzzyNow() + dt.timedelta(hours=1, minutes=30),
        ),
        (
            ["--", "+1h30m", "-2h30m"],
            _FuzzyNow() + dt.timedelta(hours=1, minutes=30),
            _FuzzyNow() - dt.timedelta(hours=2, minutes=30),
        ),
    ],
)
@patch("randog.factory.randtime", side_effect=randog.factory.randtime)
def test__main__time__suger(
    mock_func: mock.MagicMock,
    capfd,
    params,
    expected_start,
    expected_end,
):
    args = ["randog", "time", *params]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        mock_func.assert_called_once_with(expected_start, expected_end, rnd=AnyObject())

        out, err = capfd.readouterr()
        assert re.match(r"^\d{2}:\d{2}:\d{2}(?:\.\d{6})?\n$", out)
        assert err == ""


@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
def test__main__time__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "time", "00:00:00", "12:00:00", "--repeat=50"]
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


def test__main__time__help(capfd):
    args = ["randog", "time", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog time")
        assert err == ""
