import os

import pytest

from clikit.formatter import AnsiFormatter
from clikit.io import BufferedIO


@pytest.fixture()
def io():
    return BufferedIO()


@pytest.fixture()
def ansi_io():
    return BufferedIO(formatter=AnsiFormatter(forced=True))


@pytest.fixture
def environ():
    original_environ = dict(os.environ)

    yield os.environ

    os.environ.clear()
    os.environ.update(original_environ)
