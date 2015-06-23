#!/usr/bin/env python
# encoding: utf-8
# There are lots of nice decorators:
# https://wiki.python.org/moin/PythonDecoratorLibrary

###############################################################################
from __future__ import print_function
from contextlib import contextmanager
from functools import wraps
from itertools import islice
import time


###############################################################################
def pipe(data, *functions):
    """pipe data trough a pipeline of functions.

    Think of unix pipes or elixir's pipes.
    ``pipe`` tries to be smart and automatically cerates partial functions if
    you pass a tuple instead of a callable:

    - ``pipe(data, (pow, 2, 5))`` --> ``pow(data, 2, 5)``.

    - ``pipe(data, (sorted, {"reverse": True}))`` -->
      ``sorted(data, reverse=True)``

    Args:
        data (whatever): the data that is passed into the first function.
        functions (callables): functions that create the pipeline.

    Examples:
        Of course you can use lambda functions:

        >>> from math import ceil, sqrt
        >>> pipe("2.1", float, ceil, int, lambda x: x*x, sqrt)
        3.0

        Genrate your own partial functions with lambda

        >>> pipe("2.1", float, ceil, int, lambda x: pow(x, 2), sqrt)
        3.0

        There is a shortcut: tuples are interpreted as as
        ``(functions, arguments, ...)``.
        The data passed from the previous function is the first argument of the
        punction, followed by the arguments from the tuple.

        >>> pipe("2.1", float, ceil, int, (pow, 2), sqrt)
        3.0

        To make this clearer ``pipe(3, (pow, 2))`` is equivalent to
        ``pow(3, 2)``.
        Of course you can pass multiple arguments with the tuple:

        >>> pipe(3, (pow, 2, 8))  # pow(2, 3, 8) -> pow(2, 3) % 8
        1

        It can be convenient to use the following  notation if the function
        names are longer:

        >>> text = "atababsatsatsastatbadstssdhhhnbb"
        >>> pipe(text,
        ...      set,
        ...      sorted)
        ['a', 'b', 'd', 'h', 'n', 's', 't']

        It's also possible to use named arguments:

        >>> pipe(text,
        ...      set,
        ...      (sorted, {"reverse": True}))
        ['t', 's', 'n', 'h', 'd', 'b', 'a']

    """
    for f in functions:
        if isinstance(f, tuple):
            if isinstance(f[1], dict):
                data = f[0](data, **f[1])
            else:
                data = f[0](data, *f[1:])
        else:
            data = f(data)
    return data


###############################################################################
def take(n, iterable):
    """Return first n items of the iterable as a list

    Args:
        n (int): the number of elements to take.
        iterable (iterable): the iterable to take from.

    Examples:
        >>> take(2, range(5))
        [0, 1]
    """
    return list(islice(iterable, n))


###############################################################################
def nth(iterable, n, default=None):
    """Returns the nth item or a default value

    Return None if there is no nth element (or default if specified).

    Args:
        iterable (iterable): the iterable to take from.
        n (int): the nth elements to take.
        default (whatever): return default if nothing found

    Examples:
        >>> nth(range(5), 2)
        2

        >>> nth(range(5), 2, default="Hello")
        2

        >>> nth(range(5), 6)

        >>> nth(range(5), 6, default="Hello")
        'Hello'
    """
    return next(islice(iterable, n, None), default)


###############################################################################
class print_duration(object):
    """`print_duration` is a "ContextDecorator" to measure the execution time
    of the given function or context.

    A "ContextDecorator" is a combination of decorator and context manager.

    Args:
        msg (string, optional): the message that is printed before the measured
            time.
            Defaults to None.
        out (callable, optional): if set ``out`` is called with the measured
            duration.
            This can be a logger for example. ``print`` is used if out is
            ``None``. Defaults to ``None``.

    Warning:
        This is not the best implementation of a context decorator.
        Exception might get swallowed.

    Examples:
        Use print_duration as context manager:

        >>> with print_duration():  #doctest: +ELLIPSIS
        ...     # do something
        ...     range(5)
        [0, 1, 2, 3, 4]
        Duration 0...s

        Specify a message:

        >>> with print_duration(msg="range test"):  #doctest: +ELLIPSIS
        ...    range(5)
        [0, 1, 2, 3, 4]
        range test 0...s

        Use your logger:

        >>> import logging
        >>> log = logging.getLogger()
        >>> with print_duration(out=log.warning):
        ...    range(5)
        [0, 1, 2, 3, 4]

        With message and logger:

        >>> with print_duration("range test", out=log.warning):
        ...     range(5)
        [0, 1, 2, 3, 4]

        Use print_duration as decorator:

        >>> @print_duration("f took")
        ... def f():
        ...     range(5)
        >>> f()  #doctest: +ELLIPSIS
        f took 0...s

    """
    def __init__(self, msg=None, out=None):
        self.msg = msg
        self.out = print if out is None else out

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        duration = time.time() - self.start
        if self.msg:
            self.out("{} {:.6f}s".format(self.msg, duration))
        else:
            self.out("Duration {:.6f}s".format(duration))

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args):
            self.__enter__()
            result = func(*args)
            # TODO don't pass None
            self.__exit__(None, None, None)
            return result

        return wrapped_func


###############################################################################
def cache(f):
    """Decorator: cache the results of f for the same parameters.

    The decorated function is only called if the parameters differ from
    previous calls.
    Cache is really useful for recursive functions!

    Warning:
        Only use this with pure functions!

    Examples:
        >>> # try the normal fib
        >>> def fib(n):
        ...     return 1 if n < 2 else fib(n-1) + fib(n-2)
        >>> with print_duration():  #doctest: +ELLIPSIS
        ...     fib(25)
        121393
        Duration 0...s

        >>> # the cached version is much faster
        >>> @cache
        ... def fib(n):
        ...     return 1 if n < 2 else fib(n-1) + fib(n-2)
        >>> with print_duration():  #doctest: +ELLIPSIS
        ...     fib(25)
        121393
        Duration 0...s

    """
    saved = {}

    @wraps(f)
    def newfunc(*args):
        if args in saved:
            return saved[args]
        result = f(*args)
        saved[args] = result
        return result
    return newfunc


###############################################################################
@contextmanager
def ignored(*exception):
    """Context manager to ignore exceptions.

    Args:
        exception (Exception): the exception to ignore

    Example:
        >>> with ignored(OSError):
        ...     raise OSError  # this is ignored!

    """
    try:
        yield
    except exception:
        pass


###############################################################################
if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
