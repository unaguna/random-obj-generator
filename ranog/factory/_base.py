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
        import ranog.factory

        return ranog.factory.union(
            self,
            ranog.factory.const(None),
            weights=[1 - prob, prob],
            rnd=rnd,
        )

    def post_process(self, post_process: t.Callable[[T], R]) -> "Factory[R]":
        """Returns a factory whose result will be modified by `post_process`

        Examples
        --------
        >>> import ranog
        >>>
        >>> factory = ranog.factory.randstr(length=9).post_process(lambda v: v + v[0])
        >>>
        >>> generated = factory.next()
        >>>
        >>> assert len(generated) == 10
        >>> assert generated[0] == generated[-1]

        Parameters
        ----------
        post_process
            the mapping to modify the result

        Returns
        -------
        A factory whose result will be modified by `post_process`.
        """
        return PostFactory(self, post_process)


class PostFactory(Factory[R], t.Generic[T, R]):
    _base_factory: Factory[T]
    _post_process: t.Callable[[T], R]

    def __init__(self, base_factory: Factory[T], post_process: t.Callable[[T], R]):
        self._base_factory = base_factory
        self._post_process = post_process

    def next(self) -> R:
        pre_result = self._base_factory.next()
        return self._post_process(pre_result)
