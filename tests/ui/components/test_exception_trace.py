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

  at {}:45 in test_render_better_error_message
       41│ def test_render_better_error_message():
       42│     io = BufferedIO()
       43│ 
       44│     try:
    →  45│         raise Exception("Failed")
       46│     except Exception as e:
       47│         trace = ExceptionTrace(e)
       48│ 
       49│     trace.render(io)
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
  File "{}", line 79, in test_render_verbose_legacy
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

  1  {}:113 in test_render_debug_better_error_message
      111\│ 
      112\│     try:
    → 113\│         fail\(\)
      114\│     except Exception as e:  # Exception
      115\│         trace = ExceptionTrace\(e\)

  Exception

  Failed

  at {}:15 in fail
       11\│ from clikit.utils._compat import PY38
       12\│ 
       13\│ 
       14\│ def fail\(\):
    →  15\│     raise Exception\("Failed"\)
       16\│ 
       17\│ 
       18\│ @pytest.mark.skipif\(PY36, reason="Legacy error messages are Python <3.6 only"\)
       19\│ def test_render_legacy_error_message\(\):
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

  \d+  {}:163 in test_render_debug_better_error_message_recursion_error
        161\│ 
        162\│     try:
      → 163\│         recursion_error\(\)
        164\│     except RecursionError as e:
        165\│         trace = ExceptionTrace\(e\)

  ...  Previous frame repeated \d+ times

  \s*\d+  {}:152 in recursion_error
        150\│ 
        151\│ def recursion_error\(\):
      → 152\│     recursion_error\(\)
        153\│ 
        154\│ 

  RecursionError

  maximum recursion depth exceeded

  at {}:152 in recursion_error
      148\│     assert re.match\(expected, io.fetch_output\(\)\) is not None
      149\│ 
      150\│ 
      151\│ def recursion_error\(\):
    → 152\│     recursion_error\(\)
      153\│ 
      154\│ 
      155\│ @pytest.mark.skipif\(
      156\│     not PY36, reason="Better error messages are only available for Python \^3\.6"
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

  1  {}:219 in test_render_verbose_better_error_message
     fail\(\)

  Exception

  Failed

  at {}:15 in fail
       11\│ from clikit.utils._compat import PY38
       12\│ 
       13\│ 
       14\│ def fail\(\):
    →  15\│     raise Exception\("Failed"\)
       16\│ 
       17\│ 
       18\│ @pytest.mark.skipif\(PY36, reason="Legacy error messages are Python <3.6 only"\)
       19\│ def test_render_legacy_error_message\(\):
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

    expected = r"...  Previous 2 frames repeated \d+ times"

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

  4  {}:352 in test_render_shows_ignored_files_if_in_debug_mode
      350│ 
      351│     with pytest.raises(Exception) as e:
    → 352│         call()
      353│ 
      354│     trace = ExceptionTrace(e.value)

  3  {}:349 in call
      347│             outer()
      348│ 
    → 349│         run()
      350│ 
      351│     with pytest.raises(Exception) as e:

  2  {}:347 in run
      345│     def call():
      346│         def run():
    → 347│             outer()
      348│ 
      349│         run()

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
    from crashtest.contracts.base_solution import BaseSolution
    from crashtest.contracts.provides_solution import ProvidesSolution
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

  at {}:434 in call
      430│ 
      431│     io = BufferedIO()
      432│ 
      433│     def call():
    → 434│         raise CustomError("Error with solution")
      435│ 
      436│     with pytest.raises(CustomError) as e:
      437│         call()
      438│ 

  • Solution Title: Solution Description
    https://example.com,
    https://example2.com
""".format(
        trace._get_relative_file_path(__file__),
    )

    assert expected == io.fetch_output()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_falls_back_on_ascii_symbols():
    from crashtest.contracts.base_solution import BaseSolution
    from crashtest.contracts.provides_solution import ProvidesSolution
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

    io = BufferedIO(supports_utf8=False)

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

  at {}:493 in call
      489| 
      490|     io = BufferedIO(supports_utf8=False)
      491| 
      492|     def call():
    > 493|         raise CustomError("Error with solution")
      494| 
      495|     with pytest.raises(CustomError) as e:
      496|         call()
      497| 

  * Solution Title: Solution Description
    https://example.com,
    https://example2.com
""".format(
        trace._get_relative_file_path(__file__),
    )

    assert expected == io.fetch_output()
