import re
import pytest

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

at {}:42 in test_render_better_error_message
     38| def test_render_better_error_message():
     39|     io = BufferedIO()
     40| 
     41|     try:
  >  42|         raise Exception("Failed")
     43|     except Exception as e:
     44|         trace = ExceptionTrace(e)
     45| 
     46|     trace.render(io)
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
  File "{}", line 76, in test_render_verbose_legacy
    raise Exception({})

""".format(
        __file__, msg
    )
    assert expected == io.fetch_output()


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

at {}:12 in fail
      8| from clikit.utils._compat import PY38
      9| 
     10| 
     11| def fail():
  >  12|     raise Exception("Failed")
     13| 
     14| 
     15| @pytest.mark.skipif(PY36, reason="Legacy error messages are Python <3.6 only")
     16| def test_render_legacy_error_message():

Stack trace:

 1 at {}:110 in test_render_verbose_better_error_message
    108| 
    109|     try:
  > 110|         fail()
    111|     except Exception as e:  # Exception
    112|         trace = ExceptionTrace(e)
""".format(
        re.escape(__file__), re.escape(__file__)
    )

    assert re.match(expected, io.fetch_output()) is not None


def recursion_error():
    recursion_error()


@pytest.mark.skipif(
    not PY36, reason="Better error messages are only available for Python ^3.6"
)
def test_render_verbose_better_error_message_recursion_error():
    io = BufferedIO()
    io.set_verbosity(VERBOSE)

    try:
        recursion_error()
    except RecursionError as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = r"""^
RecursionError

maximum recursion depth exceeded

at {}:148 in recursion_error
    144\|     assert re.match\(expected, io.fetch_output\(\)\) is not None
    145\| 
    146\| 
    147\| def recursion_error\(\):
  > 148\|     recursion_error\(\)
    149\| 
    150\| 
    151\| @pytest.mark.skipif\(
    152\|     not PY36, reason="Better error messages are only available for Python \^3\.6"

Stack trace:

... Previous 1 frame repeated \d+ times

\d+ at {}:148 in recursion_error
    146\| 
    147\| def recursion_error\(\):
  > 148\|     recursion_error\(\)
    149\| 
    150\| 

\d+ at {}:159 in test_render_verbose_better_error_message_recursion_error
    157\| 
    158\|     try:
  > 159\|         recursion_error\(\)
    160\|     except RecursionError as e:
    161\|         trace = ExceptionTrace\(e\)
""".format(
        re.escape(__file__), re.escape(__file__), re.escape(__file__)
    )

    assert re.match(expected, io.fetch_output()) is not None
