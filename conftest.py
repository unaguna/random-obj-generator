import os
from pathlib import Path
import typing as t

import pytest


def pytest_runtest_setup(item):
    for marker in item.iter_markers(name="require_sqlalchemy"):
        __require_sqlalchemy(*marker.args)
    for _ in item.iter_markers(name="require_rstr"):
        __require_rstr()
    for _ in item.iter_markers(name="without_rstr"):
        __without_rstr()


def __require_sqlalchemy(*variants: t.Literal[1, 2]):
    require1 = 1 in variants
    require2 = 2 in variants

    ver_sqlalchemy = __get_version_of_sqlalchemy()

    if require1 and require2:
        if ver_sqlalchemy is None or ver_sqlalchemy[0] not in "12":
            pytest.skip(reason="need sqlalchemy 1 or 2")
    elif require1:
        if ver_sqlalchemy is None or ver_sqlalchemy[0] != "1":
            pytest.skip(reason="need sqlalchemy 1")
    elif require2:
        if ver_sqlalchemy is None or ver_sqlalchemy[0] != "2":
            pytest.skip(reason="need sqlalchemy 2")
    else:
        pass


def __require_rstr():
    if not __exists_rstr():
        pytest.skip(reason="need rstr")


def __without_rstr():
    if __exists_rstr():
        pytest.skip(reason="rstr is installed")


def __get_version_of_sqlalchemy() -> t.Optional[str]:
    try:
        import sqlalchemy
        return sqlalchemy.__version__
    except (ModuleNotFoundError, AttributeError):
        return None


def __exists_rstr() -> bool:
    try:
        import rstr
        return True
    except (ModuleNotFoundError, AttributeError):
        return False


@pytest.fixture
def resources():
    return Path(os.path.dirname(__file__), "tests/resources")
