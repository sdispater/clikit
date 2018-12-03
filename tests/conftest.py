import pytest

from clikit.io import BufferedIO


@pytest.fixture()
def io():
    return BufferedIO()
