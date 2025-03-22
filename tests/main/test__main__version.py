import sys
from unittest.mock import patch

import pytest

import randog.__main__


def test__main__version(capfd):
    expected_version = randog.__version__
    args = ["randog", "--version"]
    with patch.object(sys, "argv", args):
        with pytest.raises(SystemExit):
            randog.__main__.main()

        out, err = capfd.readouterr()
        assert out == f"randog {expected_version}\n"
        assert err == ""
