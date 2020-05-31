# -*- coding: utf-8 -*-
import re
import pytest

from clikit.api.io.flags import DEBUG
from clikit.api.io.flags import VERBOSE
from clikit.io.buffered_io import BufferedIO
from clikit.ui.components.exception_trace import ExceptionTrace
from clikit.utils._compat import PY36
from clikit.utils._compat import PY38


def fail():
    raise Exception("Failed")


@pytest.mark.skipif(PY36, reason="Legacy error messages are Python <3.6 only")
def test_render_legacy_error_message():
    io = BufferedIO()

    try:
        raise Exception("Failed")
    except Exception as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = """\

Exception

Failed
"""
    assert expected == io.fetch_output()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_better_error_message():
    io = BufferedIO()

    try:
        raise Exception("Failed")
    except Exception as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = """\

  Exception

  Failed

  at {}:44 in test_render_better_error_message
       40│ def test_render_better_error_message():
       41│     io = BufferedIO()
       42│ 
       43│     try:
    →  44│         raise Exception("Failed")
       45│     except Exception as e:
       46│         trace = ExceptionTrace(e)
       47│ 
       48│     trace.render(io)
""".format(
        trace._get_relative_file_path(__file__)
    )
    assert expected == io.fetch_output()


@pytest.mark.skipif(PY36, reason="Legacy error messages are Python <3.6 only")
def test_render_verbose_legacy():
    io = BufferedIO()
    io.set_verbosity(VERBOSE)

    try:
        raise Exception("Failed")
    except Exception as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    msg = "'Failed'"
    if PY38:
        msg = '"Failed"'

    expected = """\

Exception

Failed

Traceback (most recent call last):
  File "{}", line 78, in test_render_verbose_legacy
    raise Exception({})

""".format(
        __file__, msg
    )
    assert expected == io.fetch_output()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_debug_better_error_message():
    io = BufferedIO()
    io.set_verbosity(DEBUG)

    try:
        fail()
    except Exception as e:  # Exception
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = r"""^
  Stack trace:

  1  {}:112 in test_render_debug_better_error_message
      110\│ 
      111\│     try:
    → 112\│         fail\(\)
      113\│     except Exception as e:  # Exception
      114\│         trace = ExceptionTrace\(e\)

  Exception

  Failed

  at {}:14 in fail
       10\│ from clikit.utils._compat import PY38
       11\│ 
       12\│ 
       13\│ def fail\(\):
    →  14\│     raise Exception\("Failed"\)
       15\│ 
       16\│ 
       17\│ @pytest.mark.skipif\(PY36, reason="Legacy error messages are Python <3.6 only"\)
       18\│ def test_render_legacy_error_message\(\):
""".format(
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
    )

    assert re.match(expected, io.fetch_output()) is not None


def recursion_error():
    recursion_error()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_debug_better_error_message_recursion_error():
    io = BufferedIO()
    io.set_verbosity(DEBUG)

    try:
        recursion_error()
    except RecursionError as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = r"""^
  Stack trace:

  \d+  {}:162 in test_render_debug_better_error_message_recursion_error
        160\│ 
        161\│     try:
      → 162\│         recursion_error\(\)
        163\│     except RecursionError as e:
        164\│         trace = ExceptionTrace\(e\)

  ...  Previous frame repeated \d+ times

  \s*\d+  {}:151 in recursion_error
        149\│ 
        150\│ def recursion_error\(\):
      → 151\│     recursion_error\(\)
        152\│ 
        153\│ 

  RecursionError

  maximum recursion depth exceeded

  at {}:151 in recursion_error
      147\│     assert re.match\(expected, io.fetch_output\(\)\) is not None
      148\│ 
      149\│ 
      150\│ def recursion_error\(\):
    → 151\│     recursion_error\(\)
      152\│ 
      153\│ 
      154\│ @pytest.mark.skipif\(
      155\│     not PY36, reason="Better error messages are only available for Python \^3\.6"
""".format(
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
    )

    assert re.match(expected, io.fetch_output()) is not None


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_verbose_better_error_message():
    io = BufferedIO()
    io.set_verbosity(VERBOSE)

    try:
        fail()
    except Exception as e:  # Exception
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = r"""^
  Stack trace:

  1  {}:218 in test_render_verbose_better_error_message
     fail\(\)

  Exception

  Failed

  at {}:14 in fail
       10\│ from clikit.utils._compat import PY38
       11\│ 
       12\│ 
       13\│ def fail\(\):
    →  14\│     raise Exception\("Failed"\)
       15\│ 
       16\│ 
       17\│ @pytest.mark.skipif\(PY36, reason="Legacy error messages are Python <3.6 only"\)
       18\│ def test_render_legacy_error_message\(\):
""".format(
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
    )

    assert re.match(expected, io.fetch_output()) is not None


