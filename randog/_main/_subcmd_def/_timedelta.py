import argparse
import datetime
import typing as t

import randog.factory
from ..._utils.type import timedelta
from ... import timedelta_util
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments


class SubcmdDefTimedelta(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Timedelta

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        timedelta_parser = subparsers.add_parser(
            Subcmd.Timedelta.value,
            usage="python -m randog timedelta [MINIMUM MAXIMUM] [--iso] [common-options]",
            description="",  # TODO: implement
            add_help=False,
        )
        timedelta_args_group = timedelta_parser.add_argument_group("arguments")
        timedelta_args_group.add_argument(
            "minimum",
            type=timedelta,
            nargs="?",
            metavar="MINIMUM",
            help="the minimum value with the simple format such as '1d20h30m40s'. "
            "If not specified, the behavior is left to the specification of randog.factory.randtimedelta.",
        )
        timedelta_args_group.add_argument(
            "maximum",
            type=timedelta,
            nargs="?",
            metavar="MAXIMUM",
            help="the maximum value with the simple format such as '1d20h30m40s'. "
            "If not specified, the behavior is left to the specification of randog.factory.randtimedelta.",
        )
        group_date_fmt = timedelta_args_group.add_mutually_exclusive_group()
        group_date_fmt.add_argument(
            "--iso",
            action="store_true",
            help="if specified, it outputs generated object with ISO-8601 format",
        )
        group_date_fmt.add_argument(
            "--fmt",
            dest="date_fmt",
            metavar="FORMAT",
            help="if specified, it outputs generated object with the specified format, "
            "such as '%%tH:%%M:%%S.%%f'",
        )
        add_common_arguments(timedelta_parser)

        return timedelta_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Timedelta:
            return

        iargs, kwargs = self.build_args(args)
        minimum, maximum = iargs

        if minimum is not None and maximum is not None and minimum > maximum:
            subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")

        if args.output_fmt == "repr" and args.iso:
            subparser.error("argument --iso: not allowed with argument --repr")
        elif args.output_fmt == "repr" and args.date_fmt:
            subparser.error("argument --fmt: not allowed with argument --repr")

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (args.get("minimum"), args.get("maximum")), {}

    def get_factory_constructor(self) -> t.Callable:
        return lambda *a, **kw: randog.factory.randtimedelta(*a, **kw).post_process(
            _TimedeltaWrapper
        )


class _TimedeltaWrapper(datetime.timedelta):
    _base: datetime.timedelta

    def __new__(cls, base: datetime.timedelta):
        ins = super(_TimedeltaWrapper, cls).__new__(
            cls,
            days=base.days,
            seconds=base.seconds,
            microseconds=base.microseconds,
        )
        ins._base = base
        return ins

    def __str__(self):
        return timedelta_util.to_str(self)

    def __repr__(self):
        return repr(self._base)
