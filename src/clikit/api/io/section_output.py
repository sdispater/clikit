import math

from typing import List
from typing import Optional

from clikit.api.formatter import Formatter
from clikit.utils.terminal import Terminal

from .output import Output
from .output_stream import OutputStream


class SectionOutput(Output):
    def __init__(
        self, stream, sections, formatter=None
    ):  # type: (OutputStream, List[SectionOutput], Optional[Formatter]) -> None
        super(SectionOutput, self).__init__(stream, formatter=formatter)

        self._content = []
        self._lines = 0
        sections.insert(0, self)
        self._sections = sections
        self._terminal = Terminal()

    @property
    def content(self):  # type: () -> str
        return "".join(self._content)

    @property
    def lines(self):  # type: () -> int
        return self._lines

    def clear(self, lines=None):  # type: (Optional[int]) -> None
        if (
            not self._content
            or not self.supports_ansi()
            and not self._formatter.force_ansi()
        ):
            return

        if lines:
            # Multiply lines by 2 to cater for each new line added between content
            del self._content[-(lines * 2) :]
        else:
            lines = self._lines
            self._content = []

        self._lines -= lines

        super(SectionOutput, self).write(
            self._pop_stream_content_until_current_section(lines), with_indent=False
        )

    def overwrite(self, message):  # type: (str) -> None
        self.clear()
        self.write_line(message)

    def add_content(self, content):  # type: (str) -> None
        if self._indent > 0:
            content = "\n".join((" " * self._indent + s) for s in content.split("\n"))

        for line_content in content.split("\n"):
            self._lines += (
                math.ceil(
                    len(self.remove_format(line_content).replace("\t", "        "))
                    / self._terminal.width
                )
                or 1
            )
            self._content.append(line_content)
            self._content.append("\n")

    def write(
        self, string, flags=None, new_line=False, with_indent=True
    ):  # type: (str, Optional[int], bool, bool) -> None
        if not self.supports_ansi() and not self._formatter.force_ansi():
            return super(SectionOutput, self).write(string, flags=flags)

        erased_content = self._pop_stream_content_until_current_section()

        self.add_content(string)

        super(SectionOutput, self).write(string, new_line=True, with_indent=True)
        super(SectionOutput, self).write(erased_content, with_indent=False)

    def _pop_stream_content_until_current_section(
        self, lines_to_clear_count=0
    ):  # type: (int) -> str
        erased_content = []

        for section in self._sections:
            if section is self:
                break

            lines_to_clear_count += section.lines
            erased_content.append(section.content)

        if lines_to_clear_count > 0:
            # Move cursor up n lines
            super(SectionOutput, self).write(
                "\x1b[{}A".format(lines_to_clear_count), with_indent=False
            )
            # Erase to end of screen
            super(SectionOutput, self).write("\x1b[0J", with_indent=False)

        return "".join(reversed(erased_content))
