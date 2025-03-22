import ast
import filecmp
import os.path
import re
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__bytes(capfd):
    args = ["randog", "bytes"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out != ""
        assert err == ""


@pytest.mark.parametrize(
    "length",
    [0, 1, 5, 10],
)
def test__main__bytes__length(capsysbinary, length):
    args = ["randog", "bytes", "--length", str(length)]
    result_stdout = []
    for _ in range(20):
        with patch.object(sys, "argv", args):
            randog.__main__.main()

            out, err = capsysbinary.readouterr()
            assert err == b""
            result_stdout.append(out)

    assert {len(out)} == {length}


@pytest.mark.parametrize(
    ("length", "expected_length"),
    [("0:2", range(0, 3)), ("5:7", range(5, 8)), ("10:10", [10])],
)
def test__main__bytes__random_length(capsysbinary, length, expected_length):
    args = ["randog", "bytes", "--length", length]
    result_stdout = []
    for _ in range(100):
        with patch.object(sys, "argv", args):
            randog.__main__.main()

            out, err = capsysbinary.readouterr()
            assert err == b""
            result_stdout.append(out)

    assert {len(out)} <= set(expected_length)


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
def test__main__bytes__error_when_illegal_length(capfd, length):
    args = ["randog", "bytes", "--length", length]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "bytes: error: argument --length: invalid non_negative_int_range value: "
            in err
        )


def test__main__bytes__option_repr(capfd):
    expected_length = 8
    args = ["randog", "bytes", "--repr"]
    for _ in range(10):
        with patch.object(sys, "argv", args):
            randog.__main__.main()

            out, err = capfd.readouterr()
            assert err == ""
            actual = ast.literal_eval(out.strip())
            assert isinstance(actual, bytes)
            assert len(actual) == expected_length


def test__main__bytes__option_json(capfd):
    args = ["randog", "bytes", "--json", "--fmt=b"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""
        assert re.fullmatch(r"\"[01]{64}\"\n", out)


def test__main__bytes__error_with_option_json(capfd):
    args = ["randog", "bytes", "--json"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "bytes: error: argument --json can only be used with --fmt in bytes mode."
            in err
        )


@pytest.mark.parametrize(
    ("options", "expected_regex"),
    [
        (["--fmt", "b"], re.compile(r"[01]{64}")),
        (["--fmt", "_b"], re.compile(r"([01]{4}_){15}[01]{4}")),
        (["--fmt", "x"], re.compile(r"[0-9a-f]{16}")),
        (["--fmt", "_x"], re.compile(r"([0-9a-f]{4}_){3}[0-9a-f]{4}")),
        (["--fmt", "X"], re.compile(r"[0-9A-F]{16}")),
        (["--fmt", "_X"], re.compile(r"([0-9A-F]{4}_){3}[0-9A-F]{4}")),
        # TODO: base64 形式にするオプション
    ],
)
def test__main__bytes__fmt(capfd, options, expected_regex):
    args = ["randog", "bytes", *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert re.fullmatch(expected_regex, out.strip("\n"))
        assert err == ""


@pytest.mark.parametrize(
    ("options",),
    [
        (["--fmt", "c"],),
        (["--fmt", "s"],),
    ],
)
def test__main__bytes__fmt_c(capfd, options):
    args = ["randog", "bytes", *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""
        actual = ast.literal_eval("b" + repr(out.strip("\n")))
        assert isinstance(actual, bytes)


@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__bytes__option_repeat(capsysbinary, resources, option, count):
    length = 2
    args = [
        "randog",
        "bytes",
        f"--length={length}",
        option,
        str(count),
    ]
    result_stdout = []
    for _ in range(10):
        with patch.object(sys, "argv", args):
            randog.__main__.main()

            out, err = capsysbinary.readouterr()
            assert err == b""
            result_stdout.append(out)

    assert {len(out)} == {length * count}


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__bytes__error_with_negative_repeat(capfd, resources, option, length):
    args = [
        "randog",
        "bytes",
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
            "bytes: error: argument --repeat/-r: "
            f"invalid positive_int value: '{length}'" in err
        )


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__bytes__option_list(capfd, resources, option, length):
    byte_len = 2
    args = [
        "randog",
        "bytes",
        f"--length={byte_len}",
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert err == ""
        actual = ast.literal_eval(out.strip("\n"))
        assert isinstance(actual, list)
        assert {type(v) for v in actual} == {bytes}
        assert {len(v) for v in actual} == {byte_len}


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__bytes__error_with_negative_list(capfd, resources, option, length):
    args = [
        "randog",
        "bytes",
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
            f"bytes: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    "length",
    [0, 1, 5, 10],
)
def test__main__bytes__option_output(capfd, tmp_path, resources, length):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "bytes",
        f"--length={length}",
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="rb") as out_fp:
            actual = out_fp.read(length + 1)
        assert len(actual) == length


def test__main__bytes__option_output__option_repeat(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    length = 2
    args = [
        "randog",
        "bytes",
        f"--length={length}",
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

        with open(output_path, mode="rb") as out_fp:
            actual = out_fp.read(count * length + 1)
        assert len(actual) == count * length


def test__main__bytes__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    length = 3
    args = [
        "randog",
        "bytes",
        f"--length={length}",
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
            with open(output_paths[i], mode="rb") as out_fp:
                actual = out_fp.read(length + 1)
            assert len(actual) == length


@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
def test__main__bytes__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "bytes", "--repeat=50"]
    args0 = [*args_base, *seed0, "--output", str(output_path0)]
    args1 = [*args_base, *seed1, "--output", str(output_path1)]

    with patch.object(sys, "argv", args0):
        randog.__main__.main()
    with patch.object(sys, "argv", args1):
        randog.__main__.main()

    assert os.path.getsize(output_path0) > 0
    if expect_same_output:
        assert filecmp.cmp(output_path0, output_path1, shallow=False)
    else:
        assert not filecmp.cmp(output_path0, output_path1, shallow=False)

    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""


def test__main__bytes__help(capfd):
    args = ["randog", "bytes", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog bytes")
        assert err == ""
