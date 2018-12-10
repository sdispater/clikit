import pytest

from clikit.formatter import AnsiFormatter
from clikit.io import BufferedIO


@pytest.fixture()
def io():
    return BufferedIO()


@pytest.fixture()
def ansi_io():
    return BufferedIO(formatter=AnsiFormatter(forced=True))
