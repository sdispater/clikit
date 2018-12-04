import time

from clikit.formatter import AnsiFormatter
from clikit.ui.components import ProgressIndicator


def test_default_indicator(io):
    bar = ProgressIndicator(io)
    bar.start("Starting...")
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.set_message("Advancing...")
    bar.advance()
    bar.finish("Done...")
    bar.start("Starting Again...")
    time.sleep(0.101)
    bar.advance()
    bar.finish("Done Again...")
    bar.start("Starting Again...")
    time.sleep(0.101)
    bar.advance()
    bar.finish("Done Again...", reset_indicator=True)

    expected = "\n".join([" Starting...", " Advancing...", " Done..."])

    expected += "\n\n"

    expected += "\n".join([" Starting Again...", " Done Again..."])

    expected += "\n\n"

    expected += "\n".join([" Starting Again...", " Done Again..."])

    expected += "\n\n"

    assert expected == io.fetch_output()


def test_explicit_format(io):
    io.set_formatter(AnsiFormatter())

    bar = ProgressIndicator(io, ProgressIndicator.NORMAL)
    bar.start("Starting...")
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.advance()
    time.sleep(0.101)
    bar.set_message("Advancing...")
    bar.advance()
    bar.finish("Done...")
    bar.start("Starting Again...")
    time.sleep(0.101)
    bar.advance()
    bar.finish("Done Again...")
    bar.start("Starting Again...")
    time.sleep(0.101)
    bar.advance()
    bar.finish("Done Again...", reset_indicator=True)

    expected = "\n".join(
        [
            " - Starting...",
            " \\ Starting...",
            " | Starting...",
            " / Starting...",
            " - Starting...",
            " \\ Starting...",
            " \\ Advancing...",
            " | Advancing...",
            " | Done...",
        ]
    )

    expected += "\n\n"

    expected += "\n".join(
        [" - Starting Again...", " \\ Starting Again...", " \\ Done Again..."]
    )

    expected += "\n\n"

    expected += "\n".join(
        [" - Starting Again...", " \\ Starting Again...", " - Done Again..."]
    )

    expected += "\n\n"

    assert expected == io.fetch_output()
