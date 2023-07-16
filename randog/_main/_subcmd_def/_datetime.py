import argparse
import typing as t

import randog.factory
from ..._utils.type import datetime
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments


class SubcmdDefDatetime(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Datetime

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        datetime_parser = subparsers.add_parser(
            Subcmd.Datetime.value,
            usage="python -m randog datetime [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] [common-options]",
            description="It generates values of type datetime.datetime.",
            add_help=False,
        )
        datetime_args_group = datetime_parser.add_argument_group("arguments")
        datetime_args_group.add_argument(
            "minimum",
            type=datetime,
            nargs="?",
            metavar="MINIMUM",
            help="the minimum value with the ISO-8601 format. "
            "If not specified, the behavior is left to the specification of randog.factory.randdatetime.",
        )
        datetime_args_group.add_argument(
            "maximum",
            type=datetime,
            nargs="?",
            metavar="MAXIMUM",
            help="the maximum value with the ISO-8601 format. "
            "If not specified, the behavior is left to the specification of randog.factory.randdatetime.",
        )
        group_date_fmt = datetime_args_group.add_mutually_exclusive_group()
        group_date_fmt.add_argument(
            "--iso",
            action="store_true",
            help="if specified, it outputs generated object with ISO-8601 format",
        )
        group_date_fmt.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated object with the specified format, "
            "such as '%%Y/%%m/%%d %%H:%%M:%%S.%%f'",
        )
        add_common_arguments(datetime_parser)

        return datetime_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Datetime:
            return

        iargs, kwargs = self.build_args(args)
        minimum, maximum = iargs

        if minimum is not None and maximum is not None and minimum > maximum:
            subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")

        if args.output_fmt == "repr" and args.iso:
            subparser.error("argument --iso: not allowed with argument --repr")
        elif args.output_fmt == "repr" and args.format:
            subparser.error("argument --fmt: not allowed with argument --repr")

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (args.get("minimum"), args.get("maximum")), {}

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randdatetime
