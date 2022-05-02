import sys
from typing import NoReturn
import datetime
from contextlib import contextmanager

DISABLE_DEBUG = True
DISABLE_INFO = False
DISABLE_PERFLOG = True

# fmt: off
if DISABLE_DEBUG:
    def debug(msg: str) -> None:
        pass
else:
    def debug(msg: str) -> None:
        print(f"(((DEBUG)))  {msg}", file=sys.stderr, flush=True)

if DISABLE_INFO:
    def info(msg: str) -> None:
        pass
else:
    def info(msg: str) -> None:
        print(msg, file=sys.stderr, flush=True)


def fatal(msg: str) -> NoReturn:
    print(msg, file=sys.stderr, flush=True)
    raise ValueError(msg)


if DISABLE_PERFLOG:
    def perflog(msg: str) -> None:
        pass
else:
    def perflog(msg: str) -> None:
        print(f"PERF {msg}", file=sys.stderr, flush=True)
# fmt: on


def measure_time(f, additional_text: str = "", logging_function=perflog):
    """ Decorator to measure elapsed time and log it """
    def wrapper(*args, **kwargs):
        identifier = f"{f.__name__} {additional_text}" if additional_text else f"{f.__name__}"
        with measure_time_ctx(identifier, logging_function):
            return f(*args, **kwargs)
    return wrapper


@contextmanager
def measure_time_ctx(identifier: str = "", logging_function=perflog):
    before = datetime.datetime.now()
    try:
        yield
    finally:
        after = datetime.datetime.now()
        elapsed_ms = int((after - before).total_seconds() * 1000)
        logging_function(f"{identifier} = {elapsed_ms} ms")
