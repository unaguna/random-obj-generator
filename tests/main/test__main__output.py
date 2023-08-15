import glob
import os
import sys
from unittest.mock import patch

import pytest

import randog.__main__


def _make_exist_file(filepath):
    with open(filepath, mode="xt") as fp:
        fp.write("This file must be overwritten.\n")


def test__main__output__overwrite_exist_file(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out.txt")
    output_path = output_fmt_path
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        str(resources.joinpath("factory_def_bbb.py")),
        "--output",
        str(output_fmt_path),
        "--repeat=2",
    ]

    _make_exist_file(output_path)

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == "bbb\n"
            assert out_fp.readline() == "bbb\n"
            assert out_fp.readline() == ""


def test__main__output_name__def_file_name__factory_count(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{factory_count}_{def_file}.txt")
    output_paths = [
        tmp_path.joinpath("out_0_factory_def.txt"),
        tmp_path.joinpath("out_1_factory_def_bbb.txt"),
    ]
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        str(resources.joinpath("factory_def_bbb.py")),
        "--output",
        str(output_fmt_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_paths[0], mode="r") as out_fp:
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == ""
        with open(output_paths[1], mode="r") as out_fp:
            assert out_fp.readline() == "bbb\n"
            assert out_fp.readline() == ""


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        (["bool", "1.0"], "True"),
        (["int", "3", "3"], "3"),
        (["float", "3", "3"], "3.0"),
        (["str", "--length", "3", "--charset", "a"], "aaa"),
        (["date", "2022-01-02", "2022-01-02"], "2022-01-02"),
        (["time", "11:22:33", "11:22:33"], "11:22:33"),
    ],
)
def test__main__output_name__def_file_name__factory_count__without_byfile(
    capfd,
    tmp_path,
    resources,
    arguments,
    expected,
):
    output_fmt_path = tmp_path.joinpath("out_{factory_count}_{def_file}.txt")
    output_paths = tmp_path.joinpath("out_0_.txt")
    args = [
        "randog",
        *arguments,
        "--output",
        str(output_fmt_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_paths, mode="r") as out_fp:
            assert out_fp.readline() == f"{expected}\n"
            assert out_fp.readline() == ""


def test__main__output_name__repeat__def_file_name(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{def_file}.txt")
    output_paths = [
        tmp_path.joinpath("out_factory_def.txt"),
        tmp_path.joinpath("out_factory_def_bbb.txt"),
    ]
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        str(resources.joinpath("factory_def_bbb.py")),
        "--output",
        str(output_fmt_path),
        "--repeat=2",
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        # Why does it get two lines of output each?
        # => Even if output path is duplicated in `--repeat`, it writes in same file.
        with open(output_paths[0], mode="r") as out_fp:
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == ""
        with open(output_paths[1], mode="r") as out_fp:
            assert out_fp.readline() == "bbb\n"
            assert out_fp.readline() == "bbb\n"
            assert out_fp.readline() == ""


@pytest.mark.parametrize(
    ("output_files", "repeat_options"),
    [
        (
            [
                ("out_factory_def_0.txt", "aaa"),
                ("out_factory_def_1.txt", "aaa"),
                ("out_factory_def_bbb_0.txt", "bbb"),
                ("out_factory_def_bbb_1.txt", "bbb"),
            ],
            ["--repeat=2"],
        ),
        (
            [
                ("out_factory_def_0.txt", "aaa"),
                ("out_factory_def_bbb_0.txt", "bbb"),
            ],
            [],
        ),
    ],
)
def test__main__output_name__def_file__repeat_count(
    capfd,
    tmp_path,
    resources,
    output_files,
    repeat_options,
):
    output_fmt_path = tmp_path.joinpath("out_{def_file}_{repeat_count}.txt")
    output_files = list((tmp_path.joinpath(f), exp) for f, exp in output_files)
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        str(resources.joinpath("factory_def_bbb.py")),
        "--output",
        str(output_fmt_path),
        *repeat_options,
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        for output_path, expected in output_files:
            with open(output_path, mode="r") as out_fp:
                assert out_fp.readline() == f"{expected}\n"
                assert out_fp.readline() == ""


def test__main__output_name__now(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{now:%Y%m%d%H%M%S}.txt")
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        str(resources.joinpath("factory_def_bbb.py")),
        "--output",
        str(output_fmt_path),
    ]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        output_paths = glob.glob(str(tmp_path.joinpath("out_*.txt")))

        assert len(output_paths) == 1
        with open(output_paths[0], mode="r") as out_fp:
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == "bbb\n"
            assert out_fp.readline() == ""


def test__main__output__env(capfd, tmp_path, resources):
    output_fmt_path = tmp_path.joinpath("out_{FOO}.txt")
    output_path = tmp_path.joinpath("out_testing.txt")
    args = [
        "randog",
        "byfile",
        str(resources.joinpath("factory_def.py")),
        "--output",
        str(output_fmt_path),
    ]

    os.environ["FOO"] = "testing"

    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == ""
        assert err == ""

        with open(output_path, mode="r") as out_fp:
            assert out_fp.readline() == "aaa\n"
            assert out_fp.readline() == ""
