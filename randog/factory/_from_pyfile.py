import dataclasses
from os import PathLike
import types
import typing as t

from randog.factory import Factory


@dataclasses.dataclass
class FactoryDef:
    factory: Factory
    csv_columns: t.Optional[t.Sequence[str]]


@t.overload
def from_pyfile(
    file: t.Union[str, PathLike, t.IO], *, full_response: t.Literal[False] = False
) -> Factory:
    pass


@t.overload
def from_pyfile(
    file: t.Union[str, PathLike, t.IO], *, full_response: t.Literal[True]
) -> FactoryDef:
    pass


def from_pyfile(
    file: t.Union[str, PathLike, t.IO],
    *,
    full_response: bool = False,
) -> t.Union[FactoryDef, Factory]:
    """Returns a factory defined in the specified file.

    Parameters
    ----------
    file : str | PathLike | IO
        the filename of the factory definition
    full_response : bool (default=False)
        If True is specified, the return value is the FactoryDef dataclass,
        and data other than the factory can be obtained.
    """
    if isinstance(file, (str, PathLike)):
        with open(file, mode="rb") as fp:
            factory_def = _from_pyfile(fp, file)
    else:
        factory_def = _from_pyfile(file, "<io>")

    if full_response:
        return factory_def
    else:
        return factory_def.factory


FACTORY_ATTR_NAME = "FACTORY"
CSV_COL_ATTR_NAME = "CSV_COLUMNS"


def _from_pyfile(fp: t.IO, filename: t.Union[str, PathLike]) -> FactoryDef:
    import randog

    d = types.ModuleType("factory")
    d.randog = randog
    d.__file__ = filename
    try:
        exec(compile(fp.read(), filename, "exec"), d.__dict__)
    except OSError as e:
        e.strerror = f"Unable to load factory file ({e.strerror})"
        raise

    return _load_factory_module(d, filename=filename)


def _load_factory_module(
    module: types.ModuleType, *, filename: t.Union[str, PathLike]
) -> FactoryDef:
    if not hasattr(module, FACTORY_ATTR_NAME):
        raise AttributeError(
            f"factory file '{filename}' has no attribute '{FACTORY_ATTR_NAME}'"
        )

    factory = getattr(module, FACTORY_ATTR_NAME)
    if not isinstance(factory, Factory):
        raise AttributeError(
            f"attribute '{FACTORY_ATTR_NAME}' of factory file '{filename}' is not a factory"
        )

    csv_columns = getattr(module, CSV_COL_ATTR_NAME, None)
    if csv_columns is not None and not isinstance(csv_columns, t.Sequence):
        raise AttributeError(
            f"attribute '{CSV_COL_ATTR_NAME}' of factory file '{filename}' MUST be None or a sequence of strings"
        )

    return FactoryDef(
        factory=factory,
        csv_columns=csv_columns,
    )
