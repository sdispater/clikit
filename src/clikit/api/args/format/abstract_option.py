from typing import Optional


class AbstractOption(object):
    """
    Base class for command line options.
    """

    PREFER_LONG_NAME = 1
    PREFER_SHORT_NAME = 2

    def __init__(
        self, long_name, short_name=None, flags=0, description=None
    ):  # type: (str, Optional[str], int, Optional[str]) -> None
        long_name = self._remove_double_dash_prefix(long_name)
        short_name = self._remove_dash_prefix(short_name)

        self._validate_flags(flags)
        # TODO verify names

        self._long_name = long_name
        self._short_name = short_name
        self._description = description

        flags = self._add_default_flags(flags)

        self._flags = flags

    @property
    def long_name(self):  # type: () -> str
        return self._long_name

    @property
    def short_name(self):  # type: () -> Optional[str]
        return self._short_name

    @property
    def flags(self):  # type: () -> int
        return self._flags

    @property
    def description(self):  # type: () -> Optional[str]
        return self._description

    def is_long_name_preferred(self):  # type: () -> bool
        return bool(self._flags & self.PREFER_LONG_NAME)

    def is_short_name_preferred(self):  # type: () -> bool
        return bool(self._flags & self.PREFER_SHORT_NAME)

    def _remove_double_dash_prefix(self, string):  # type: (str) -> str
        if string.startswith("--"):
            string = string[2:]

        return string

    def _remove_dash_prefix(self, string):  # type: (Optional[str]) -> Optional[str]
        if string is None:
            return string

        if string.startswith("-"):
            string = string[1:]

        return string

    def _validate_flags(self, flags):  # type: (int) -> None
        if flags & self.PREFER_SHORT_NAME and flags & self.PREFER_SHORT_NAME:
            raise ValueError(
                "The option flags PREFER_SHORT_NAME and PREFER_LONG_NAME cannot be combined."
            )

    def _add_default_flags(self, flags):  # type: (int) -> int
        if not flags & (self.PREFER_LONG_NAME | self.PREFER_SHORT_NAME):
            flags |= (
                self.PREFER_SHORT_NAME if self._short_name else self.PREFER_LONG_NAME
            )

        return flags
