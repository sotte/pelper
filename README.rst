################################
pelper - python helper functions
################################

``pelper`` -- python helper functions to ease measuring, ignoring, caching, ...

``pelper`` contains useful helper functions, decorators, context managers - all
that stuff that make the python life a bit easier.

Examples
========

::

    >>> # measure duration of a function
    >>> from pelper import print_duration
    >>> @print_duration(out=mylogger)
    ... def f(n): pass

    >>> # measure duration of a context
    >>> from pelper import print_duration
    >>> with print_duration(out=mylogger):
    ...     range(4)

    >>> # ignore exceptions
    >>> from pelper import ignored
    >>> with ignored(OSError):
    ...     raise OSError()

    >>> # cache already computed results of functions
    >>> from pelper import cache
    >>> @cache
    ... def fib(n):
    ...     return 1 if n < 2 else fib(n-1) + fib(n-2)
    >>> f(5)
    8


Installation
============

``pelper`` is only one file and has no dependencies.
You can simply drop ``pelper.py`` into your project and use it.

Run the tests::

    python pelper.py


TODO
====

  * add CONTRIBUTING.rst

  * improve doc: use sphinx? is it worth it?

  * Install
    * pip
    * conda

  * add badges
    * travis
    * read the docs
    * pypi
