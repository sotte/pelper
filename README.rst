################################
pelper - python helper functions
################################

|docs| |coverage_status| |build_status| |pypi| |github|

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
    >>> pipe("some datat, some data", set, (sorted, {"reverse": True}))
    ['t', 's', 'o', 'm', 'e', 'd', 'a', ',', ' ']


Pelper offers `p`-functions, i.e., functions where the first argument is data.
There is ``pmap`` (like map, but works with ``pipel``):

.. code:: python

    >>> from pelper import pipe, pmap
    >>> pipe(
    ...     range(5),
    ...     (pmap, lambda x: x*x),
    ...     list)
    [0, 1, 4, 9, 16]


...and also pfilter:

.. code:: python

    >>> from pelper import pipe, pfilter
    >>> pipe(
    ...     range(5),
    ...     (pfilter, lambda x: x > 2),
    ...     list)
    [3, 4]


Take `n` elements from iterables (useful if you can't use the square bracket
notation, e.g., if you're using pipe)

.. code:: python

    >>> from pelper import take
    >>> take("hello world", 5)
    ['h', 'e', 'l', 'l', 'o']


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
    ...  def f(n): pass


Measure the duration of a context:

.. code:: python

    >>> from pelper import print_duration
    >>> with print_duration():
    ...     range(4)


Ignore exceptions:

.. code:: python

    >>> from pelper import ignored
    >>> with ignored(OSError):
    ...     raise OSError()  # this is ignored


Cache already computed results of functions:

.. code:: python

    >>> from pelper import cache
    >>> @cache
    >>> def fib(n):
    ...     return 1 if n < 2 else fib(n-1) + fib(n-2)
    >>> f(500)  # this would run for quite a wile without the cache decorator


Easier printing and formating:

.. code:: python

    >>> from pelper import printf
    >>> printf("Hello {name}, I'm {something}", name="Alan", something="world")
    Hello Alan, I'm world


Installation
============

``pelper`` is only one file and has no dependencies.
You can simply drop ``pelper.py`` into your project and use it.

Or install it from pypi by running::

    pip install pelper

Or install it from source by running::

    pip install .


Development
===========

Use virtualenv_ for working on ``pelper``.
Install the dev requrirements via::

    pip install -e requirements-dev.txt

Tests
-----

``pelper`` uses doctest, ``py.test``, and ``tox`` for testing.
It also has |coverage_status| coverage.

You can run the tests for all supported versions of python and build and test
the docs::

    tox

Run only the tests for the specified version of python::

    tox -e py27,py34,py35

Alternatively just run tests for the current version of python::

    py.test


Docs
----

Build the docs via::

    cd docs
    sphinx html


.. ============================================================================
.. Links

.. |build_status| image:: https://api.shippable.com/projects/572309a32a8192902e1e65c7/badge?branch=master
    :alt: Build status
    :target: https://app.shippable.com/projects/572309a32a8192902e1e65c7

.. |coverage_status| image:: https://api.shippable.com/projects/572309a32a8192902e1e65c7/coverageBadge?branch=master
    :alt: Coverage status
    :target: https://app.shippable.com/projects/572309a32a8192902e1e65c7

.. |docs| image:: https://readthedocs.org/projects/pelper/badge/?version=latest
    :alt: read the docs
    :target: http://pelper.readthedocs.org/en/latest/

.. |pypi| image:: https://badge.fury.io/py/pelper.svg
    :alt: PyPI page
    :target: https://badge.fury.io/py/pelper

.. |github| image:: https://badge.fury.io/gh/sotte%2Fpelper.svg
    :alt: Github page
    :target: https://badge.fury.io/gh/sotte%2Fpelper

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
