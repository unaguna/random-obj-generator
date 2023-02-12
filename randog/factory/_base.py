from abc import ABC, abstractmethod
import typing as t
from random import Random

T = t.TypeVar("T")
R = t.TypeVar("R")


class Factory(ABC, t.Generic[T]):
    @abstractmethod
    def next(self) -> T:
        pass

    def or_none(
        self,
        prob: float = 0.1,
        *,
        rnd: t.Optional[Random] = None,
    ) -> "Factory[t.Union[T, None]]":
        import randog.factory

        return randog.factory.union(
            self,
            randog.factory.const(None),
            weights=[1 - prob, prob],
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
        post_process
            the mapping to modify the result

        Returns
        -------
        A factory whose result will be modified by `post_process`.
        """
        return PostFactory(self, post_process)

    def iter(self, size: int) -> t.Iterator[T]:
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
        size
            the number of the iterator

        Returns
        -------
        An iterator
        """
        for _ in range(size):
            yield self.next()

    def infinity_iter(self) -> t.Iterator[T]:
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

        Returns
        -------
        An infinity iterator
        """
        while True:
            yield self.next()


class PostFactory(Factory[R], t.Generic[T, R]):
    _base_factory: Factory[T]
    _post_process: t.Callable[[T], R]

    def __init__(self, base_factory: Factory[T], post_process: t.Callable[[T], R]):
        self._base_factory = base_factory
        self._post_process = post_process

    def next(self) -> R:
        pre_result = self._base_factory.next()
        return self._post_process(pre_result)
