"""
the package contains the Args of module execution and its builder
"""

import argparse
import typing as t
from enum import Enum

from ._utils.type import positive_int, probability


class Subcmd(Enum):
    Byfile = "byfile"
    Bool = "bool"
    Int = "int"
    Float = "float"


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
        _add_byfile_parser(subparsers, parent_parser=parent_parser)
        _add_bool_parser(subparsers, parent_parser=parent_parser)
        int_parser = _add_int_parser(subparsers, parent_parser=parent_parser)
        float_parser = _add_float_parser(subparsers, parent_parser=parent_parser)

        self._args = parser.parse_args(argv[1:])

        _validate_int_parser(self, int_parser)
        _validate_float_parser(self, float_parser)

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

    def output_path_for(self, number: int) -> t.Optional[str]:
        if self._args.output is None:
            return None
        else:
            return self._args.output.format(number)

    def randbool_args(self) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (self._args.prop_true,), {}

    def randint_args(self) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (self._args.minimum, self._args.maximum), {}

    def randfloat_args(self) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (self._args.minimum, self._args.maximum), {
            "p_inf": self._args.p_inf,
            "n_inf": self._args.n_inf,
            "nan": self._args.nan,
        }


def _add_byfile_parser(subparsers, *, parent_parser):
    byfile_parser = subparsers.add_parser(
        Subcmd.Byfile.value,
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

    return byfile_parser


def _add_bool_parser(subparsers, *, parent_parser):
    bool_parser = subparsers.add_parser(
        Subcmd.Bool.value,
        parents=[parent_parser],
        usage="python -m randog int [PROP_TRUE] [options]",
        description="",  # TODO: implement
    )
    bool_parser.add_argument(
        "prop_true",
        type=probability,
        default=0.5,
        nargs="?",
        metavar="PROP_TRUE",
        help="the probability of True",
    )

    return bool_parser


def _add_int_parser(subparsers, *, parent_parser):
    int_parser = subparsers.add_parser(
        Subcmd.Int.value,
        parents=[parent_parser],
        usage="python -m randog int MINIMUM MAXIMUM [options]",
        description="",  # TODO: implement
    )
    int_parser.add_argument(
        "minimum",
        type=int,
        metavar="MINIMUM",
        help="the minimum value",
    )
    int_parser.add_argument(
        "maximum",
        type=int,
        metavar="MAXIMUM",
        help="the maximum value",
    )

    return int_parser


def _add_float_parser(subparsers, *, parent_parser):
    float_parser = subparsers.add_parser(
        Subcmd.Float.value,
        parents=[parent_parser],
        usage="python -m randog float MINIMUM MAXIMUM [--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] "
        "[options]",
        description="",  # TODO: implement
    )
    float_parser.add_argument(
        "minimum",
        type=float,
        metavar="MINIMUM",
        help="the minimum value",
    )
    float_parser.add_argument(
        "maximum",
        type=float,
        metavar="MAXIMUM",
        help="the maximum value",
    )
    float_parser.add_argument(
        "--p-inf",
        type=probability,
        default=0.0,
        metavar="PROB_P_INF",
        help="the probability of positive infinity; default=0.0",
    )
    float_parser.add_argument(
        "--n-inf",
        type=probability,
        default=0.0,
        metavar="PROB_N_INF",
        help="the probability of negative infinity; default=0.0",
    )
    float_parser.add_argument(
        "--nan",
        type=probability,
        default=0.0,
        metavar="PROB_NAN",
        help="the probability of NaN; default=0.0",
    )

    return float_parser


def _validate_int_parser(args: Args, subparser: argparse.ArgumentParser):
    if args.sub_cmd != Subcmd.Int:
        return

    iargs, kwargs = args.randint_args()
    minimum, maximum = iargs

    if minimum is not None and maximum is not None and minimum > maximum:
        subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")


def _validate_float_parser(args: Args, subparser: argparse.ArgumentParser):
    if args.sub_cmd != Subcmd.Float:
        return

    iargs, kwargs = args.randfloat_args()
    minimum, maximum = iargs
    nan = kwargs["nan"]
    p_inf = kwargs["p_inf"]
    n_inf = kwargs["n_inf"]

    if minimum is not None and maximum is not None and minimum > maximum:
        subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")

    if nan + p_inf + n_inf > 1.0:
        subparser.error(
            "arguments must satisfy that PROB_P_INF + PROB_N_INF + PROB_NAN <= 1.0"
        )
