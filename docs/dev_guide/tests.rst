.. _testing:

******************
Testing Guidelines
******************

This section describes the testing framework and format standards for tests in SunPy.
Here we have heavily adapted the `Astropy version <http://docs.astropy.org/en/latest/development/testguide.html>`_.

Testing Framework
=================

The testing framework used by SunPy is the `pytest`_ framework, accessed through the ``python setup.py test`` command.

.. _pytest: https://pytest.org/en/latest/

.. note::

    The ``pytest`` project was formerly called ``py.test``, and you may
    see the two spellings used interchangeably in the documentation.

Testing Dependencies
====================

As of SunPy 1.0, the dependencies used by the SunPy test runner are provided by a separate package called `pytest-sunpy`_.
This package provides the ``pytest`` dependency itself, in addition to several ``pytest`` plugins that are used by SunPy, and will also be of general use to other packages.

Since the testing dependencies are not actually required to install or use SunPy, they are not included in ``install_requires`` in ``setup.cfg``.

Developers who want to run the test suite will need to install the testing package using pip::

    $ pip install pytest-sunpy

You can also do::

    $ pip intall -e .[tests]

.. _pytest-astropy: https://github.com/nabobalis/pytest-sunpy

Running Tests
=============

There are currently three different ways to invoke the SunPy tests.
Each method invokes pytest to run the tests but offers different options when
calling.

python setup.py test
--------------------

SunPy provide a ``test`` setup command, invoked by running ``python setup.py test`` while in the
package root directory.
Run ``python setup.py test --help`` to see the options to the test command.

Since ``python setup.py test`` wraps the widely-used pytest framework, you may from time to time want to pass options to the ``pytest`` command itself.
For example, the ``-x`` option to stop after the first failure can be passed through with the ``--args`` argument::

    $ python setup.py test --args "-x"

``pytest`` will look for files that `look like tests <https://pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery>`_ in the current directory and all recursive directories then run all the code that `looks like tests <https://pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery>`_ within those files.

Note also that this test runner actually installs sunpy into a temporary directory and uses that for running the tests.
This means that tests of things like entry points or data file paths should act just like they would once sunpy is installed.
The other two approaches described below do *not* do this, and hence may give different results when run.
Hence if you're running the tests because you've modified code that might be impacted by this, the ``setup.py test`` approach is the recommended method.

``pytest``
----------

The test suite can be run directly from the native ``pytest`` command.
In this case, it is important for developers to be aware that they must manually rebuild any extensions by running ``setup.py build_ext`` before testing.

Test-running options
====================

Running parts of the test suite
-------------------------------

It is possible to run only the tests for a particular subpackage or set of subpackages.
For example, to run only the ``map`` tests from the commandline::

    python setup.py test -P map

Or, to run only the ``map`` and ``timeseries`` tests::

    python setup.py test -P map,timeseries

You can also specify a single file to test from the commandline::

    python setup.py test -t sunpy/map/tests/test_mapbase.py

When the ``-t`` option is given a relative path, it is relative to  installed root of sunpy.
When ``-t`` is given a relative path to a documentation ``.rst`` file to test, it is relative to the root of the documentation, i.e. the ``docs`` directory in the source tree.
For example::

    python setup.py test -t guide/index.rst

Test coverage reports
---------------------

SunPy can use `coverage.py <http://coverage.readthedocs.io/en/latest/>`_  generate test coverage reports.
To generate a test coverage report, use::

    python setup.py test --coverage

Settings for this are stored in ``setup.cfg``.

Running tests in parallel
-------------------------

It is possible to speed up SunPy's tests using the `pytest-xdist <https://pypi.python.org/pypi/pytest-xdist>`_ plugin.
This plugin can be installed using `pip`_::

    pip install pytest-xdist

Once installed, tests can be run in parallel using the ``'--parallel'`` commandline option.
For example, to use 4 processes::

    python setup.py test --parallel=4

Pass ``--parallel=auto`` to create the same number of processes as cores
on your machine.

