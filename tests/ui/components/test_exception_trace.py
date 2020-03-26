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
  RecursionError

  maximum recursion depth exceeded

  at {}:150 in recursion_error
      146\|     assert re.match\(expected, io.fetch_output\(\)\) is not None
      147\| 
      148\| 
      149\| def recursion_error\(\):
    > 150\|     recursion_error\(\)
      151\| 
      152\| 
      153\| @pytest.mark.skipif\(
      154\|     not PY36, reason="Better error messages are only available for Python \^3\.6"

  Stack trace:

  ...  Previous frame repeated \d+ times

  \d+  {}:150 in recursion_error
        148\| 
        149\| def recursion_error\(\):
      > 150\|     recursion_error\(\)
        151\| 
        152\| 

  \d+  {}:161 in test_render_debug_better_error_message_recursion_error
        159\| 
        160\|     try:
      > 161\|         recursion_error\(\)
        162\|     except RecursionError as e:
        163\|         trace = ExceptionTrace\(e\)
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

  1  {}:217 in test_render_verbose_better_error_message
     fail\(\)
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
