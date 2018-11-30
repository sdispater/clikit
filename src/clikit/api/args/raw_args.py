from typing import List
from typing import Optional


class RawArgs(object):
    """
    The unparsed console arguments.
    """

    @property
    def script_name(self):  # type: () -> Optional[str]
        raise NotImplementedError()

    @property
    def tokens(self):  # type: () -> List[str]
        raise NotImplementedError()

    def has_token(self, token):  # type: (str) -> bool
        raise NotImplementedError()

    def to_string(self, script_name=True):  # type: (bool) -> str
        raise NotImplementedError()