Writing tests
=============

``pytest`` has the following test discovery rules:

 * ``test_*.py`` or ``*_test.py`` files
 * ``Test`` prefixed classes (without an ``__init__`` method)
 * ``test_`` prefixed functions and methods

Consult the `test discovery rules <https://pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery>`_ for detailed information on how to name files and tests so that they are automatically discovered by ``pytest``.

A rule of thumb for unit testing is to have at least one unit test per public function.

Simple example
--------------

The following example shows a simple function and a test to test this
function::

    def func(x):
        """Add one to the argument."""
        return x + 1

    def test_answer():
        """Check the return value of func() for an example argument."""
        assert func(3) == 5

If we place this in a ``test.py`` file and then run::

    pytest test.py

The result is::

    ============================= test session starts ==============================
    python: platform darwin -- Python 3.6.0 -- pytest-3.2.0
    test object 1: /Users/username/tmp/test.py

    test.py F

    =================================== FAILURES ===================================
    _________________________________ test_answer __________________________________

        def test_answer():
    >       assert func(3) == 5
    E       assert 4 == 5
    E        +  where 4 = func(3)

    test.py:5: AssertionError
    =========================== 1 failed in 0.07 seconds ===========================

Sometimes the output from the test suite will have ``xfail`` meaning a test has passed although it has been marked as ``@pytest.mark.xfail``), or ``skipped`` meaing a test that has been skipped due to not meeting some condition (online and figure tests are the most common).

You need to use the option ``-rs`` for skipped tests and ``-rx`` for xfailed tests, respectively.
Or use ``-rxs`` for detailed information on both skipped and xfailed tests.

Where to put tests
------------------

Each package should include a suite of unit tests, covering as many of the public methods/functions as possible.
These tests should be included inside each package, e.g::

    sunpy/map/tests/

``tests`` directories should contain an ``__init__.py`` file so that the tests can be imported.

Online Tests
------------

There are some tests for functions and methods in SunPy that require a working connection to the internet.
``pytest`` is configured in a way that it iterates over all tests that have been marked as ``pytest.mark.remote_data`` and checks if there is an established connection to the internet.
If there is none, the test is skipped, otherwise it is run.

Marking tests is pretty straightforward, use the decorator ``@pytest.mark.remote_data`` to mark a test function as needing an internet connection::

    @pytest.mark.remote_data
    def func(x):
        """Add one to the argument."""
        return x + 1

Tests that create files
-----------------------

Tests may often be run from directories where users do not have write permissions so tests which create files should always do so in temporary directories.
This can be done with the `pytest tmpdir function argument <https://pytest.org/en/latest/tmpdir.html>`_ or with Python's built-in `tempfile module
<https://docs.python.org/3/library/tempfile.html#module-tempfile>`_.

Figure unit tests
-----------------

You can write SunPy unit tests that test the generation of matplotlib figures by adding the decorator `sunpy.tests.helpers.figure_test`.
Here is a simple example: ::

    import matplotlib.pyplot as plt
    from sunpy.tests.helpers import figure_test

    @figure_test
    def test_simple_plot():
        plt.plot([0,1])

The current figure at the end of the unit test, or an explicitly returned figure, has its hash compared against an established hash library (more on this below).
If the hashes do not match, the figure has changed, and thus the test is considered to have failed.

You will need to update the library of figure hashes after you create a new figure test or after a figure has intentionally changed due to code improvement.
The file is located at ``sunpy/tests/figure_tests_env_py36.json``.

Writing Doctests
================

Code examples in the documentation will also be run as tests and this helps to validate that the documentation is accurate and up to date.
SunPy uses the same system as Astropy, so for information on writing doctests see the astropy `documentation <http://docs.astropy.org/en/latest/development/testguide.html#writing-doctests>`_.

Bugs discovered
===============

In addition to writing unit tests new functionality, it is also a good practice to write a unit test each time a bug is found, and submit the unit test along with the fix for the problem.
This way we can ensure that the bug does not re-emerge at a later time.
