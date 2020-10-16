from clikit.io.output_stream.buffered_output_stream import BufferedOutputStream


def test_supports_utf8():
    output_stream = BufferedOutputStream()

    assert output_stream.supports_utf8()

    output_stream = BufferedOutputStream(supports_utf8=False)

    assert not output_stream.supports_utf8()
