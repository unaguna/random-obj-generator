import sys
from unittest.mock import patch

import randog.__main__


def test__main__option_f(capfd, resources):
    args = ["prog", "-f", str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n"
        assert err == ""


def test__main__option_factory(capfd, resources):
    args = ["prog", "--factory", str(resources.joinpath("factory_def.py"))]
    with patch.object(sys, "argv", args):
        randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == "aaa\n"
        assert err == ""
