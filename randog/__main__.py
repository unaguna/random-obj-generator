import json
import sys
import typing as t

import randog.factory
from randog._main_args import Args, Subcmd


def _build_factories(args: Args) -> t.Iterator[randog.factory.Factory]:
    if args.sub_cmd == Subcmd.Byfile:
        for filepath in args.factories:
            if filepath == "-":
                yield randog.factory.from_pyfile(sys.stdin)
            else:
                yield randog.factory.from_pyfile(filepath)
    elif args.sub_cmd == Subcmd.Bool:
        iargs, kwargs = args.randbool_args()
        yield randog.factory.randbool(*iargs, **kwargs)
    elif args.sub_cmd == Subcmd.Int:
        iargs, kwargs = args.randint_args()
        yield randog.factory.randint(*iargs, **kwargs)


class _DummyIO:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _open_output_fp_only(args: Args) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or args.multiple_output_path:
        return _DummyIO()
    else:
        return open(args.output_path, mode="wt")


def _open_output_fp_numbered(args: Args, number: int) -> t.Union[_DummyIO, t.TextIO]:
    if args.output_path is None or not args.multiple_output_path:
        return _DummyIO()
    else:
        return open(args.output_path_for(number), mode="wt")


def _output_generated(generated: t.Any, fp: t.TextIO, args: Args):
    if args.output_fmt == "repr":
        print(repr(generated), file=fp)
    elif args.output_fmt == "json":
        json.dump(generated, fp, default=str)
        fp.write("\n")
    else:
        print(generated, file=fp)


def main():
    args = Args(sys.argv)

    with _open_output_fp_only(args) as fp_only:
        index = 0
        for factory in _build_factories(args):
            for r_index in range(args.repeat):
                if args.list is None:
                    generated = factory.next()
                else:
                    generated = list(factory.iter(args.list))

                with _open_output_fp_numbered(args, index) as fp_numbered:
                    if not isinstance(fp_numbered, _DummyIO):
                        fp = fp_numbered
                    elif not isinstance(fp_only, _DummyIO):
                        fp = fp_only
                    else:
                        fp = sys.stdout

                    _output_generated(generated, fp, args=args)

                index += 1


if __name__ == "__main__":
    main()
