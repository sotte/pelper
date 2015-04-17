#!/usr/bin/env python
# encoding: utf-8
# There are lots of nice decorators:
# https://wiki.python.org/moin/PythonDecoratorLibrary

###############################################################################
from __future__ import print_function
from contextlib import contextmanager
from functools import wraps
import time


###############################################################################
def pipe(data, *functions):
    """pipe data trough a pipeline of functions.

    Think of unix pipes for python or elixir's pipes

    Examples:

    Of course you can use lambda functions
    >>> from math import ceil, sqrt
    >>> pipe("2.1", float, ceil, int, lambda x: x*x, sqrt)
    3.0

    Genrate your own partial functions with lambda
    >>> pipe("2.1", float, ceil, int, lambda x: pow(x, 2), sqrt)
    3.0

    >>> pipe("2.1", float, ceil, int, lambda x: pow(x, 2), sqrt)
    3.0

    There is a shortcut: tuples are interpreted as as
    ``(functions, arguments, ...)``. The data passed from the previous function
    is the first argument of the punction, followed by the arguments from the
    tuple.
    >>> pipe("2.1", float, ceil, int, (pow, 2), sqrt)
    3.0

    To make this clearer ``pipe(3, (pow, 2))`` is equivalent to ``pow(3, 2)``.
    Of course you can pass multiple arguments with the tuple
    >>> pipe(3, (pow, 2, 8))  # pow(2, 3, 8) -> pow(2, 3) % 8
    1

    It can be convenient to use this notation if the function names are longer
    >>> text = "atababsatsatsastatbadstssdhhhnbb"
    >>> pipe(text,
    ...      set,
    ...      sorted)
    ['a', 'b', 'd', 'h', 'n', 's', 't']

    It's also possible to use named arguments:
    >>> pipe(text, set, (sorted, {"reverse": True}))
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
class print_duration(object):
    """`print_duration` is a "ContextDecorator" to measure the execution time
    of the given function or context.

    A "ContextDecorator" is a combination of decorator and context manager.

    Warning:

    This is not the best implementation of a context decorator.
    Exception might get swallowed.

    Args:
        msg (string): the message that is printed before the measured time
            Default is None

    Examples:

    >>> # use print_duration as context manager
    >>> with print_duration():  #doctest: +ELLIPSIS
    ...     # do something
    ...     range(5)
    [0, 1, 2, 3, 4]
    Duration 0...s

    >>> # specify a message
    >>> with print_duration(msg="range test"):  #doctest: +ELLIPSIS
    ...    range(5)
    [0, 1, 2, 3, 4]
    range test 0...s

    >>> # use your logger
    >>> import logging
    >>> log = logging.getLogger()
    >>> with print_duration(out=log.warning):
    ...    range(5)
    [0, 1, 2, 3, 4]

    >>> # with message and logger
    >>> with print_duration("range test", out=log.warning):
    ...     range(5)
    [0, 1, 2, 3, 4]

    >>> # use print_duration as decorator
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
    """Cache the results of f.

    Note: Only use this with pure functions!

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
    # print(doctest.testmod(verbose=True))
    print(doctest.testmod())
