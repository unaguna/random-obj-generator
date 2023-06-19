import sys
from unittest.mock import patch

import pytest

import randog.__main__


@pytest.mark.parametrize(
    ("option", "def_file", "expected"),
    [
        ("-f", "factory_def.py", "aaa\n"),
        ("--factory", "factory_def_bbb.py", "bbb\n"),
    ],
)
def test__main__spec_factory(capfd, resources, option, def_file, expected):
    args = ["randog", option, str(resources.joinpath(def_file))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == expected
        assert err == ""


def test__main__option_repr(capfd, resources):
    args = ["randog", "--repr", "-f", str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "'aaa'\n"
        assert err == ""


def test__main__option_json(capfd, resources):
    args = ["randog", "--json", "-f", str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == '"aaa"\n'
        assert err == ""


@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__option_repeat(capfd, resources, option, count):
    args = [
        "randog",
        option,
        str(count),
        "-f",
        str(resources.joinpath("factory_def.py")),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n" * count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--repeat", -1),
        ("-r", 0),
    ],
)
def test__main__error_with_negative_repeat(capfd, resources, option, length):
    args = [
        "randog",
        option,
        str(length),
        "-f",
        str(resources.joinpath("factory_def.py")),
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            f"randog: error: argument --repeat/-r: invalid positive_int value: '{length}'"
            in err
        )


def test__main__multiple_factories(capfd, resources):
    args = [
        "randog",
        "-f",
        str(resources.joinpath("factory_def.py")),
        str(resources.joinpath("factory_def_bbb.py")),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\nbbb\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "r_count", "f_count"),
    [
        ("--repeat", 3, 2),
        ("-r", 2, 5),
    ],
)
def test__main__option_repeat__multiple_factories(
    capfd, resources, option, r_count, f_count
):
    factory_path = str(resources.joinpath("factory_def.py"))
    factory_bbb_path = str(resources.joinpath("factory_def_bbb.py"))
    args = (
        ["randog", option, str(r_count), "-f"]
        + (f_count - 1) * [factory_path]
        + [factory_bbb_path]
    )
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n" * (r_count * (f_count - 1)) + "bbb\n" * r_count
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", 1),
        ("-L", 2),
    ],
)
def test__main__option_list(capfd, resources, option, length):
    args = [
        "randog",
        "-f",
        str(resources.joinpath("factory_def.py")),
        option,
        str(length),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == str(["aaa"] * length) + "\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "length"),
    [
        ("--list", -1),
        ("-L", 0),
    ],
)
def test__main__error_with_negative_list(capfd, resources, option, length):
    args = [
        "randog",
        option,
        str(length),
        "-f",
        str(resources.joinpath("factory_def.py")),
    ]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert (
            f"randog: error: argument --list/-L: invalid positive_int value: '{length}'"
            in err
        )


def test__main__option_output(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    args = [
        "randog",
        "-f",
        str(resources.joinpath("factory_def.py")),
        "--output",
        str(output_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == ""


def test__main__option_output__option_repeat(capfd, tmp_path, resources):
    output_path = tmp_path.joinpath("out.txt")
    count = 3
    args = [
        "randog",
        "-f",
        str(resources.joinpath("factory_def.py")),
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
                assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == ""


def test__main__option_output__option_repeat__separate(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{}.txt")
    output_paths = [tmp_path.joinpath("out_0.txt"), tmp_path.joinpath("out_1.txt")]
    count = len(output_paths)
    args = [
        "randog",
        "-f",
        str(resources.joinpath("factory_def.py")),
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
                assert out_fp.readline() == "aaa\n"
                assert out_fp.readline() == ""


@pytest.mark.parametrize(
    ("options",),
    [
        (["--json", "--repr"],),
    ],
)
def test__main__error_duplicate_format(capfd, resources, options):
    args = ["randog", *options, "-f", str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("usage:")
        assert "not allowed with argument" in err
