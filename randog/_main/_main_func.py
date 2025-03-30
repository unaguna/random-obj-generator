import datetime
import itertools
import json
import os
import random
import sys
import typing as t
import warnings

import randog.factory
from ._subcmd_def.fmt_wrapper import StripWrapper, strip_wrapper
from ._subcmd_def.fmt_wrapper.bytes import BytesWrapper
from ..exceptions import RandogWarning
from .._processmode import Subcmd, set_process_mode
from . import Args, get_subcmd_def
from ._logging import (
    logger,
    apply_stderr_logging_config,
    apply_logging_config_file,
    apply_default_logging_config,
)
from ._rnd import construct_random
from ._warning import apply_formatwarning
from .._utils.exceptions import get_message_recursive
from ..factory import FactoryStopException, FactoryDef, Factory
from .._output import generate_to_csv
from ..postprocess import (
    Base64PostProcess,
    FormatPostProcess,
    IsoFormatPostProcess,
    PicklePostProcess,
)


def _build_factories(
    args: Args,
) -> t.Iterator[
    t.Tuple[
        int,
        str,
        randog.factory.Factory,
        t.Optional[FactoryDef],
    ]
]:
    subcmd_def = get_subcmd_def(args.sub_cmd)
    post_process_of_binary_fmt = _post_process_of_binary_fmt(
        args.binary_fmt,
        strict_type=args.sub_cmd != Subcmd.Byfile,
    )
    post_process_of_value_fmt = _post_process_of_value_fmt(args)

    if args.sub_cmd == Subcmd.Byfile:
        for factory_count, filepath in enumerate(args.factories):
            rnd = construct_random(args.seed)
            if filepath == "-":
                def_file_name = ""
                factory_def = randog.factory.from_pyfile(
                    sys.stdin, full_response=True, rnd=rnd
                )
            else:
                def_file_name = os.path.basename(filepath)
                if def_file_name.endswith(".py"):
                    def_file_name = def_file_name[:-3]
                factory_def = randog.factory.from_pyfile(
                    filepath, full_response=True, rnd=rnd
                )
            factory = factory_def.factory

            if args.pickle:
                # only if --pickle is specified, apply --list before --pickle.
                # It is in order to allow the flow --list -> --pickle -> base64/fmt
                # in order to output pickle of list as base64 or --fmt=x etc.
                if args.list is not None:
                    factory = _IterAsListFactory(
                        factory.post_process(strip_wrapper),
                        length=args.list,
                        regenerate=args.regenerate,
                        discard=args.discard,
                        raise_on_factory_stopped=args.error_on_factory_stopped,
                    )
                factory = factory.post_process(PicklePostProcess()).post_process(
                    BytesWrapper
                )
            if post_process_of_binary_fmt is not None:
                factory = factory.post_process(post_process_of_binary_fmt)
            if post_process_of_value_fmt is not None:
                factory = factory.post_process(post_process_of_value_fmt)
            # if --pickle is not specified, apply --list after --fmt etc.
            if not args.pickle and args.list is not None:
                factory = _IterAsListFactory(
                    factory,
                    length=args.list,
                    regenerate=args.regenerate,
                    discard=args.discard,
                    raise_on_factory_stopped=args.error_on_factory_stopped,
                )

            yield factory_count, def_file_name, factory, factory_def
    else:
        iargs, kwargs = subcmd_def.build_args(args)
        construct_factory = subcmd_def.get_factory_constructor()
        logger.debug(
            "construct factory: %s",
            _repr_function_call(construct_factory, iargs, kwargs),
        )
        factory = construct_factory(*iargs, **kwargs)
        if args.pickle:
            # only if --pickle is specified, apply --list before --pickle.
            # It is in order to allow the flow --list -> --pickle -> base64/fmt
            # in order to output pickle of list as base64 or --fmt=x etc.
            if args.list is not None:
                factory = _IterAsListFactory(
                    factory.post_process(strip_wrapper),
                    length=args.list,
                    regenerate=args.regenerate,
                    discard=args.discard,
                    raise_on_factory_stopped=args.error_on_factory_stopped,
                )
            factory = factory.post_process(
                StripWrapper(PicklePostProcess())
            ).post_process(BytesWrapper)
        if post_process_of_binary_fmt is not None:
            factory = factory.post_process(post_process_of_binary_fmt)
        if post_process_of_value_fmt is not None:
            factory = factory.post_process(post_process_of_value_fmt)
        # if --pickle is not specified, apply --list after --fmt etc.
        if not args.pickle and args.list is not None:
            factory = _IterAsListFactory(
                factory,
                length=args.list,
                regenerate=args.regenerate,
                discard=args.discard,
                raise_on_factory_stopped=args.error_on_factory_stopped,
            )
        yield 0, "", factory, None