def first():
    def second():
        first()

    second()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_debug_better_error_message_recursion_error_with_multiple_duplicated_frames():
    io = BufferedIO()
    io.set_verbosity(VERBOSE)

    with pytest.raises(RecursionError) as e:
        first()

    trace = ExceptionTrace(e.value)

    trace.render(io)

    expected = r"...  Previous 2 frames repeated \d+ times".format(
        filename=re.escape(trace._get_relative_file_path(__file__)),
    )

    assert re.search(expected, io.fetch_output()) is not None


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_can_ignore_given_files():
    import os
    from .helpers import outer

    io = BufferedIO()
    io.set_verbosity(VERBOSE)

    def call():
        def run():
            outer()

        run()

    with pytest.raises(Exception) as e:
        call()

    trace = ExceptionTrace(e.value)
    helpers_file = os.path.join(os.path.dirname(__file__), "helpers.py")
    trace.ignore_files_in("^{}$".format(re.escape(helpers_file)))

    trace.render(io)

    expected = """
  Stack trace:

  2  {}:297 in test_render_can_ignore_given_files
     call()

  1  {}:294 in call
     run()

  Exception

  Foo

  at {}:3 in inner
      1│ def outer():
      2│     def inner():
    → 3│         raise Exception("Foo")
      4│ 
      5│     inner()
      6│ 
""".format(
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(helpers_file),
    )

    assert expected == io.fetch_output()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_shows_ignored_files_if_in_debug_mode():
    import os
    from .helpers import outer

    io = BufferedIO()
    io.set_verbosity(DEBUG)

    def call():
        def run():
            outer()

        run()

    with pytest.raises(Exception) as e:
        call()

    trace = ExceptionTrace(e.value)
    helpers_file = os.path.join(os.path.dirname(__file__), "helpers.py")
    trace.ignore_files_in("^{}$".format(re.escape(helpers_file)))

    trace.render(io)

    expected = """
  Stack trace:

  4  {}:351 in test_render_shows_ignored_files_if_in_debug_mode
      349│ 
      350│     with pytest.raises(Exception) as e:
    → 351│         call()
      352│ 
      353│     trace = ExceptionTrace(e.value)

  3  {}:348 in call
      346│             outer()
      347│ 
    → 348│         run()
      349│ 
      350│     with pytest.raises(Exception) as e:

  2  {}:346 in run
      344│     def call():
      345│         def run():
    → 346│             outer()
      347│ 
      348│         run()

  1  {}:5 in outer
      3│         raise Exception("Foo")
      4│ 
    → 5│     inner()
      6│ 

  Exception

  Foo

  at {}:3 in inner
      1│ def outer():
      2│     def inner():
    → 3│         raise Exception("Foo")
      4│ 
      5│     inner()
      6│ 
""".format(
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(helpers_file),
        trace._get_relative_file_path(helpers_file),
    )

    assert expected == io.fetch_output()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_supports_solutions():
    from crashtest.contracts.provides_solution import ProvidesSolution
    from crashtest.contracts.base_solution import BaseSolution
    from crashtest.solution_providers.solution_provider_repository import (
        SolutionProviderRepository,
    )

    class CustomError(ProvidesSolution, Exception):
        @property
        def solution(self):
            solution = BaseSolution("Solution Title.", "Solution Description")
            solution.documentation_links.append("https://example.com")
            solution.documentation_links.append("https://example2.com")

            return solution

    io = BufferedIO()

    def call():
        raise CustomError("Error with solution")

    with pytest.raises(CustomError) as e:
        call()

    trace = ExceptionTrace(
        e.value, solution_provider_repository=SolutionProviderRepository()
    )

    trace.render(io)

    expected = """
  CustomError

  Error with solution

  at {}:433 in call
      429│ 
      430│     io = BufferedIO()
      431│ 
      432│     def call():
    → 433│         raise CustomError("Error with solution")
      434│ 
      435│     with pytest.raises(CustomError) as e:
      436│         call()
      437│ 

  • Solution Title: Solution Description
    https://example.com,
    https://example2.com
""".format(
        trace._get_relative_file_path(__file__),
    )

    assert expected == io.fetch_output()
