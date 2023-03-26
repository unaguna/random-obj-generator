import argparse
import sys
import typing as t

import randog.factory


class Args:
    _args: argparse.Namespace

    def __init__(self, argv: t.Sequence[str]):
        parser = argparse.ArgumentParser(description="Create object at random.")
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
        self._args = parser.parse_args(argv[1:])

    @property
    def factories(self) -> t.Sequence[str]:
        return self._args.factories

    @property
    def output_repr(self) -> bool:
        return self._args.repr


def _build_factories(args: Args) -> t.Iterator[randog.factory.Factory]:
    for filepath in args.factories:
        yield randog.factory.from_pyfile(filepath)


def main():
    args = Args(sys.argv)

    for factory in _build_factories(args):
        generated = factory.next()

        if args.output_repr:
            print(repr(generated))
        else:
            print(generated)


if __name__ == "__main__":
    main()
