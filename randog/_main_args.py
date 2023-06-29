"""
the package contains the Args of module execution and its builder
"""

import argparse
import typing as t
from enum import Enum

import randog.factory
from ._utils.type import positive_int, probability, non_negative_int, datetime


class Subcmd(Enum):
    Byfile = "byfile"
    Bool = "bool"
    Int = "int"
    Float = "float"
    String = "str"
    Decimal = "decimal"
    Datetime = "datetime"


class Args:
    _args: argparse.Namespace

    def __init__(self, argv: t.Sequence[str]):
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
        _add_byfile_parser(subparsers)
        _add_bool_parser(subparsers)
        int_parser = _add_int_parser(subparsers)
        float_parser = _add_float_parser(subparsers)
        _add_str_parser(subparsers)
        decimal_parser = _add_decimal_parser(subparsers)
        datetime_parser = _add_datetime_parser(subparsers)

        self._args = parser.parse_args(argv[1:])

        _validate_int_parser(self, int_parser)
        _validate_float_parser(self, float_parser)
        _validate_decimal_parser(self, decimal_parser)
        _validate_datetime_parser(self, datetime_parser)

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

    def randstr_args(self) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        kwargs = {"charset": self._args.charset}
        if self._args.length is not None:
            if self._args.length[0] == self._args.length[1]:
                kwargs["length"] = self._args.length[0]
            else:
                kwargs["length"] = randog.factory.randint(*self._args.length)

        return tuple(), kwargs

    def randdecimal_args(self) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (self._args.minimum, self._args.maximum), {
            "decimal_len": self._args.decimal_len,
            "p_inf": self._args.p_inf,
            "n_inf": self._args.n_inf,
            "nan": self._args.nan,
        }

    def randdatetime_args(self) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        return (self._args.minimum, self._args.maximum), {}


def _add_common_arguments(parser: argparse.ArgumentParser):
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


def _add_byfile_parser(subparsers):
    byfile_parser = subparsers.add_parser(
        Subcmd.Byfile.value,
        usage="python -m randog byfile FACTORY_PATH [FACTORY_PATH ...] [common-options]",
        description="",  # TODO: implement
        add_help=False,
    )
    byfile_args_group = byfile_parser.add_argument_group("arguments")
    byfile_args_group.add_argument(
        "factories",
        nargs="+",
        metavar="FACTORY_PATH",
        help="path of factory definition files",
    )
    _add_common_arguments(byfile_parser)

    return byfile_parser


def _add_bool_parser(subparsers):
    bool_parser = subparsers.add_parser(
        Subcmd.Bool.value,
        usage="python -m randog int [PROP_TRUE] [common-options]",
        description="",  # TODO: implement
        add_help=False,
    )
    bool_args_group = bool_parser.add_argument_group("arguments")
    bool_args_group.add_argument(
        "prop_true",
        type=probability,
        default=0.5,
        nargs="?",
        metavar="PROP_TRUE",
        help="the probability of True",
    )
    _add_common_arguments(bool_parser)

    return bool_parser


def _add_int_parser(subparsers):
    int_parser = subparsers.add_parser(
        Subcmd.Int.value,
        usage="python -m randog int MINIMUM MAXIMUM [common-options]",
        description="",  # TODO: implement
        add_help=False,
    )
    int_args_group = int_parser.add_argument_group("arguments")
    int_args_group.add_argument(
        "minimum",
        type=int,
        metavar="MINIMUM",
        help="the minimum value",
    )
    int_args_group.add_argument(
        "maximum",
        type=int,
        metavar="MAXIMUM",
        help="the maximum value",
    )
    _add_common_arguments(int_parser)

    return int_parser


def _add_float_parser(subparsers):
    float_parser = subparsers.add_parser(
        Subcmd.Float.value,
        usage="python -m randog float [MINIMUM MAXIMUM] [--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] "
        "[common-options]",
        description="",  # TODO: implement
        add_help=False,
    )
    float_args_group = float_parser.add_argument_group("arguments")
    float_args_group.add_argument(
        "minimum",
        type=float,
        nargs="?",
        metavar="MINIMUM",
        help="the minimum value. "
        "If not specified, the behavior is left to the specification of randog.factory.randfloat.",
    )
    float_args_group.add_argument(
        "maximum",
        type=float,
        nargs="?",
        metavar="MAXIMUM",
        help="the maximum value. "
        "If not specified, the behavior is left to the specification of randog.factory.randfloat.",
    )
    float_args_group.add_argument(
        "--p-inf",
        type=probability,
        default=0.0,
        metavar="PROB_P_INF",
        help="the probability of positive infinity; default=0.0",
    )
    float_args_group.add_argument(
        "--n-inf",
        type=probability,
        default=0.0,
        metavar="PROB_N_INF",
        help="the probability of negative infinity; default=0.0",
    )
    float_args_group.add_argument(
        "--nan",
        type=probability,
        default=0.0,
        metavar="PROB_NAN",
        help="the probability of NaN; default=0.0",
    )
    _add_common_arguments(float_parser)

    return float_parser


