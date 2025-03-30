import base64
import filecmp
import pickle
import re
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


@pytest.mark.require_rstr
@pytest.mark.parametrize(
    "regex",
    [
        r"[\d]+BC",
        r"[abc]+",
    ],
)
def test__main__str__regex(capfd, regex):
    args = ["randog", "str", "--regex", regex, "--repeat=100"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()

        assert {
            v for v in out.splitlines(keepends=False) if not re.fullmatch(regex, v)
        } == set()
        assert err == ""


@pytest.mark.require_rstr
@pytest.mark.parametrize(
    "options",
    [
        ["--length", "3"],
        ["--charset", "a"],
    ],
)
def test__main__str__error_when_specify_regex_and_length_charset(capfd, options):
    args = ["randog", "str", "--regex", "[0-9]+c", *options]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err


@pytest.mark.without_rstr
def test__main__str__regex__error_without_rstr(capfd):
    args = ["randog", "str", "--regex", "[0-9]+c"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            "str: error: argument --regex: package 'rstr' is required to use --regex"
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
    ("options", "expected"),
    [
        (
            ["--charset=あ", "--length=3", "--json-ensure-ascii"],
            r'"\u3042\u3042\u3042"',
        ),
        (
            ["--charset=あ", "--length=3"],
            r'"あああ"',
        ),
    ],
)
def test__main__str__option_json_unicode(capfd, options, expected):
    args = ["randog", "str", *options, "--json"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (["--charset=a", "--length=3", "--fmt", ">5"], "  aaa"),
    ],
)
def test__main__str__fmt(capfd, options, expected):
    args = ["randog", "str", *options]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__str__pickle(capfd, tmp_path, repeat):
    expected_value = "aaa"
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "str",
        "--length=3",
        "--charset=a",
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
def test__main__str__pickle_base64(capfd, repeat):
    expected_value = "aaa"
    args = [
        "randog",
        "str",
        "--length=3",
        "--charset=a",
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
def test__main__str__pickle_fmt(capfd, tmp_path, repeat):
    expected_value = "aaa"
    args = [
        "randog",
        "str",
        "--length=3",
        "--charset=a",
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


@pytest.mark.parametrize("repeat", [1, 2])
def test__main__str__pickle_list(capfd, tmp_path, repeat):
    expected_value = "aaa"
    list_length = 2
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "str",
        "--length=3",
        "--charset=a",
        "--pickle",
        "--list",
        str(list_length),
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

    assert values == [[expected_value] * list_length] * repeat


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
        assert out == "aa\n" * count
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
            assert out_fp.readline() == "aa\n"
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
                assert out_fp.readline() == "aa\n"
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
                assert out_fp.readline() == "aa\n"
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


@pytest.mark.parametrize(
    ("seed0", "seed1", "expect_same_output"),
    [
        (["--seed=100"], ["--seed=100"], True),
        (["--seed=100"], ["--seed=1000"], False),
        ([], ["--seed=1000"], False),
        ([], [], False),
    ],
)
def test__main__str__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "str", "--repeat=50"]
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


def test__main__str__help(capfd):
    args = ["randog", "str", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: randog str")
        assert err == ""
