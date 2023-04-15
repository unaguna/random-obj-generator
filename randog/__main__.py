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
            "--repeat",
            "-r",
            metavar="COUNT",
            default=1,
            type=int,
            help=(
                "repeat generation a specified number of times. "
                "The results are output one by one; if you want them as a single list, use --list instead."
            ),
        )
        parser.add_argument(
            "--list",
            metavar="LENGTH",
            type=int,
            help=(
                "if specified, repeats the specified numerical generation "
                "and returns a list consisting of the results."
            ),
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
    def repeat(self) -> int:
        return self._args.repeat

    @property
    def list(self) -> t.Optional[int]:
        return self._args.list

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


def _open_output_fp_only(args: Args) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or args.multiple_output_path:
        return _DummyIO()
    else:
        return open(args.output_path, mode="wt")


def _open_output_fp_numbered(args: Args, number: int) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or not args.multiple_output_path:
        return _DummyIO()
    else:
        return open(args.output_path_for(number), mode="wt")


def _output_generated(generated: t.Any, fp: t.TextIO, args: Args):
    if args.output_repr:
        print(repr(generated), file=fp)
    else:
        print(generated, file=fp)


def main():
    args = Args(sys.argv)

    with _open_output_fp_only(args) as fp_only:
        index = 0
        for factory in _build_factories(args):
            for r_index in range(args.repeat):
                if args.list is None:
                    generated = factory.next()
                else:
                    generated = list(factory.iter(args.list))

                with _open_output_fp_numbered(args, index) as fp_numbered:
                    if not isinstance(fp_numbered, _DummyIO):
                        fp = fp_numbered
                    elif not isinstance(fp_only, _DummyIO):
                        fp = fp_only
                    else:
                        fp = sys.stdout

                    _output_generated(generated, fp, args=args)

                index += 1


if __name__ == "__main__":
    main()
