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

  at {}:43 in test_render_better_error_message
       39| def test_render_better_error_message():
       40|     io = BufferedIO()
       41| 
       42|     try:
    >  43|         raise Exception("Failed")
       44|     except Exception as e:
       45|         trace = ExceptionTrace(e)
       46| 
       47|     trace.render(io)
""".format(
        __file__
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
  File "{}", line 77, in test_render_verbose_legacy
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
  Exception

  Failed

  at {}:13 in fail
        9\| from clikit.utils._compat import PY38
       10\| 
       11\| 
       12\| def fail\(\):
    >  13\|     raise Exception\("Failed"\)
       14\| 
       15\| 
       16\| @pytest.mark.skipif\(PY36, reason="Legacy error messages are Python <3.6 only"\)
       17\| def test_render_legacy_error_message\(\):

  Stack trace:

  1  {}:111 in test_render_debug_better_error_message
      109\| 
      110\|     try:
    > 111\|         fail\(\)
      112\|     except Exception as e:  # Exception
      113\|         trace = ExceptionTrace\(e\)
""".format(
        re.escape(__file__), re.escape(__file__)
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
  RecursionError

  maximum recursion depth exceeded

  at {}:149 in recursion_error
      145\|     assert re.match\(expected, io.fetch_output\(\)\) is not None
      146\| 
      147\| 
      148\| def recursion_error\(\):
    > 149\|     recursion_error\(\)
      150\| 
      151\| 
      152\| @pytest.mark.skipif\(
      153\|     not PY36, reason="Better error messages are only available for Python \^3\.6"

  Stack trace:

  ...  Previous 1 frame repeated \d+ times

  \d+  {}:149 in recursion_error
        147\| 
        148\| def recursion_error\(\):
      > 149\|     recursion_error\(\)
        150\| 
        151\| 

  \d+  {}:160 in test_render_debug_better_error_message_recursion_error
        158\| 
        159\|     try:
      > 160\|         recursion_error\(\)
        161\|     except RecursionError as e:
        162\|         trace = ExceptionTrace\(e\)
""".format(
        re.escape(__file__), re.escape(__file__), re.escape(__file__)
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
  Exception

  Failed

  at {}:13 in fail
        9\| from clikit.utils._compat import PY38
       10\| 
       11\| 
       12\| def fail\(\):
    >  13\|     raise Exception\("Failed"\)
       14\| 
       15\| 
       16\| @pytest.mark.skipif\(PY36, reason="Legacy error messages are Python <3.6 only"\)
       17\| def test_render_legacy_error_message\(\):

  Stack trace:

  1  {}:214 in test_render_verbose_better_error_message
     fail\(\)
""".format(
        re.escape(__file__), re.escape(__file__)
    )

    assert re.match(expected, io.fetch_output()) is not None
