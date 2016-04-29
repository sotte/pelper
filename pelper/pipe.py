from __future__ import print_function
from itertools import islice


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
def returning(data, fn, *args, **kwargs):
    """
    Call function `fn` with `data` and return the unchanged data.

    The return value of `fn` is ignored.
    `returning` is useful if `fn` does not return anything but has sideeffects,
    e.g., printing `data` in a `pipe` call.

    Args:
        data (anything): argument for fn
        fn (callable): a function that is going to be called
        *args: optional arguments
        **kwargs: optional key word arguments

    Returns:
        `data`


    Examples:
        >>> pipe(
        ...     "Some text",
        ...     (returning, print),
        ...     lambda data: data.upper(),
        ... )
        Some text
        'SOME TEXT'
    """
    fn(data, *args, **kwargs)
    return data


###############################################################################
def pmap(iterable, fn):
    """
    Pipeable version of `map`, i.e., the arguments are swapped.

    Because `map` expects a function as first argument it is not really suited
    for `pipe`. `pmap` swaps the arguments.

    Args:
        iterable: some iterable
        fn (callable):

    Returns:
        result of map(fn, iterable)

    Examples:
        >>> pipe(
        ...     range(5),
        ...     (pmap, lambda x: x*x),
        ...     list)
        [0, 1, 4, 9, 16]

    """
    return map(fn, iterable)


def pfilter(iterable, fn):
    """
    Pipeable version of `filter`, i.e., the arguments are swapped.

    Because `filter` expects a function as first argument it is not really
    suited for `pipe`. `pfilter` swaps the arguments.

    Args:
        iterable: some iterable
        fn (callable):

    Returns:
        result of filter(fn, iterable)

    Examples:
        >>> pipe(
        ...     range(5),
        ...     (pfilter, lambda x: x > 2),
        ...     list)
        [3, 4]

    """
    return filter(fn, iterable)


###############################################################################
def print_return(data):
    """
    Print data and return data.

    Args:
        data (anything): data to print and return

    Returns:
        `data`

    Examples:
        >>> pipe(
        ...     "Some text",
        ...     print_return,
        ...     lambda data: data.upper(),
        ... )
        Some text
        'SOME TEXT'
    """
    return returning(data, print)
