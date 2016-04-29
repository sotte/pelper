from __future__ import print_function
from contextlib import contextmanager
from functools import wraps
import time


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
        ...     fib(24)
        75025
        Duration 0...s

        >>> # the cached version is much faster
        >>> @cache
        ... def fib(n):
        ...     return 1 if n < 2 else fib(n-1) + fib(n-2)
        >>> with print_duration():  #doctest: +ELLIPSIS
        ...     fib(24)
        75025
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
def printf(string, *args, **kwargs):
    """Combine print with format.


    Examples:
        Use printf like print without any arguments:
        >>> from pelper import printf
        >>> printf('text')
        text

        With args:
        >>> printf('text {} {}', 'alan', 'bob')
        text alan bob

        >>> printf('text {1} {0}', 'alan', 'bob')
        text bob alan

        With named arguments:
        >>> printf('text {first} {second}', first='alan', second='bob')
        text alan bob

        Unpacking a dict:
        >>> printf('text {first} {second}',
        ...    **{'first': 'alan', 'second': 'bob'})
        text alan bob

    """
    print(string.format(*args, **kwargs))
