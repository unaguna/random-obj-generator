import argparse
import sys
import typing as t

import randog.factory


class Args:
    _args: argparse.Namespace

    def __init__(self, argv: t.Sequence[str]):
        parser = argparse.ArgumentParser(description="Create object at random.")
        parser.add_argument(
            "--factory",
            "-f",
            metavar="FILEPATH",
            required=True,
            help="path of a factory definition file",
        )
        parser.add_argument(
            "--repr",
            action="store_true",
            help="if specified, it outputs generated object by repr()",
        )
        self._args = parser.parse_args(argv[1:])

    @property
    def factory(self) -> str:
        return self._args.factory

    @property
    def output_repr(self) -> bool:
        return self._args.repr


def _build_factory(args: Args):
    return randog.factory.from_pyfile(args.factory)


def main():
    args = Args(sys.argv)

    factory = _build_factory(args)

    generated = factory.next()

    if args.output_repr:
        print(repr(generated))
    else:
        print(generated)


if __name__ == "__main__":
    main()
