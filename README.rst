################################
pelper - python helper functions
################################

.. image:: https://travis-ci.org/sotte/pelper.svg?branch=master
    :target: https://travis-ci.org/sotte/pelper

.. image:: https://coveralls.io/repos/sotte/pelper/badge.svg?branch=master
    :target: https://coveralls.io/r/sotte/pelper?branch=master

``pelper`` -- python helper functions to ease measuring, ignoring, caching, ...

``pelper`` contains useful helper functions, decorators, context managers - all
that stuff that make the python life a bit easier.

Examples
========

Measure the duration of a function::

    from pelper import print_duration
    @print_duration()
    def f(n): pass


Measure duration of a context::

    from pelper import print_duration
    with print_duration():
        range(4)

Ignore exceptions::

    from pelper import ignored
    with ignored(OSError):
        raise OSError()  # this is ignored

Cache already computed results of functions::

    from pelper import cache
    @cache
    def fib(n):
        return 1 if n < 2 else fib(n-1) + fib(n-2)

    f(500)  # this would run for quite a wile without the cache decorator

Pipe data through unix-like pipes::

    from pelper import pipe
    pipe("some datat, some data",
         set,
         (sorted, {"reverse": True}))


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
