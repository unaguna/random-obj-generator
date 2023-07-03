import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__str(capfd):
    args = ["randog", "str"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        assert err == ""


@pytest.mark.parametrize(
    "length",
    [0, 1, 5, 10],
)
def test__main__str__length(capfd, length):
    args = ["randog", "str", "--length", str(length), "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert set(map(len, out.splitlines(keepends=False))) == {length}
        assert err == ""


@pytest.mark.parametrize(
    ("length", "expected_length"),
    [("0:2", range(0, 3)), ("5:7", range(5, 8)), ("10:10", [10])],
)
def test__main__str__random_length(capfd, length, expected_length):
    args = ["randog", "str", "--length", length, "--repeat=200"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert set(map(len, out.splitlines(keepends=False))) == set(expected_length)
        assert err == ""


@pytest.mark.parametrize(
    "charset",
    ["0123456789", "abc", "ABC"],
)
def test__main__str__charset(capfd, charset):
    args = ["randog", "str", "--charset", charset, "--length=1000"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        for out_line in out.splitlines(keepends=False):
            assert set(out_line) == set(charset)
        assert err == ""


@pytest.mark.parametrize(
    "length",
    [
        "0.1",
        "a",
        "-1",
        "-",
        # illegal range (missing)
        ":",
        "1:",
        ":5",
        # illegal range (non-integer)
        "1.2:5",
        "1:5.6",
        "a:5",
        "5:a",
        # illegal range (negative)
        "'-1:1'",
        "1:-1",
        # illegal range (max < min)
        "2:1",
        "10:7",
    ],
)
def test__main__str__error_when_illegal_length(capfd, length):
    args = ["randog", "str", "--length", length]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "str: error: argument --length: invalid non_negative_int_range value: "
            in err
        )


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["--charset=a", "--length=3"], "'aaa'"),
        (["--length=0"], "''"),
    ],
)
def test__main__str__option_repr(capfd, options, expected):
    args = ["randog", "str", *options, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["--charset=a", "--length=3"], '"aaa"'),
        (["--length=0"], '""'),
    ],
)
def test__main__str__option_json(capfd, options, expected):
    args = ["randog", "str", *options, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__str__option_repeat(capfd, resources, option, count):
    args = [
        "randog",
        "str",
        "--length=2",
        "--charset=a",
        option,
        str(count),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"aa\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__str__error_with_negative_repeat(capfd, resources, option, length):
    args = [
        "randog",
        "str",
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
            f"str: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__str__option_list(capfd, resources, option, length):
    args = [
        "randog",
        "str",
        "--length=2",
        "--charset=a",
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str(["aa"] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__str__error_with_negative_list(capfd, resources, option, length):
    args = [
        "randog",
        "str",
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
            f"str: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__str__option_output(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "str",
        "--length=2",
        "--charset=a",
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == f"aa\n"
            assert out_fp.readline() == ""


def test__main__str__option_output__option_repeat(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "str",
        "--length=2",
        "--charset=a",
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
                assert out_fp.readline() == f"aa\n"
            assert out_fp.readline() == ""


def test__main__str__option_output__option_repeat__separate(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "str",
        "--length=2",
        "--charset=a",
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
                assert out_fp.readline() == f"aa\n"
                assert out_fp.readline() == ""


@pytest.mark.parametrize(
    ("options",),
    [
        (["--json", "--repr"],),
    ],
)
def test__main__str__error_duplicate_format(capfd, resources, options):
    args = ["randog", "str", *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


def test__main__str__help(capfd):
    args = ["randog", "str", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: python -m randog str")
        assert err == ""