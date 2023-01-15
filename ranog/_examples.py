import typing as t


class Example(t.Sequence):
    _objs: t.Sequence

    @t.overload
    def __getitem__(self, index: int) -> t.Any:
        ...

    @t.overload
    def __getitem__(self, index: slice) -> t.Sequence[t.Any]:
        ...

    def __getitem__(self, index: t.Union[int, slice]):
        return self._objs[index]

    def __len__(self) -> int:
        return len(self._objs)

    def __init__(self, *objs):
        self._objs = objs
