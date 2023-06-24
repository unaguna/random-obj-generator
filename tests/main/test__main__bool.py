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
    ("prop_true", "expected"),
    [("0", False), ("0.0", False), ("1", True), ("1.0", True)],
)
def test__main__bool__option_repr(capfd, prop_true, expected):
    args = ["randog", "bool", prop_true, "--repr"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("prop_true", "expected"),
    [("0", "false"), ("0.0", "false"), ("1", "true"), ("1.0", "true")],
)
def test__main__bool__option_json(capfd, prop_true, expected):
    args = ["randog", "bool", prop_true, "--json"]
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
