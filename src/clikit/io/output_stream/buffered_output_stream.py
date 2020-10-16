from clikit.api.io import OutputStream
from clikit.utils._compat import decode


class BufferedOutputStream(OutputStream):
    """
    An output stream that writes to a buffer.
    """

    def __init__(self, supports_utf8=True):  # type: (bool) -> None
        self._buffer = ""
        self._closed = False
        self._supports_utf8 = supports_utf8

    def fetch(self):  # type: () -> str
        return self._buffer

    def clear(self):  # type: () -> None
        self._buffer = ""

    def write(self, string):  # type: (str) -> None
        """
        Writes a string to the stream.
        """
        if self._closed:
            raise IOError("Cannot read from a closed input.")

        self._buffer += decode(string)

    def flush(self):  # type: () -> None
        """
        Flushes the stream and forces all pending text to be written out.
        """
        if self._closed:
            raise IOError("Cannot read from a closed input.")

    def supports_ansi(self):  # type: () -> bool
        """
        Returns whether the stream supports ANSI format codes.
        """
        return False

    def supports_utf8(self):  # type: () -> bool
        return self._supports_utf8

    def close(self):  # type: () -> None
        """
        Closes the stream.
        """
        self._closed = True

    def is_closed(self):  # type: () -> bool
        """
        Returns whether the stream is closed.
        """
        return self._closed
