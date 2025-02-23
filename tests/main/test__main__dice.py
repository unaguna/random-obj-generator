import filecmp
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__dice__error_when_miss_args(capfd):
    args = ["randog", "dice"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "the following arguments are required: DICE_ROLL" in err


@pytest.mark.parametrize(
    "expected",
    [1, 2, 3],
)
@pytest.mark.parametrize(
    "sep",
    ["d", "D"],
)
def test__main__dice__code(capfd, expected, sep):
    args = ["randog", "dice", str(expected) + sep + "1"]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"{expected}\n"
        assert err == ""


@pytest.mark.parametrize(
    ("code", "maximum"),
    [
        ("1d10", 10),
        ("d6", 6),
        ("3d100", 300),
        ("1D10", 10),
        ("D6", 6),
        ("3D100", 300),
    ],
)
def test__main__dice__code2(capfd, code, maximum):
    args = ["randog", "dice", code]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert 1 <= int(out.strip()) <= maximum
        assert err == ""


@pytest.mark.parametrize(
    ("code",),
    [
        ("100",),
        ("10d",),
    ],
)
def test__main__dice__error_when_illegal_code(capfd, code):
    args = ["randog", "dice", code]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "dice: error: argument DICE_ROLL: invalid dice_roll value: " in err


@pytest.mark.parametrize(
    "expected",
    [1, 2, 3],
)
@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__dice__option_repeat(capfd, resources, expected, option, count):
    args = [
        "randog",
        "dice",
        f"{expected}d1",
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
def test__main__int__error_with_negative_repeat(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "dice",
        f"{expected}d1",
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
            f"dice: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


@pytest.mark.parametrize(
    "expected",
    [1, 2, 3],
)
@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__dice__option_list(capfd, resources, expected, option, length):
    args = [
        "randog",
        "dice",
        f"{expected}d1",
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
def test__main__dice__error_with_negative_list(capfd, resources, option, length):
    expected = 100
    args = [
        "randog",
        "dice",
        f"{expected}d1",
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
            f"dice: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__dice__option_output(capfd, tmp_path, resources):
    expected = 100
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "dice",
        f"{expected}d1",
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


def test__main__dice__option_output__option_repeat(capfd, tmp_path, resources):
    expected = 100
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "dice",
        f"{expected}d1",
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


def test__main__dice__option_output__option_repeat__separate(
    capfd, tmp_path, resources
):
    expected = 100
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "dice",
        f"{expected}d1",
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
def test__main__dice__error_duplicate_format(capfd, resources, options):
    args = ["randog", "dice", "1d100", *options]
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
def test__main__dice__seed(capfd, tmp_path, seed0, seed1, expect_same_output):
    output_path0 = tmp_path.joinpath("out_0.txt")
    output_path1 = tmp_path.joinpath("out_1.txt")
    args_base = ["randog", "dice", "1d100", "--repeat=50"]
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


def test__main__dice__help(capfd):
    args = ["randog", "dice", "--help"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit) as ex:
            randog.__main__.main()

        assert ex.value.code == 0

        out, err = capfd.readouterr()
        assert out.startswith("usage: python -m randog dice")
        assert err == ""
