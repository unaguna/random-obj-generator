import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main(capfd, resources):
    args = ["randog", str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n"
        assert err == ""


def test__main__option_repr(capfd, resources):
    args = ["randog", "--repr", str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "'aaa'\n"
        assert err == ""


@pytest.mark.parametrize(
    ("option", "count"),
    [
        ("--repeat", 3),
        ("-r", 2),
    ],
)
def test__main__option_repeat(capfd, resources, option, count):
    args = ["randog", option, str(count), str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n" * count
        assert err == ""
