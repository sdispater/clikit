from clikit.api.io.output import Output
from clikit.io.output_stream.buffered_output_stream import BufferedOutputStream


def test_supports_utf8():
    output = Output(BufferedOutputStream())

    assert output.supports_utf8()

    output = Output(BufferedOutputStream(supports_utf8=False))

    assert not output.supports_utf8()


def test_indent():
    output = Output(BufferedOutputStream())

    output.indent(2)

    output.write_line("Foo")
    output.write("Bar\nBaz", new_line=True)

    output.indent(4)

    output.write_line("Foo")
    output.write("Bar\nBaz", new_line=True)

    with output.indent(3):
        output.write_line("Foo")
        output.write("Bar\nBaz", new_line=True)

    output.write_line("Foo")
    output.write("Bar\nBaz", new_line=True)

    expected = """\
  Foo
  Bar
  Baz
    Foo
    Bar
    Baz
   Foo
   Bar
   Baz
    Foo
    Bar
    Baz
"""

    assert expected == output.stream.fetch()


def test_increment_indent():
    output = Output(BufferedOutputStream())

    output.increment_indent(2)

    output.write_line("Foo")
    output.write("Bar\nBaz", new_line=True)

    output.increment_indent(2)

    output.write_line("Foo")
    output.write("Bar\nBaz", new_line=True)

    with output.increment_indent(-1):
        output.write_line("Foo")
        output.write("Bar\nBaz", new_line=True)

    output.write_line("Foo")
    output.write("Bar\nBaz", new_line=True)

    expected = """\
  Foo
  Bar
  Baz
    Foo
    Bar
    Baz
   Foo
   Bar
   Baz
    Foo
    Bar
    Baz
"""

    assert expected == output.stream.fetch()
