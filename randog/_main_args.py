"""
the package contains the Args of module execution and its builder
"""

import argparse
import typing as t

from ._utils.type import positive_int


class Args:
    _args: argparse.Namespace

    def __init__(self, argv: t.Sequence[str]):
        parent_parser = argparse.ArgumentParser(add_help=False)
        group_output_fmt = parent_parser.add_mutually_exclusive_group()
        parent_parser.add_argument(
            "--repeat",
            "-r",
            metavar="COUNT",
            default=1,
            type=positive_int,
            help=(
                "repeat generation a specified number of times. "
                "The results are output one by one; if you want them as a single list, use --list instead."
            ),
        )
        parent_parser.add_argument(
            "--list",
            "-L",
            metavar="LENGTH",
            type=positive_int,
            help=(
                "if specified, repeats the specified numerical generation "
                "and returns a list consisting of the results."
            ),
        )
        group_output_fmt.add_argument(
            "--repr",
            dest="output_fmt",
            action="store_const",
            const="repr",
            help="if specified, it outputs generated object by repr()",
        )
        group_output_fmt.add_argument(
            "--json",
            dest="output_fmt",
            action="store_const",
            const="json",
            help="if specified, it outputs generated object by json format",
        )
        parent_parser.add_argument(
            "--output",
            "-O",
            metavar="DESC_PATH",
            help="destination file path",
        )

        parser = argparse.ArgumentParser(
            prog="randog",
            description="Create object at random.",
        )
        subparsers = parser.add_subparsers(
            required=True,
            dest="sub",
            metavar="MODE",
            help="",  # TODO: implement
        )
        byfile_parser = subparsers.add_parser(
            "byfile",
            parents=[parent_parser],
            usage="python -m randog byfile FACTORY_PATH [FACTORY_PATH ...] [options]",
            description="",  # TODO: implement
        )
        byfile_parser.add_argument(
            "factories",
            nargs="+",
            metavar="FACTORY_PATH",
            help="path of factory definition files",
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
    def output_fmt(self) -> t.Optional[str]:
        return self._args.output_fmt

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
