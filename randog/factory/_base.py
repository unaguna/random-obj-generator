import random
from abc import ABC, abstractmethod
import typing as t
from fractions import Fraction
from random import Random

from .._utils.nullsafe import dfor

T = t.TypeVar("T")
R = t.TypeVar("R")

REGENERATE_PROB_MAX = float(Fraction(1023, 1024))


class Factory(ABC, t.Generic[T]):
    @abstractmethod
    def next(self) -> T:
        """Generate a value randomly according to the rules specified when assembling the factory.

        Returns
        -------
        T
            a value generated randomly
        """
        pass

    def or_none(
        self,
        prob: float = 0.1,
        *,
        lazy_choice: bool = False,
        rnd: t.Optional[Random] = None,
    ) -> "Factory[t.Union[T, None]]":
        """Returns a factory whose result may be None with the specified probability.

        Examples
        --------
        >>> import randog
        >>>
        >>> factory = randog.factory.randstr().or_none(0.2)
        >>>
        >>> generated = factory.next()
        >>> assert generated is None or isinstance(generated, str)

        Parameters
        ----------
        prob : float, default=0.1
            Probability that the result is None
        lazy_choice : bool, optional
            If it is True, when generating a value,
            first generate value with the base factory and then decides whether to adopt it or None.
            Otherwise, it first decides whether to return None or generate a value and return it,
            and then generates a value only if it is returned.
        rnd : Random, optional
            random number generator to be used

        Returns
        -------
        Factory[T|None]
            A factory whose result may be None with the specified probability.
        """
        import randog.factory

        return randog.factory.union(
            self,
            randog.factory.const(None),
            weights=[1 - prob, prob],
            lazy_choice=lazy_choice,
            rnd=rnd,
        )

    def post_process(self, post_process: t.Callable[[T], R]) -> "Factory[R]":
        """Returns a factory whose result will be modified by `post_process`

        Examples
        --------
        >>> import randog
        >>>
        >>> # use post_process to format the random decimal value
        >>> factory = (
        ...     randog.factory.randdecimal(0, 50000, decimal_len=2)
        ...                  .post_process(lambda x: f"${x:,}")
        ... )
        >>>
        >>> # examples: '$12,345.67', '$3,153.21', '$12.90', etc.
        >>> generated = factory.next()
        >>> assert isinstance(generated, str)
        >>> assert generated[0] == "$"

        Parameters
        ----------
        post_process : Callable[[T], R]
            the mapping to modify the result

        Returns
        -------
        Factory[R]
            A factory whose result will be modified by `post_process`.
        """
        return PostFactory(self, post_process)

    def iter(
        self,
        size: int,
        *,
        regenerate: float = 0.0,
        discard: float = 0.0,
        rnd: t.Optional[Random] = None,
    ) -> t.Iterator[T]:
        """Returns an iterator which serves result randomly `size` times.

        Examples
        --------
        >>> import randog
        >>> factory = randog.factory.randstr(length=5)
        >>>
        >>> for result in factory.iter(10):
        ...     assert isinstance(result, str)
        >>>
        >>> results = list(factory.iter(5))
        >>> assert len(results) == 5

        Parameters
        ----------
        size : int
            the number of the iterator
        regenerate : float, default=0.0
            the probability that the original factory generation value is not returned as is, but is regenerated.
            It affects cases where the original factory returns a value that is not completely random.
        discard : float, default=0.0
            the probability that the original factory generation value is not returned as is, but is discarded.
            If discarded, the number of times the value is generated is less than `size`.
        rnd : Random, optional
            random number generator to be used

        Returns
        -------
        Iterator[T]
            An iterator
        """
        return FactoryIter(self, size, regenerate=regenerate, discard=discard, rnd=rnd)

    def infinity_iter(
        self,
        *,
        regenerate: float = 0.0,
        rnd: t.Optional[Random] = None,
    ) -> t.Iterator[T]:
        """Returns an infinity iterator which serves result randomly.

        The result is INFINITY so do NOT use it directly with `for`, `list`, and so on.

        Examples
        --------
        >>> import randog
        >>> factory = randog.factory.randstr(length=5)
        >>>
        >>> keys = ["foo", "bar"]
        >>> for k, v in zip(keys, factory.infinity_iter()):
        ...     assert k in keys
        ...     assert isinstance(v, str)

        Parameters
        ----------
        regenerate : float, default=0.0
            the probability that the original factory generation value is not returned as is, but is regenerated.
            It affects cases where the original factory returns a value that is not completely random.
        rnd : Random, optional
            random number generator to be used

        Returns
        -------
        Iterator[T]
            An infinity iterator
        """
        return FactoryIter(self, None, regenerate=regenerate, rnd=rnd)


class PostFactory(Factory[R], t.Generic[T, R]):
    _base_factory: Factory[T]
    _post_process: t.Callable[[T], R]

    def __init__(self, base_factory: Factory[T], post_process: t.Callable[[T], R]):
        self._base_factory = base_factory
        self._post_process = post_process

    def next(self) -> R:
        pre_result = self._base_factory.next()
        return self._post_process(pre_result)


class FactoryIter(t.Generic[T], t.Iterator[T]):
    _rnd: random.Random
    _factory: Factory[T]
    _size: t.Union[int, float]
    _regenerate_prob: float
    _discard_prob: float
    _count: int = 0

    def __init__(
        self,
        factory: Factory[T],
        size: t.Union[int, None],
        *,
        regenerate: float = 0.0,
        discard: float = 0.0,
        rnd: t.Optional[Random] = None,
    ):
        self._rnd = dfor(rnd, random.Random())
        self._factory = factory

        if regenerate > 0 and discard > 0:
            raise ValueError(
                "`regenerate` and `discard` cannot be specified at the same time"
            )
        if regenerate < 0 or REGENERATE_PROB_MAX < regenerate:
            raise ValueError(
                "the probability `regenerate` must range from 0 to 1023/1024"
            )
        if discard < 0 or 1 < discard:
            raise ValueError("the probability `discard` must range from 0 to 1")

        self._size = size if size is not None else float("Infinity")
        self._regenerate_prob = regenerate
        self._discard_prob = discard

    def __next__(self) -> T:
        while True:
            if self._count >= self._size:
                raise StopIteration()

            self._count += 1

            # Regenerate until break
            while True:
                generated = self._factory.next()
                if (
                    self._regenerate_prob <= 0
                    or self._rnd.random() >= self._regenerate_prob
                ):
                    break

            # Probabilistically, discard the value generated this time and proceed to the next one
            if self._discard_prob > 0 and self._rnd.random() < self._discard_prob:
                continue

            return generated
