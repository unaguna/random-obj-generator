import sys
from unittest.mock import patch

import randog.__main__


def test__main__output_name__def_file_name(capfd, tmp_path, resources):
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
