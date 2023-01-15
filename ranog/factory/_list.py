import typing as t
from random import Random

from ._base import Factory


def randlist(
    *items: Factory,
    length: t.Optional[int] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[list]:
    """Return a factory generating random list.

    Parameters
    ----------
    items : Factory
        the factories of each item
    length : int, optional
        length of generated list.
        If not specified, the length of generated list will be equals to the number of `items`.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    pass
