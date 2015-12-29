#!/usr/bin/env python
# encoding: utf-8
###############################################################################
from __future__ import print_function
from contextlib import contextmanager
from functools import wraps
from itertools import islice
import time

__version__ = "0.0.3"


###############################################################################
def pipe(data, *functions):
    """pipe data trough a pipeline of functions.

    Think of unix pipes or elixir's pipes.
    ``pipe`` assumes that data is the first argument of a function.

    ``pipe`` tries to be smart and automatically cerates partial functions if
    you pass a tuple instead of a callable:

    - ``pipe(data, (pow, 2, 5))`` --> ``pow(data, 2, 5)``.

    - ``pipe(data, (sorted, {"reverse": True}))`` -->
      ``sorted(data, reverse=True)``

    Args:
        data (whatever): the data that is passed into the first function.
        functions (callables): functions that create the pipeline.

    Returns:
        The result of your pipeline.

    Examples:
        ``pipe`` allows you to turn something which is hard to read:

        >>> from math import ceil, sqrt
        >>> sqrt(pow(int(ceil(float("2.1"))), 2))
        3.0

        into something that is easy to read:

        >>> pipe("2.1", float, ceil, int, lambda x: x*x, sqrt)
        3.0

        Genrate your own partial functions with lambda

        >>> pipe("2.1", float, ceil, int, lambda x: pow(x, 2), sqrt)
        3.0

        But there is a shortcut: tuples are interpreted as as
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

        It can be convenient to use the following notation if the function
        names are longer:

        >>> text = "atababsatsatsastatbadstssdhhhnbb"
        >>> pipe(text,
        ...      set,
        ...      sorted)
        ['a', 'b', 'd', 'h', 'n', 's', 't']

        It's also possible to use named arguments by using a dict:

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
def take(iterable, n):
    """Return first n items of the iterable as a list

    Args:
        iterable (iterable): the iterable to take from.
        n (int): the number of elements to take.

    Returns:
        list: the first n elements of iterable.

    Examples:
        >>> take(range(5), 2)
        [0, 1]

        >>> take(range(5), 0)
        []
    """
    return list(islice(iterable, n))


###############################################################################
def nth(iterable, n, default=None):
    """Returns the n-th item or a default value

    Return None if there is no nth element (or default if specified).

    Args:
        iterable (iterable): the iterable to take from.
        n (int): the n-th elements to take.
        default (whatever): return default if nothing found

    Returns:
        The n-th element of iterable.

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
        ...     list(range(5))
        [0, 1, 2, 3, 4]
        Duration 0...s

        Specify a message:

        >>> with print_duration(msg="range test"):  #doctest: +ELLIPSIS
        ...    list(range(5))
        [0, 1, 2, 3, 4]
        range test 0...s

        Use your logger:

        >>> import logging
        >>> log = logging.getLogger()
        >>> with print_duration(out=log.warning):  #doctest: +ELLIPSIS
        ...    list(range(5))
        [0, 1, 2, 3, 4]

        With message and logger:

        >>> with print_duration("range test", out=log.warning):
        ...     list(range(5))
        [0, 1, 2, 3, 4]

        Use print_duration as decorator:

        >>> @print_duration("f took")
        ... def f():
        ...     list(range(5))
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

    Args:
        f (function): the function to cache.

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
def flatten(nested_list):
    """Flatten arbitrarily nested lists.

    Args:
        nested_list (iterable): arbitrarily nested list.

    Returns:
        list: a flattened list.

    Examples:

        >>> flatten(range(5))
        [0, 1, 2, 3, 4]

        >>> flatten([1, [2, 2]])
        [1, 2, 2]

        >>> flatten([1, [2, 2], [3, 3, 3, [4, 4, 4, 4,], 3], 1])
        [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 3, 1]

        Note that strings are not flattened:

        >>> flatten(["one", ["two", "three", ["four"]]])
        ['one', 'two', 'three', 'four']

    """
    if not hasattr(nested_list, "__iter__") or isinstance(nested_list, str):
        return [nested_list]

    result = []
    for e in nested_list:
        result.extend(flatten(e))
    return result


###############################################################################
if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
