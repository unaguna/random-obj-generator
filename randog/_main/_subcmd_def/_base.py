import argparse
from abc import ABC, abstractmethod
import typing as t

from ..._utils.type import positive_int
from .._subcmd import Subcmd
from .._main_args import Args


class SubcmdDef(ABC):
    @abstractmethod
    def cmd(self) -> Subcmd:
        ...

    @abstractmethod
    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        ...

    @abstractmethod
    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        ...

    @abstractmethod
    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        ...

    @abstractmethod
    def get_factory_constructor(self) -> t.Callable:
        ...


def add_common_arguments(parser: argparse.ArgumentParser):
    common_opt_group = parser.add_argument_group("common-options")
    other_opt_group = parser.add_argument_group("other options")
    group_output_fmt = common_opt_group.add_mutually_exclusive_group()
    common_opt_group.add_argument(
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
    common_opt_group.add_argument(
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
    common_opt_group.add_argument(
        "--output",
        "-O",
        metavar="DESC_PATH",
        help="destination file path",
    )
    other_opt_group.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
