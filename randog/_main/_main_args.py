"""
the package contains the Args of module execution and its builder
"""

import argparse
import typing as t

from ._subcmd import Subcmd


class Args:
    _args: argparse.Namespace

    def __init__(self, argv: t.Sequence[str]):
        from ._subcmd_def import iter_subcmd_def

        parser = argparse.ArgumentParser(
            prog="randog",
            description="It generates values randomly according to the specified mode and arguments.",
        )
        subparsers = parser.add_subparsers(
            required=True,
            dest="sub",
            metavar="MODE",
            help=f"mode of value generation; candidates: {', '.join(map(lambda c: c.value, Subcmd))}. "
            "For more information, see the command 'randog MODE --help'.",
        )

        # create subcommands and add them to the ArgumentParser
        subcmd_parsers = {}
        for subcmd in iter_subcmd_def():
            subcmd_parsers[subcmd.cmd()] = subcmd.add_parser(subparsers)

        # parse the arguments
        self._args = parser.parse_args(argv[1:])

        # validate arguments for subcommands
        for subcmd in iter_subcmd_def():
            subcmd.validate_parser(self, subcmd_parsers[subcmd.cmd()])

    @property
    def sub_cmd(self) -> Subcmd:
        return Subcmd(self._args.sub)

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

    @property
    def iso(self) -> bool:
        if hasattr(self._args, "iso"):
            return self._args.iso
        else:
            return False

    @property
    def format(self) -> t.Optional[str]:
        if hasattr(self._args, "format"):
            return self._args.format
        else:
            return None

    @property
    def regenerate(self) -> float:
        if hasattr(self._args, "regenerate"):
            return self._args.regenerate
        else:
            return 0.0

    @property
    def discard(self) -> float:
        if hasattr(self._args, "discard"):
            return self._args.discard
        else:
            return 0.0

    @property
    def csv(self) -> t.Optional[int]:
        if hasattr(self._args, "csv"):
            return self._args.csv
        else:
            return None

    def output_path_for(self, number: int) -> t.Optional[str]:
        if self._args.output is None:
            return None
        else:
            return self._args.output.format(number)

    def get(self, key: str, default: t.Any = None) -> t.Any:
        if hasattr(self._args, key):
            return getattr(self._args, key)
        else:
            return default
