import sys

from io import StringIO

import pytest

from clikit.io.output_stream.stream_output_stream import StreamOutputStream


@pytest.fixture()
def stdout():
    original_encoding = sys.stdout.encoding

    yield sys.stdout

    sys.stdout.encoding = original_encoding


def test_supports_utf8_without_encoding(mocker):
    mocker.patch("locale.getpreferredencoding", return_value="ascii")
    stream = StringIO("")
    output_stream = StreamOutputStream(stream)

    assert not output_stream.supports_utf8()

    mocker.patch("locale.getpreferredencoding", return_value="utf-8")
    output_stream = StreamOutputStream(stream)

    assert output_stream.supports_utf8()


def test_supports_utf8_with_encoding(environ, stdout):
    stdout.encoding = "ascii"
    output_stream = StreamOutputStream(stdout)

    assert not output_stream.supports_utf8()

    stdout.encoding = "UTF8"
    output_stream = StreamOutputStream(stdout)

    assert output_stream.supports_utf8()