def _add_str_parser(subparsers):
    str_parser = subparsers.add_parser(
        Subcmd.String.value,
        usage="python -m randog str [--length LENGTH] [--charset CHARSET] [common-options]",
        description="",  # TODO: implement
        add_help=False,
    )
    str_args_group = str_parser.add_argument_group("arguments")
    str_args_group.add_argument(
        "--length",
        type=non_negative_int_range,
        default=None,
        metavar="LENGTH",
        help="the length of generated strings. "
        "You can specify an integer such as '--length 5' or a range such as '--length 3:8'.",
    )
    str_args_group.add_argument(
        "--charset",
        type=str,
        default=None,
        metavar="CHARSET",
        help="the characters which contained by generated strings",
    )
    _add_common_arguments(str_parser)

    return str_parser


def _add_decimal_parser(subparsers):
    decimal_parser = subparsers.add_parser(
        Subcmd.Decimal.value,
        usage="python -m randog decimal [MINIMUM MAXIMUM] [--decimal-len DECIMAL_LENGTH] "
        "[--p-inf PROB_P_INF] [--n-inf PROB_N_INF] [--nan PROB_NAN] [common-options]",
        description="",  # TODO: implement
        add_help=False,
    )
    decimal_args_group = decimal_parser.add_argument_group("arguments")
    decimal_args_group.add_argument(
        "minimum",
        type=float,
        nargs="?",
        metavar="MINIMUM",
        help="the minimum value. "
        "If not specified, the behavior is left to the specification of randog.factory.randdecimal.",
    )
    decimal_args_group.add_argument(
        "maximum",
        type=float,
        nargs="?",
        metavar="MAXIMUM",
        help="the maximum value. "
        "If not specified, the behavior is left to the specification of randog.factory.randdecimal.",
    )
    decimal_args_group.add_argument(
        "--decimal-len",
        type=non_negative_int,
        default=None,
        metavar="DECIMAL_LENGTH",
        help="the length of decimal part of generated values",
    )
    decimal_args_group.add_argument(
        "--p-inf",
        type=probability,
        default=0.0,
        metavar="PROB_P_INF",
        help="the probability of positive infinity; default=0.0",
    )
    decimal_args_group.add_argument(
        "--n-inf",
        type=probability,
        default=0.0,
        metavar="PROB_N_INF",
        help="the probability of negative infinity; default=0.0",
    )
    decimal_args_group.add_argument(
        "--nan",
        type=probability,
        default=0.0,
        metavar="PROB_NAN",
        help="the probability of NaN; default=0.0",
    )
    _add_common_arguments(decimal_parser)

    return decimal_parser


def _add_datetime_parser(subparsers):
    datetime_parser = subparsers.add_parser(
        Subcmd.Datetime.value,
        usage="python -m randog datetime [MINIMUM MAXIMUM] [common-options]",
        description="",  # TODO: implement
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
    _add_common_arguments(datetime_parser)

    return datetime_parser


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


def _validate_decimal_parser(args: Args, subparser: argparse.ArgumentParser):
    if args.sub_cmd != Subcmd.Decimal:
        return

    iargs, kwargs = args.randdecimal_args()
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


def _validate_datetime_parser(args: Args, subparser: argparse.ArgumentParser):
    if args.sub_cmd != Subcmd.Datetime:
        return

    iargs, kwargs = args.randdatetime_args()
    minimum, maximum = iargs

    if minimum is not None and maximum is not None and minimum > maximum:
        subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")


def non_negative_int_range(value: str) -> t.Tuple[int, int]:
    if ":" in value:
        value_s_str, value_e_str = value.split(":", 1)
        value_s = non_negative_int(value_s_str)
        value_e = non_negative_int(value_e_str)

        if value_s > value_e:
            raise ValueError("range must not be empty")

    else:
        value_s = value_e = non_negative_int(value)

    return value_s, value_e
