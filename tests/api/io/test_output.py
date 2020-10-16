from clikit.api.io.output import Output
from clikit.io.output_stream.buffered_output_stream import BufferedOutputStream


def test_supports_utf8():
    output = Output(BufferedOutputStream())

    assert output.supports_utf8()

    output = Output(BufferedOutputStream(supports_utf8=False))

    assert not output.supports_utf8()
