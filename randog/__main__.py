import csv
import json
import os
import random
import sys
import typing as t

import randog.factory
from .factory import FactoryDef, FactoryStopException
from ._main import Args, Subcmd, get_subcmd_def


def _build_factories(
    args: Args,
) -> t.Iterator[t.Tuple[int, str, randog.factory.Factory]]:
    subcmd_def = get_subcmd_def(args.sub_cmd)

    if args.sub_cmd == Subcmd.Byfile:
        for factory_count, filepath in enumerate(args.factories):
            if filepath == "-":
                def_file_name = ""
                factory_def = randog.factory.from_pyfile(sys.stdin, full_response=True)
            else:
                def_file_name = os.path.basename(filepath)
                if def_file_name.endswith(".py"):
                    def_file_name = def_file_name[:-3]
                factory_def = randog.factory.from_pyfile(filepath, full_response=True)
            factory = factory_def.factory

            post_process = _gen_post_function(args, factory_def)
            if post_process is not None:
                factory = factory.post_process(post_process)

            yield factory_count, def_file_name, factory
    else:
        iargs, kwargs = subcmd_def.build_args(args)
        yield 0, "", subcmd_def.get_factory_constructor()(*iargs, **kwargs)


def _get_csv_field(pre_value: t.Mapping, col) -> t.Any:
    if isinstance(col, t.Callable):
        return col(pre_value)
    else:
        return pre_value.get(col)


def _gen_post_function(
    args: Args, factory_def: FactoryDef
) -> t.Optional[t.Callable[[t.Any], t.Any]]:
    """args に応じて、factory_def.factory に適用する post_process 関数を作成する。"""

    # CSV 出力の場合、CSVの行 (Sequence[Any]) を生成するような post_process を作成する。
    if args.get("csv", False):
        if factory_def.csv_columns is not None:

            def _post_function(pre_value) -> t.Optional[t.Sequence[t.Any]]:
                if pre_value is None:
                    return None
                elif isinstance(pre_value, t.Mapping):
                    return [
                        _get_csv_field(pre_value, col)
                        for col in factory_def.csv_columns
                    ]
                elif isinstance(pre_value, t.Sequence):
                    return pre_value
                else:
                    # TODO: 警告
                    return [pre_value]

        else:

            def _post_function(pre_value) -> t.Optional[t.Sequence[t.Any]]:
                if pre_value is None:
                    return None
                elif isinstance(pre_value, t.Mapping):
                    # TODO: 警告
                    return list(pre_value.values())
                elif isinstance(pre_value, t.Sequence) and not isinstance(
                    pre_value, str
                ):
                    return pre_value
                else:
                    # TODO: 警告
                    return [pre_value]

        return _post_function
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
    *,
    def_file: str,
    repeat_count: int,
    factory_count: int,
) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None:
        return _DummyIO()
    else:
        options = {
            "mode": "at",
        }

        if args.get("csv", False):
            options["newline"] = ""
        elif args.output_linesep is not None:
            options["newline"] = args.output_linesep

        if args.output_encoding is not None:
            options["encoding"] = args.output_encoding

        return open(
            args.output_path_for(
                number,
                def_file=def_file,
                repeat_count=repeat_count,
                factory_count=factory_count,
            ),
            **options,
        )


def _output_generated(generated: t.Any, fp: t.TextIO, args: Args):
    if args.output_fmt == "repr":
        print(repr(generated), file=fp)
    elif args.output_fmt == "json":
        json.dump(generated, fp, default=_json_default(args))
        fp.write("\n")
    else:
        if args.iso and hasattr(generated, "isoformat"):
            print(generated.isoformat(), file=fp)
        elif args.format:
            print(generated.__format__(args.format), file=fp)
        else:
            print(generated, file=fp)


def _json_default(args: Args):
    if args.iso:
        return lambda v: v.isoformat()
    elif args.format:
        return lambda v: v.__format__(args.format)
    else:
        return str


def _output_to_csv(
    factory: randog.factory.Factory[t.Optional[t.Sequence[t.Sequence[t.Any]]]],
    line_num: int,
    fp: t.TextIO,
    regenerate: float,
    discard: float,
    raise_on_factory_stopped: bool,
    linesep: t.Optional[str],
):
    writer_options = {}
    if fp in (sys.stdout, sys.stderr):
        # windows で "\r\n" にすると、標準出力時に改行が "\r\r\n" に変換されてしまう。
        # よって、windows で改行を "\r\n" にしたい場合も、標準出力時はここには　"\n" を指定する。
        writer_options["lineterminator"] = "\n"
    elif linesep is None:
        writer_options["lineterminator"] = os.linesep
    else:
        writer_options["lineterminator"] = linesep

    csv_writer = csv.writer(fp, **writer_options)
    csv_writer.writerows(
        filter(
            lambda x: x is not None,
            factory.iter(
                line_num,
                regenerate=regenerate,
                discard=discard,
                raise_on_factory_stopped=raise_on_factory_stopped,
            ),
        )
    )


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
        generated = list(
            factory.iter(
                args.list,
                regenerate=args.regenerate,
                discard=args.discard,
                raise_on_factory_stopped=args.error_on_factory_stopped,
            )
        )
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


def main():
    args = Args(sys.argv)

    try:
        index = 0
        for factory_count, def_file, factory in _build_factories(args):
            for r_index in range(args.repeat):
                with _open_output_fp(
                    args,
                    index,
                    def_file=def_file,
                    repeat_count=r_index,
                    factory_count=factory_count,
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
                        _output_to_csv(
                            factory,
                            args.csv,
                            fp,
                            regenerate=args.regenerate,
                            discard=args.discard,
                            raise_on_factory_stopped=args.error_on_factory_stopped,
                            linesep=args.output_linesep,
                        )
                    else:
                        generated, gen_result = _generate_according_args(args, factory)

                        if gen_result == "stop_iter":
                            break
                        elif gen_result == "discarded":
                            continue
                        else:
                            _output_generated(generated, fp, args=args)
    except FactoryStopException:
        print(
            "error: the factory stopped generating before the process was complete",
            file=sys.stderr,
        )
        exit(1)


if __name__ == "__main__":
    main()
