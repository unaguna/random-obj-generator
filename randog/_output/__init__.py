import csv
import os
import sys
import typing as t

from ..factory import Factory


def generate_to_csv(
    factory: Factory,
    line_num: int,
    fp: t.TextIO,
    regenerate: float = 0.0,
    discard: float = 0.0,
    raise_on_factory_stopped: bool = False,
    linesep: t.Optional[str] = None,
):
    """Generate values randomly and output as CSV

    Parameters
    ----------
    factory : Factory
        the factory to generate values
    line_num : int
        the number of the iterator.
        However, if the argument `raise_on_factory_stopped` is not True,
        fewer iterations than the specified `size` will be executed
        if the factory is stopped.
        Also, if the argument `discard` is specified, the size may be less.
    fp : TextIO
        CSV output destination
    regenerate : float, default=0.0
        the probability that the original factory generation value is not returned
        as is, but is regenerated.
        It affects cases where the original factory returns a value
        that is not completely random.
    discard : float, default=0.0
        the probability that the original factory generation value is not returned
        as is, but is discarded.
        If discarded, the number of times the value is generated is less than
        `size`.
    raise_on_factory_stopped : bool, default=False
        If True, raises `FactoryStopException`
        in case the factory cannot generate value due to `StopIteration`.
        If False, simply raises `StopIteration`.
    linesep : str, optional
        If specified, CSV rows are separated by this string.
    """
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
