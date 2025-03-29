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
    [
        "1",
        "a",
        "-",
        "2022-01-01+1h",
        "2022-01-01+1d1s",
        "today+1h",
        "today+1d1s",
        "1h",
        "1d1s",
        "today1d",
        "2d",
        "today0",
        "0",
    ],
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
    [
        "1",
        "a",
        "-",
        "2022-01-01+1h",
        "2022-01-01+1d1s",
        "today+1h",
        "today+1d1s",
        "1h",
        "1d1s",
        "today1d",
        "2d",
        "today0",
        "0",
    ],
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
        # with --list
        ("2020-01-02", ["--list=2", "--iso"], "['2020-01-02', '2020-01-02']"),
        ("2020-01-02", ["--list=1", "--fmt", "%Y/%m/%d"], "['2020/01/02']"),
        # with --list and --json
        ("2020-01-02", ["--list=2", "--json", "--iso"], '["2020-01-02", "2020-01-02"]'),
        ("2020-01-02", ["--list=1", "--json", "--fmt", "%Y/%m/%d"], '["2020/01/02"]'),
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


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__date__pickle(capfd, tmp_path, repeat):
    expected_value = dt.date(2000, 1, 2)
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "date",
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
def test__main__date__pickle_base64(capfd, repeat):
    expected_value = dt.date(2000, 1, 2)
    args = [
        "randog",
        "date",
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
def test__main__date__pickle_fmt(capfd, tmp_path, repeat):
    expected_value = dt.date(2000, 1, 2)
    args = [
        "randog",
        "date",
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
        ("2020-01-02", dt.date(2020, 1, 2)),
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


class _FuzzyNow:
    radius: dt.timedelta
    shift: dt.timedelta

    def __init__(self, *, shift=dt.timedelta(0), radius=dt.timedelta(0)):
        self.radius = radius
        self.shift = shift

        if radius < dt.timedelta(0):
            raise ValueError("radius must not be negative")

    def __repr__(self):
        result = "today"

        if self.shift != dt.timedelta(0):
            result += timedelta_util.to_str(self.shift, explicit_sign=True)
        if self.radius != dt.timedelta(0):
            result += " +- " + timedelta_util.to_str(self.radius)

        return f"Fuzzy({result})"

    def __eq__(self, other):
        today = dt.date.today()
        self_as_date = today + self.shift
        sub = self_as_date - other
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
        (["2022-01-01", "2022-01-02"], dt.date(2022, 1, 1), dt.date(2022, 1, 2)),
        (["today", "today"], _FuzzyNow(), _FuzzyNow()),
        (["today-0", "today+0"], _FuzzyNow(), _FuzzyNow()),
        (
            ["today-1d", "today+1d"],
            _FuzzyNow() - dt.timedelta(days=1),
            _FuzzyNow() + dt.timedelta(days=1),
        ),
        (
            ["today-1d48h", "today+1d24h"],
            _FuzzyNow() - dt.timedelta(days=3),
            _FuzzyNow() + dt.timedelta(days=2),
        ),
        (
            ["today-1d-2d", "today+1d+2d"],
            _FuzzyNow() - dt.timedelta(days=3),
            _FuzzyNow() + dt.timedelta(days=3),
        ),
        (
            ["2022-01-01-1d", "2022-01-01+1d"],
            dt.date(2021, 12, 31),
            dt.date(2022, 1, 2),
        ),
        (
            ["+1d"],
            _FuzzyNow(),
            _FuzzyNow() + dt.timedelta(days=1),
        ),
        (
            ["--", "-2d"],
            _FuzzyNow() - dt.timedelta(days=2),
            _FuzzyNow(),
        ),
        (
            ["2022-01-01", "+1d"],
            dt.date(2022, 1, 1),
            dt.date(2022, 1, 2),
        ),
        (
            ["today-2d", "+1d"],
            _FuzzyNow() - dt.timedelta(days=2),
            _FuzzyNow() - dt.timedelta(days=2) + dt.timedelta(days=1),
        ),
        (
            ["--", "-2d", "2022-01-01"],
            dt.date(2021, 12, 30),
            dt.date(2022, 1, 1),
        ),
        (
            ["--", "-2d", "today+1d"],
            _FuzzyNow() + dt.timedelta(days=1) - dt.timedelta(days=2),
            _FuzzyNow() + dt.timedelta(days=1),
        ),
        (
            ["--", "-2d", "+1d"],
            _FuzzyNow() - dt.timedelta(days=2),
            _FuzzyNow() + dt.timedelta(days=1),
        ),
    ],
)
@patch("randog.factory.randdate", side_effect=randog.factory.randdate)
def test__main__datetime__suger(
    mock_func: mock.MagicMock,
    capfd,
    params,
    expected_start,
    expected_end,
):
    args = ["randog", "date", *params]

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        mock_func.assert_called_once_with(expected_start, expected_end, rnd=AnyObject())

        out, err = capfd.readouterr()
        assert re.match(r"^\d{4}-\d{2}-\d{2}\n$", out)
        assert err == ""


@pytest.mark.parametrize(
    ("params",),
    [
        (["2020-01-02", "2020-01-01"],),
        (["--", "2020-01-02", "-1d"],),
        (["+1d", "2020-01-02"],),
        (["--", "+1d", "-1d"],),
    ],
)
def test__main__date__suger__error_by_inverse_range(
    capfd,
    params,
):
    args = ["randog", "date", *params]

    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "date: error: arguments must satisfy MINIMUM <= MAXIMUM" in err


@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
def test__main__date__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "date", "2022-01-01", "2022-12-31", "--repeat=50"]
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


def test__main__date__help(capfd):
    args = ["randog", "date", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog date")
        assert err == ""
