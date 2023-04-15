from os import PathLike
import types
import typing as t

from randog.factory import Factory


def from_pyfile(file: t.Union[str, PathLike, t.IO]) -> Factory:
    """Returns a factory defined in the specified file.

    Parameters
    ----------
    file : str | PathLike | IO
        the filename of the factory definition
    """
    if isinstance(file, (str, PathLike)):
        with open(file, mode="rb") as fp:
            return _from_pyfile(fp, file)
    else:
        return _from_pyfile(file, "<io>")


def _from_pyfile(fp: t.IO, filename: t.Union[str, PathLike]) -> Factory:
    import randog

    d = types.ModuleType("factory")
    d.randog = randog
    d.__file__ = filename
    try:
        exec(compile(fp.read(), filename, "exec"), d.__dict__)
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
