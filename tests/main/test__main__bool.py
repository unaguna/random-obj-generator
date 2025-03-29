import base64
import filecmp
import pickle
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__bool(capfd):
    args = ["randog", "bool"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out in ("True\n", "False\n")
        assert err == ""


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
def test__main__bool__prop_true(capfd, prop_true, expected):
    args = ["randog", "bool", prop_true]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    "prop_true",
    ["-1", "-0.1", "1.1", "INF", "foo"],
)
def test__main__bool__error_when_illegal_prop_true(capfd, prop_true):
    args = ["randog", "bool", prop_true]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "bool: error: argument PROP_TRUE: invalid probability value: " in err


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["0", "--repr"], "False"),
        (["1", "--repr"], "True"),
        (["0", "--json"], "false"),
        (["1", "--json"], "true"),
        (["0", "--fmt", "1"], "0"),
        (["1", "--fmt", "1"], "1"),
    ],
)
def test__main__bool__fmt(capfd, options, expected):
    args = ["randog", "bool", *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__bool__option_repeat(capfd, prop_true, expected, option, count):
    args = [
        "randog",
        "bool",
        prop_true,
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
def test__main__bool__error_with_negative_repeat(capfd, option, length):
    args = [
        "randog",
        "bool",
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
            f"bool: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__bool__option_list(capfd, prop_true, expected, option, length):
    args = [
        "randog",
        "bool",
        prop_true,
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
def test__main__bool__error_with_negative_list(capfd, option, length):
    args = [
        "randog",
        "bool",
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
            f"bool: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
def test__main__bool__option_output(capfd, tmp_path, prop_true, expected):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "bool",
        prop_true,
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


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
def test__main__bool__option_output__option_repeat(
    capfd, tmp_path, prop_true, expected
):
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "bool",
        prop_true,
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


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
def test__main__bool__option_output__option_repeat__separate(
    capfd, tmp_path, prop_true, expected
):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "bool",
        prop_true,
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
def test__main__bool__error_duplicate_format(capfd, options):
    args = ["randog", "bool", *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
@pytest.mark.parametrize("repeat", [1, 2])
def test__main__bool__pickle(capfd, tmp_path, prop_true, expected, repeat):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "bool",
        prop_true,
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

    assert values == [expected] * repeat


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
@pytest.mark.parametrize("repeat", [1, 2])
def test__main__bool__pickle_base64(capfd, prop_true, expected, repeat):
    args = [
        "randog",
        "bool",
        prop_true,
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

    assert values == [expected] * repeat


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
@pytest.mark.parametrize("repeat", [1, 2])
def test__main__bool__pickle_fmt(capfd, tmp_path, prop_true, expected, repeat):
    args = [
        "randog",
        "bool",
        prop_true,
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

    assert values == [expected] * repeat


@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
def test__main__bool__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "bool", "--repeat=50"]
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


def test__main__bool__help(capfd):
    args = ["randog", "bool", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog bool")
        assert err == ""
