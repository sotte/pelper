################################
pelper - python helper functions
################################

|build_status| |coveralls| |docs|

``pelper`` -- python helper functions to ease measuring, ignoring, caching,
piping, functional helpers, and more for python 2.7, 3.4, and 3.5.

``pelper`` contains useful helper functions, decorators, context managers
- all the things that make your python life a tiny bit easier.
``pelper`` has no dependencies,
has a coverage of 100%,
and is well documented.


Examples
========

Pipe data through unix-like/elixir-like pipes:

.. code:: python

    >>> from pelper import pipe
    >>> pipe("some datat, some data",
    >>>      set,
    >>>      (sorted, {"reverse": True}))
    ['t', 's', 'o', 'm', 'e', 'd', 'a', ',', ' ']



Take `n` elements from iterables (useful if you can't use the square bracket
notation, e.g., if you're using pipe)

.. code:: python

    >>> from pelper import take
    >>> take("hello world", 5)
    'hello'


Take the `n`-th elements from iterables (useful if you can't use the square
bracket notation, e.g., if you're using pipe)

.. code:: python

    >>> from pelper import nth
    >>> nth(range(5), 2)
    2


Flatten arbitrarily nested lists:

.. code:: python

    >>> from pelper import flatten
    >>> flatten([1, [2, 2, [3, 3]]])
    [1, 2, 2, 3, 3]


Measure the duration of a function:

.. code:: python

    >>> from pelper import print_duration
    >>> @print_duration()
    >>> def f(n):
    >>>     pass


Measure the duration of a context:

.. code:: python

    >>> from pelper import print_duration
    >>> with print_duration():
    >>>     range(4)


Ignore exceptions:

.. code:: python

    >>> from pelper import ignored
    >>> with ignored(OSError):
    >>>     raise OSError()  # this is ignored


Cache already computed results of functions:

.. code:: python

    >>> from pelper import cache
    >>> @cache
    >>> def fib(n):
    >>>     return 1 if n < 2 else fib(n-1) + fib(n-2)
    >>> f(500)  # this would run for quite a wile without the cache decorator


Installation
============

``pelper`` is only one file and has no dependencies.
You can simply drop ``pelper.py`` into your project and use it.

Or install it from pypi by running::

    pip install pelper

Or install it from source by running::

    pip install .


Tests
=====

``pelper`` uses doctest extensively and has |coveralls|.
You can run the tests with::

    python pelper/pelper.py

or::

    python -m doctest pelper/pelper.py

or::

    python3 pelper/pelper.py

or::

    python3 -m doctest pelper/pelper.py


.. ============================================================================
.. Links

.. |build_status| image:: https://travis-ci.org/sotte/pelper.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/sotte/pelper

.. |coveralls| image:: https://coveralls.io/repos/sotte/pelper/badge.svg?branch=master
    :alt: coverage
    :target: https://coveralls.io/r/sotte/pelper?branch=master

.. |docs| image:: https://readthedocs.org/projects/pelper/badge/?version=latest
    :alt: read the docs
    :target: http://pelper.readthedocs.org/en/latest/