class _IterAsListFactory(Factory[t.List]):
    _base: Factory
    _length: int
    _regenerate: float
    _discard: float
    _raise_on_factory_stopped: bool

    def __init__(
        self,
        factory: Factory,
        *,
        length: int,
        regenerate: float,
        discard: float,
        raise_on_factory_stopped: bool,
    ):
        self._base = factory
        self._length = length
        self._regenerate = regenerate
        self._discard = discard
        self._raise_on_factory_stopped = raise_on_factory_stopped

    def _next(self) -> t.List:
        return list(
            self._base.iter(
                self._length,
                regenerate=self._regenerate,
                discard=self._discard,
                raise_on_factory_stopped=self._raise_on_factory_stopped,
            )
        )


def _post_process_of_binary_fmt(
    binary_fmt: t.Optional[str],
    *,
    strict_type: bool,
) -> t.Optional[t.Callable[[t.Any], t.Any]]:
    """callable object to convert bytes to str according binary_fmt"""
    if binary_fmt is None:
        return None
    elif binary_fmt == "base64":
        return StripWrapper(Base64PostProcess(strict_type=strict_type))
    else:
        raise ValueError(f"unknown binary format: {binary_fmt}")


def _post_process_of_value_fmt(
    args: Args,
) -> t.Optional[t.Callable[[t.Any], t.Any]]:
    """callable object to convert value to str according Args.format etc."""
    if args.iso:
        return IsoFormatPostProcess()
    elif args.format:
        return FormatPostProcess(args.format)
    else:
        return None


class _DummyIO:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _open_output_fp(
    args: Args,
    number: int,
    factory_def: t.Optional[FactoryDef],
    *,
    def_file: str,
    repeat_count: int,
    factory_count: int,
    now: datetime.datetime,
    already_written_files: t.MutableSet[str],
) -> t.Union[_DummyIO, t.TextIO]:
    output_path = args.output_path_for(
        number,
        def_file=def_file,
        repeat_count=repeat_count,
        factory_count=factory_count,
        now=now,
        env=os.environ,
    )

    if output_path is None:
        return _DummyIO()
    else:
        options = {}

        if output_path in already_written_files or args.output_appending_mode:
            options["mode"] = "at"
        else:
            options["mode"] = "wt"
            already_written_files.add(output_path)

        if args.get("csv", False):
            options["newline"] = ""
        elif args.output_linesep is not None:
            options["newline"] = args.output_linesep
        elif factory_def is not None and factory_def.output_linesep is not None:
            options["newline"] = factory_def.output_linesep.value

        if args.output_encoding is not None:
            options["encoding"] = args.output_encoding
        elif factory_def is not None and factory_def.output_encoding is not None:
            options["encoding"] = factory_def.output_encoding

        logger.debug(f"open file: {output_path}")

        return open(output_path, **options)


def _output_generated(generated: t.Any, fp: t.TextIO, args: Args):
    if args.output_fmt == "repr":
        print(repr(generated), file=fp)
    elif isinstance(generated, bytes):
        fp.buffer.write(generated)
    elif isinstance(generated, BytesWrapper):
        fp.buffer.write(generated.base)
    elif args.output_fmt == "json":
        json.dump(
            generated,
            fp,
            default=str,
            indent=args.json_indent,
            ensure_ascii=args.json_ensure_ascii,
        )
        fp.write("\n")
    else:
        print(generated, file=fp)


class _Discarded(Exception):
    pass


def _generate_according_args(
    args: Args,
    factory: randog.factory.Factory,
) -> t.Tuple[t.Any, t.Literal["generated", "stop_iter", "discarded"]]:
    """generated a value according arguments

    This method generates values assuming it is not a csv output.

    Parameters
    ----------
    args
        the arguments
    factory
        the factory

    Returns
    -------
    Tuple[Any, Literal["generated", "stop_iter", "discarded"]]
        the generated value and a return type

    Raises
    ------
    RuntimeError
        When CSV output is specified.
        This method generates values assuming it is not a csv output.
    """
    if args.csv:
        raise RuntimeError("cannot use this method if --csv is specified")

    if args.list is not None:
        # If generates test, args.regenerate and args.discard are already attached
        generated = factory.next()
    else:
        try:
            while True:
                generated = factory.next(
                    raise_on_factory_stopped=args.error_on_factory_stopped
                )
                if random.random() >= args.regenerate:
                    break
        except StopIteration:
            return None, "stop_iter"
        if random.random() < args.discard:
            return None, "discarded"

    return generated, "generated"


