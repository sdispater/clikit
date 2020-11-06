from typing import TYPE_CHECKING
from typing import List


if TYPE_CHECKING:
    from .output import Output


class Indent:
    def __init__(
        self, outputs, indent, increment=False
    ):  # type: (List[Output], int, bool) -> None
        self._outputs = outputs
        self._original_indents = [output._indent for output in outputs]

        for output in outputs:
            if increment:
                output._indent = output._indent + indent
            else:
                output._indent = indent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i, output in enumerate(self._outputs):
            output._indent = self._original_indents[i]
