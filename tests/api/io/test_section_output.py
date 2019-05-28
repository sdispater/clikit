import pytest

from clikit.api.io.section_output import SectionOutput
from clikit.formatter.ansi_formatter import AnsiFormatter
from clikit.io.output_stream.buffered_output_stream import BufferedOutputStream


@pytest.fixture()
def stream():
    return BufferedOutputStream()


@pytest.fixture()
def sections():
    return []


@pytest.fixture()
def output(stream, sections):
    return SectionOutput(stream, sections, AnsiFormatter(forced=True))


@pytest.fixture()
def output2(stream, sections):
    return SectionOutput(stream, sections, AnsiFormatter(forced=True))


def test_clear_all(output, stream):
    output.write_line("Foo\nBar")
    output.clear()

    assert "Foo\nBar\n\x1b[2A\x1b[0J" == stream.fetch()


def test_clear_with_number_of_lines(output, stream):
    output.write_line("Foo\nBar\nBaz\nFooBar")
    output.clear(2)

    assert "Foo\nBar\nBaz\nFooBar\n\x1b[2A\x1b[0J" == stream.fetch()


def test_clear_with_number_of_lines_and_multiple_sections(output, output2, stream):
    output2.write_line("Foo")
    output2.write_line("Bar")
    output2.clear(1)
    output.write_line("Baz")

    assert "Foo\nBar\n\x1b[1A\x1b[0J\x1b[1A\x1b[0JBaz\nFoo\n" == stream.fetch()


def test_clear_preserves_empty_lines(output, output2, stream):
    output2.write_line("\nFoo")
    output2.clear(1)
    output.write_line("Bar")

    assert "\nFoo\n\x1b[1A\x1b[0J\x1b[1A\x1b[0JBar\n\n" == stream.fetch()


def test_overwrite(output, stream):
    output.write_line("Foo")
    output.overwrite("Bar")

    assert "Foo\n\x1b[1A\x1b[0JBar\n" == stream.fetch()


def test_overwrite_multiple_lines(output, stream):
    output.write_line("Foo\nBar\nBaz")
    output.overwrite("Bar")

    assert "Foo\nBar\nBaz\n\x1b[3A\x1b[0JBar\n" == stream.fetch()


def test_add_multiple_sections(output, output2, sections):
    assert 2 == len(sections)


def test_multiple_sections_output(output, output2, stream):
    output.write_line("Foo")
    output2.write_line("Bar")

    output.overwrite("Baz")
    output2.overwrite("Foobar")

    assert (
        "Foo\nBar\n\x1b[2A\x1b[0JBar\n\x1b[1A\x1b[0JBaz\nBar\n\x1b[1A\x1b[0JFoobar\n"
        == stream.fetch()
    )
