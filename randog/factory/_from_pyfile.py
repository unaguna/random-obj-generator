from os import PathLike
import types
import typing as t

from randog.factory import Factory


def from_pyfile(filename: t.Union[str, PathLike]) -> Factory:
    """Returns a factory defined in the specified file.

    Parameters
    ----------
    filename : str | PathLike
        the filename of the factory definition
    """
    d = types.ModuleType("factory")
    d.__file__ = filename
    try:
        with open(filename, mode="rb") as config_file:
            exec(compile(config_file.read(), filename, "exec"), d.__dict__)
    except OSError as e:
        e.strerror = f"Unable to load factory file ({e.strerror})"
        raise

    attr_name = "FACTORY"

    if not hasattr(d, attr_name):
        raise AttributeError(
            f"factory file '{filename}' has no attribute '{attr_name}'"
        )

    factory = getattr(d, attr_name)

    if not isinstance(factory, Factory):
        raise AttributeError(
            f"attribute '{attr_name}' of factory file '{filename}' is not a factory"
        )

    return factory
