import ast
import inspect
import keyword
import math
import sys
import traceback

from clikit.api.io import IO


class ExceptionTrace(object):
    """
    Renders the trace of an exception.
    """

    THEME = {
        "comment": "<fg=black;options=bold>",
        "keyword": "<fg=yellow>",
        "builtin": "<fg=blue>",
        "literal": "<fg=magenta>",
    }

    AST_ELEMENTS = {
        "builtins": __builtins__.keys()
        if type(__builtins__) is dict
        else dir(__builtins__),
        "keywords": [
            getattr(ast, cls)
            for cls in dir(ast)
            if keyword.iskeyword(cls.lower())
            and inspect.isclass(getattr(ast, cls))
            and issubclass(getattr(ast, cls), ast.AST)
        ],
    }

    def __init__(self, exception):  # type: (Exception) -> None
        self._exception = exception
        self._exc_info = sys.exc_info()

    def render(self, io):  # type: (IO) -> None
        if hasattr(self._exception, "__traceback__"):
            tb = self._exception.__traceback__
        else:
            tb = self._exc_info[2]

        title = "\n[<error>{}</error>]\n<error>{}</error>".format(
            self._exception.__class__.__name__, str(self._exception)
        )
        io.write_line(title)

        if io.is_verbose():
            io.write_line("")
            self._render_traceback(io, tb)

    def _render_traceback(self, io, tb):  # type: (IO, ...) -> None
        frames = []
        while tb:
            frames.append(self._format_traceback_frame(io, tb))

            tb = tb.tb_next

        io.write_line("<comment>Traceback (most recent call last):</comment>")
        io.write_line("".join(traceback.format_list(frames)))

    def _format_traceback_frame(self, io, tb):  # type: (IO, ...) -> Tuple[Any]
        frame_info = inspect.getframeinfo(tb)
        filename = frame_info.filename
        lineno = frame_info.lineno
        function = frame_info.function
        line = frame_info.code_context[0]

        stripped_line = line.lstrip(" ")
        try:
            tree = ast.parse(stripped_line, mode="exec")
            formatted = self._format_tree(tree, stripped_line, io)
            formatted = (len(line) - len(stripped_line)) * " " + formatted
        except SyntaxError:
            formatted = line

        return (
            io.format("<info>{}</info>".format(filename)),
            lineno,
            function,
            formatted,
        )

    def _format_tree(self, tree, source, io):
        offset = 0
        chunks = []

        nodes = [n for n in ast.walk(tree)]

        displayed_nodes = []

        for node in nodes:
            nodecls = node.__class__
            nodename = nodecls.__name__

            if "col_offset" not in dir(node):
                continue

            if nodecls in self.AST_ELEMENTS["keywords"]:
                displayed_nodes.append((node, nodename.lower(), "keyword"))
            elif nodecls == ast.Name and node.id in self.AST_ELEMENTS["builtins"]:
                displayed_nodes.append((node, node.id, "builtin"))
            elif nodecls == ast.Str:
                displayed_nodes.append((node, "'{}'".format(node.s), "literal"))
            elif nodecls == ast.Num:
                displayed_nodes.append((node, str(node.n), "literal"))

        displayed_nodes.sort(key=lambda elem: elem[0].col_offset)

        for dn in displayed_nodes:
            node = dn[0]
            s = dn[1]
            theme = dn[2]

            begin_col = node.col_offset

            src_chunk = source[offset:begin_col]
            chunks.append(src_chunk)
            chunks.append(io.format("{}{}</>".format(self.THEME[theme], s)))
            offset = begin_col + len(s)

        chunks.append(source[offset:])

        return "".join(chunks)
