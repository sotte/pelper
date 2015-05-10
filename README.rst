################################
pelper - python helper functions
################################

|build_status| |coveralls| |docs|

``pelper`` -- python helper functions to ease measuring, ignoring, caching, ...

``pelper`` contains useful helper functions, decorators, context managers
- all the stuff that make the python life a tiny bit easier.
It has no dependencies,
has a coverage of 100%,
and is well documented.

Examples
========

Measure the duration of a function:

.. code:: python

    from pelper import print_duration
    @print_duration()
    def f(n):
        pass


Measure duration of a context:

.. code:: python

    from pelper import print_duration
    with print_duration():
        range(4)

Ignore exceptions:

.. code:: python

    from pelper import ignored
    with ignored(OSError):
        raise OSError()  # this is ignored

Cache already computed results of functions:

.. code:: python

    from pelper import cache
    @cache
    def fib(n):
        return 1 if n < 2 else fib(n-1) + fib(n-2)

    f(500)  # this would run for quite a wile without the cache decorator

Pipe data through unix-like pipes

.. code:: python

    from pelper import pipe
    pipe("some datat, some data",
         set,
         (sorted, {"reverse": True}))


Take `n` elements from iterables (useful if you can't use the square bracket
notation, e.g., if you're using pipe)

.. code:: python

    from pelper import take
    take(2, range(5))

Take the `n`-th elements from iterables (useful if you can't use the square bracket
notation, e.g., if you're using pipe)

.. code:: python

    from pelper import nth
    nth(2, range(5))


Installation
============

``pelper`` is only one file and has no dependencies.
You can simply drop ``pelper.py`` into your project and use it.

Run the tests::

    python pelper.py


TODO
====

- install via pip and conda


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
