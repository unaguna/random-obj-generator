import argparse
import sys
import typing as t

import randog.factory


class Args:
    _args: argparse.Namespace

    def __init__(self, argv: t.Sequence[str]):
        parser = argparse.ArgumentParser(
            usage="python -m randog [options] FACTORY_PATH [FACTORY_PATH ...]",
            description="Create object at random.",
        )
        parser.add_argument(
            "factories",
            nargs="+",
            metavar="FACTORY_PATH",
            help="path of factory definition files",
        )
        parser.add_argument(
            "--repr",
            action="store_true",
            help="if specified, it outputs generated object by repr()",
        )
        parser.add_argument(
            "--output",
            "-O",
            metavar="DESC_PATH",
            help="destination file path",
        )
        self._args = parser.parse_args(argv[1:])

    @property
    def factories(self) -> t.Sequence[str]:
        return self._args.factories

    @property
    def output_repr(self) -> bool:
        return self._args.repr

    @property
    def output_path(self) -> t.Optional[str]:
        return self._args.output

    @property
    def multiple_output_path(self) -> bool:
        if self._args.output is None:
            return False
        else:
            return self.output_path_for(1) != self.output_path_for(2)

    def output_path_for(self, number: int) -> t.Optional[str]:
        if self._args.output is None:
            return None
        else:
            return self._args.output.format(number)


def _build_factories(args: Args) -> t.Iterator[randog.factory.Factory]:
    for filepath in args.factories:
        yield randog.factory.from_pyfile(filepath)


class _DummyIO:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _open_output_fp(args: Args) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None:
        return _DummyIO()
    else:
        return open(args.output_path, mode="wt")
        pass


def _open_output_fp_numbered(args: Args, number: int) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None:
        return _DummyIO()
    else:
        return open(args.output_path_for(number), mode="wt")


def _output_generated(generated: t.Any, fp: t.Union[_DummyIO, t.TextIO], args: Args):
    if isinstance(fp, _DummyIO):
        fp = sys.stdout

    if args.output_repr:
        print(repr(generated), file=fp)
    else:
        print(generated, file=fp)


def main():
    args = Args(sys.argv)

    for index, factory in enumerate(_build_factories(args)):
        generated = factory.next()

        with _open_output_fp_numbered(args, index) as fp_numbered:
            _output_generated(generated, fp_numbered, args=args)


if __name__ == "__main__":
    main()