def _setup_primary_configuration(args: Args):
    """Setup primary python configuration

    It performs a setup that should be performed as soon as the arguments are
    determined in accordance with the python specification.

    This method should be executed once and only once when randog is run as command.

    Parameters
    ----------
    args:
        arguments of command execution
    """

    # setup logging
    if args.log_stderr:
        apply_stderr_logging_config(args.log_stderr, args.log_stderr_is_full)
    elif args.log_config_file:
        try:
            apply_logging_config_file(args.log_config_file)
        except Exception as e:
            logger.error(
                "failed to apply the logging configure file; "
                f"{'; '.join(get_message_recursive(e))}",
            )
            # If yaml is missed, warn about it, as that might cause Exception
            try:
                import yaml

                assert yaml is not None
            except ModuleNotFoundError:
                logger.error(
                    "Are you trying to use YAML format logging configuration? "
                    "If you want to use YAML format configuration files, "
                    "PyYAML must be installed."
                )
            exit(1)
    else:
        apply_default_logging_config()

    # setup warning
    if args.hide_randog_warnings:
        warnings.simplefilter("ignore", RandogWarning)


def main():
    apply_formatwarning()

    args = Args(sys.argv)
    now = datetime.datetime.now()
    set_process_mode(args.sub_cmd)
    already_written_files = set()

    _setup_primary_configuration(args)

    # set environments
    os.environ.update(args.env)

    logger.info(f"run randog with args: {args.commanded_args}")

    try:
        index = 0
        for factory_count, def_file, factory, factory_def in _build_factories(args):
            csv_columns = factory_def.csv_columns if factory_def is not None else None

            for r_index in range(args.repeat):
                with _open_output_fp(
                    args,
                    index,
                    factory_def,
                    def_file=def_file,
                    repeat_count=r_index,
                    factory_count=factory_count,
                    now=now,
                    already_written_files=already_written_files,
                ) as fp_opened:
                    index += 1
                    # args に応じて出力先 fp を決定する。
                    if not isinstance(fp_opened, _DummyIO):
                        fp = fp_opened
                    else:
                        fp = sys.stdout

                    # 生成処理と出力処理
                    # CSV 出力の場合に生成の方法が異なるので、生成と出力をひとまとめにした。
                    if args.csv is not None:
                        if args.output_linesep is not None:
                            output_linesep = args.output_linesep
                        elif (
                            factory_def is not None
                            and factory_def.output_linesep is not None
                        ):
                            output_linesep = factory_def.output_linesep.value
                        else:
                            output_linesep = None
                        generate_to_csv(
                            factory,
                            args.csv,
                            fp,
                            csv_columns=csv_columns,
                            regenerate=args.regenerate,
                            discard=args.discard,
                            raise_on_factory_stopped=args.error_on_factory_stopped,
                            linesep=output_linesep,
                        )
                        logger.debug(
                            "output to CSV; "
                            f"factory_count={factory_count}, repeat_count={r_index}"
                        )
                    else:
                        generated, gen_result = _generate_according_args(args, factory)

                        if gen_result == "stop_iter":
                            break
                        elif gen_result == "discarded":
                            continue
                        else:
                            _output_generated(generated, fp, args=args)
                            logger.debug(
                                "output generated; "
                                f"factory_count={factory_count}, repeat_count={r_index}"
                            )
    except FactoryStopException:
        logger.error("the factory stopped generating before the process was complete")
        exit(1)
    except Exception as e:
        logger.error("; ".join(get_message_recursive(e)), exc_info=e)
        exit(1)


def _repr_function_call(
    func_name: t.Union[str, t.Callable],
    args: t.Sequence[t.Any],
    kwargs: t.Mapping[str, t.Any],
) -> str:
    if not isinstance(func_name, str):
        func_name = getattr(func_name, "__name__", "function")

    args_str = itertools.chain(
        (repr(arg) for arg in args),
        (f"{key}={repr(value)}" for key, value in kwargs.items()),
    )
    return f"{func_name}({', '.join(args_str)})"
