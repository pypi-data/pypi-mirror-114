import builtins
import time
from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from typing import Optional

from enilm.reports.sys import print_mem
from pydantic import BaseModel

@contextmanager
def redirect_stdout_file(file: Path):
    fp = open(file, 'w')
    try:
        # https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout
        with redirect_stdout(fp):
            yield
    finally:
        fp.close()


class SectionOptions(BaseModel):
    header: Optional[str] = None
    n_spaces: int = 2
    mem: bool = False
    timing: bool = False
    redirect_stdout_file: Optional[Path] = None


@contextmanager
def sec(opts: SectionOptions = None, **kwargs):
    # opts or kwargs
    if opts is None:
        opts = SectionOptions.parse_obj(kwargs)

    # new print with spaces
    original_print = builtins.print

    def custom_print(*args, **kwargs):
        original_print(' ' * opts.n_spaces, end='')
        original_print(*args, **kwargs)

    # record timing
    start_time = None
    try:
        # header
        if opts.header is not None:
            print(opts.header)

        # memory
        if opts.mem:
            print_mem()

        # timing
        if opts.timing:
            start_time = time.perf_counter()

        # replace print
        builtins.print = custom_print

        # to file?
        if opts.redirect_stdout_file is not None:
            with redirect_stdout_file(opts.redirect_stdout_file):
                yield
        else:
            yield
    finally:
        # restore print
        builtins.print = original_print

        # print timing
        if opts.timing:
            print(f'Duration: {time.perf_counter() - start_time}')

        # print memory
        if opts.mem:
            print_mem()
