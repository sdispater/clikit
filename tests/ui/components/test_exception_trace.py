from clikit.api.io.flags import VERBOSE
from clikit.io.buffered_io import BufferedIO
from clikit.ui.components.exception_trace import ExceptionTrace
from clikit.utils._compat import PY2, PY38


def test_render():
    io = BufferedIO()

    try:
        raise Exception("Failed")
    except Exception as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = """\

[Exception]
Failed
"""
    assert expected == io.fetch_output()


def test_render_verbose():
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

[Exception]
Failed

Traceback (most recent call last):
  File "{}", line 30, in test_render_verbose
    raise Exception({})

""".format(
        __file__, msg
    )
    assert expected == io.fetch_output()
