from abc import ABC, abstractmethod
import typing as t
from random import Random

T = t.TypeVar("T")


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
