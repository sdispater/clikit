from typing import List
from typing import Optional


from clikit.api.args.args_parser import ArgsParser
from clikit.api.args.format.args_format import ArgsFormat
from clikit.api.args.format.argument import Argument
from clikit.api.args.args import Args
from clikit.api.args.exceptions import CannotParseArgsException
from clikit.api.args.exceptions import NoSuchOptionException
from clikit.api.args.raw_args import RawArgs


class DefaultArgsParser(ArgsParser):
    """
    Default parser for RawArgs instances.
    """

    def __init__(self):  # type: () -> None
        self._arguments = 0

    def parse(
        self, args, fmt, lenient=False
    ):  # type: (RawArgs, ArgsFormat, bool) -> Args
        self._arguments = 0

        arguments = []
        for i, command_name in enumerate(fmt.get_command_names()):
            arguments.append(Argument("cmd{}".format(i)))

        for arg in fmt.get_arguments().values():
            arguments.append(arg)

        fmt = ArgsFormat(
            fmt.get_command_names() + arguments + list(fmt.get_options().values())
        )

        parsed_args = Args(fmt, args)
        # self._insert_missing_command_names(fmt, lenient)

        self._parse(args, parsed_args)

        return parsed_args

    def _parse(self, raw_args, args):  # type: (RawArgs, Args) -> None
        tokens = raw_args.tokens[:]

        parse_options = True
        while True:
            try:
                token = tokens.pop(0)
            except IndexError:
                break

            if parse_options and token == "":
                self._parse_argument(token, args)
            elif parse_options and token == "--":
                parse_options = False
            elif parse_options and token.find("--") == 0:
                self._parse_long_option(token, tokens, args)
            elif parse_options and token[0] == "-" and token != "-":
                self._parse_short_option(token, tokens, args)
            else:
                self._parse_argument(token, args)

    def _parse_argument(self, token, args):  # type: (str, Args) -> None
        c = self._arguments

        # if input is expecting another argument, add it
        if args.is_argument_defined(c):
            args.set_argument(c, token)
        elif (
            args.is_argument_defined(c - 1)
            and args.format.get_argument(c - 1).is_multi_valued()
        ):
            args.set_argument(c - 1, token)
        # unexpected argument
        else:
            raise CannotParseArgsException.too_many_arguments()

        self._arguments += 1

    def _parse_long_option(
        self, token, tokens, args
    ):  # type: (str, List[str], Args) -> None
        name = token[2:]
        pos = name.find("=")
        if pos != -1:
            self._add_long_option(name[:pos], name[pos + 1 :], tokens, args)
        else:
            if (
                args.is_option_defined(name)
                and args.format.get_option(name).accepts_value()
            ):
                try:
                    value = tokens.pop(0)
                except IndexError:
                    value = None

                if value and value.startswith("-"):
                    tokens.insert(0, value)
                    value = None

                self._add_long_option(name, value, tokens, args)
            else:
                self._add_long_option(name, None, tokens, args)

    def _parse_short_option(
        self, token, tokens, args
    ):  # type: (str, List[str], Args) -> None
        name = token[1:]
        if len(name) > 1:
            if (
                args.is_option_defined(name[0])
                and args.format.get_option(name[0]).accepts_value()
            ):
                # an option with a value (with no space)
                self._add_short_option(name[0], name[1], tokens, args)
            else:
                self._parse_short_option_set(name, tokens, args)
        else:
            if (
                args.is_option_defined(name[0])
                and args.format.get_option(name[0]).accepts_value()
            ):
                try:
                    value = tokens.pop(0)
                except IndexError:
                    value = None

                if value and value.startswith("-"):
                    tokens.insert(0, value)
                    value = None

                self._add_short_option(name, value, tokens, args)
            else:
                self._add_short_option(name, None, tokens, args)

    def _parse_short_option_set(
        self, name, tokens, args
    ):  # type: (str, List[str], Args) -> None
        l = len(name)
        for i in range(0, l):
            if not args.is_option_defined(name[i]):
                raise NoSuchOptionException(name[i])

            option = args.format.get_option(name[i])
            if option.accepts_value():
                self._add_long_option(
                    option.long_name,
                    None if l - 1 == i else name[i + 1 :],
                    tokens,
                    args,
                )

                break
            else:
                self._add_long_option(option.long_name, None, tokens, args)

    def _add_long_option(
        self, name, value, tokens, args
    ):  # type: (str, Optional[str], List[str], Args) -> None
        if not args.is_option_defined(name):
            raise NoSuchOptionException(name)

        option = args.format.get_option(name)

        if value is False:
            value = None

        if value is not None and not option.accepts_value():
            raise CannotParseArgsException.option_does_not_accept_value(name)

        if value is None and option.accepts_value() and len(tokens):
            # if option accepts an optional or mandatory argument
            # let's see if there is one provided
            try:
                nxt = tokens.pop(0)
            except IndexError:
                nxt = None

            if nxt and len(nxt) >= 1 and nxt[0] != "-":
                value = nxt
            elif not nxt:
                value = ""
            else:
                tokens.insert(0, nxt)

        # This test is here to handle cases like --foo=
        # and foo option value is optional
        if value == "":
            value = None

        if value is None:
            if option.is_value_required():
                raise CannotParseArgsException.option_requires_value(name)

            if not option.is_multi_valued():
                value = option.default if option.is_value_optional() else True

        args.set_option(name, value)

    def _add_short_option(
        self, name, value, tokens, args
    ):  # type: (str, Optional[str], List[str], Args) -> None
        if not args.is_option_defined(name):
            raise NoSuchOptionException(name)

        self._add_long_option(
            args.format.get_option(name).long_name, value, tokens, args
        )
