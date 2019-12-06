import pytest

from clikit.api.args.exceptions import CannotParseArgsException
from clikit.api.args.exceptions import NoSuchOptionException
from clikit.api.args.format import ArgsFormatBuilder
from clikit.api.args.format import Argument
from clikit.api.args.format import CommandName
from clikit.api.args.format import Option
from clikit.args import DefaultArgsParser
from clikit.args import StringArgs


@pytest.fixture()
def parser():
    return DefaultArgsParser()


def test_parse_command_names(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    fmt = builder.format

    args = parser.parse(StringArgs("server add"), fmt)

    assert [server, add] == args.command_names
    assert {} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_command_name_aliases(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server", ["server-alias"])
    add = CommandName("add", ["add-alias"])
    builder.add_command_names(server, add)
    fmt = builder.format

    args = parser.parse(StringArgs("server-alias add-alias"), fmt)

    assert [server, add] == args.command_names
    assert {} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_ignores_missing_command_names(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server", ["server-alias"])
    add = CommandName("add", ["add-alias"])
    builder.add_command_names(server, add)
    fmt = builder.format

    args = parser.parse(StringArgs(""), fmt)

    assert [server, add] == args.command_names
    assert {} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_arguments(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    builder.add_argument(Argument("argument2"))
    fmt = builder.format

    args = parser.parse(StringArgs("server add foo bar"), fmt)

    assert {"argument1": "foo", "argument2": "bar"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_arguments_ignores_missing_command_names(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    builder.add_argument(Argument("argument2"))
    fmt = builder.format

    args = parser.parse(StringArgs("server foo bar"), fmt)

    assert {"argument1": "foo", "argument2": "bar"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_arguments_ignores_missing_command_name_aliases(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server", ["server-alias"])
    add = CommandName("add", ["add-alias"])
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    builder.add_argument(Argument("argument2"))
    fmt = builder.format

    args = parser.parse(StringArgs("server-alias foo bar"), fmt)

    assert {"argument1": "foo", "argument2": "bar"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_arguments_ignores_missing_optional_arguments(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    builder.add_argument(Argument("argument2"))
    fmt = builder.format

    args = parser.parse(StringArgs("server add foo"), fmt)

    assert {"argument1": "foo"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_fails_if_missing_required_argument(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1", Argument.REQUIRED))
    builder.add_argument(Argument("argument2", Argument.REQUIRED))
    fmt = builder.format

    with pytest.raises(CannotParseArgsException):
        parser.parse(StringArgs("server add foo"), fmt)


def test_parse_does_not_fail_if_missing_required_argument_and_lenient(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1", Argument.REQUIRED))
    builder.add_argument(Argument("argument2", Argument.REQUIRED))
    fmt = builder.format

    args = parser.parse(StringArgs("server add foo"), fmt, True)

    assert {"argument1": "foo"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_fails_if_missing_required_argument_with_missing_command_name(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1", Argument.REQUIRED))
    builder.add_argument(Argument("argument2", Argument.REQUIRED))
    fmt = builder.format

    with pytest.raises(CannotParseArgsException):
        parser.parse(StringArgs("server foo"), fmt)


def test_parse_does_not_fail_if_missing_required_argument_with_missing_command_name_and_lenient(
    parser,
):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1", Argument.REQUIRED))
    builder.add_argument(Argument("argument2", Argument.REQUIRED))
    fmt = builder.format

    args = parser.parse(StringArgs("server foo"), fmt, True)

    assert {"argument1": "foo"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_fail_if_too_many_arguments(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    fmt = builder.format

    with pytest.raises(CannotParseArgsException):
        parser.parse(StringArgs("server add foo bar"), fmt)


def test_parse_does_not_fail_if_too_many_arguments_and_lenient(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    fmt = builder.format

    args = parser.parse(StringArgs("server add foo bar"), fmt, True)

    assert {"argument1": "foo"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_fail_if_too_many_arguments_with_missing_command_name(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    fmt = builder.format

    with pytest.raises(CannotParseArgsException):
        parser.parse(StringArgs("server foo bar"), fmt)


def test_parse_does_not_fail_if_too_many_arguments_with_missing_command_name_and_lenient(
    parser,
):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument1"))
    fmt = builder.format

    args = parser.parse(StringArgs("server foo bar"), fmt, True)

    assert {"argument1": "foo"} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_multi_valued_arguments(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("multi", Argument.MULTI_VALUED))
    fmt = builder.format

    args = parser.parse(StringArgs("server add one two three"), fmt)

    assert {"multi": ["one", "two", "three"]} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_multi_valued_arguments_ignores_missing_command_names(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("multi", Argument.MULTI_VALUED))
    fmt = builder.format

    args = parser.parse(StringArgs("server one two three"), fmt)

    assert {"multi": ["one", "two", "three"]} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_long_option_without_value(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option"))
    fmt = builder.format

    args = parser.parse(StringArgs("server add --option"), fmt)

    assert {} == args.arguments(False)
    assert {"option": True} == args.options(False)


def test_parse_long_option_with_value(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option", flags=Option.OPTIONAL_VALUE))
    fmt = builder.format

    args = parser.parse(StringArgs("server add --option foo"), fmt)

    assert {} == args.arguments(False)
    assert {"option": "foo"} == args.options(False)


def test_parse_long_option_with_value2(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option", flags=Option.OPTIONAL_VALUE))
    fmt = builder.format

    args = parser.parse(StringArgs("server add --option=foo"), fmt)

    assert {} == args.arguments(False)
    assert {"option": "foo"} == args.options(False)


def test_parse_long_option_fails_if_missing_value(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option", flags=Option.REQUIRED_VALUE))
    fmt = builder.format

    with pytest.raises(CannotParseArgsException) as e:
        parser.parse(StringArgs("server add --option"), fmt)

    assert 'The "--option" option requires a value.' == str(e.value)


def test_parse_short_option_without_value(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option", "o"))
    fmt = builder.format

    args = parser.parse(StringArgs("server add -o"), fmt)

    assert {} == args.arguments(False)
    assert {"option": True} == args.options(False)


def test_parse_short_option_with_value(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option", "o", flags=Option.OPTIONAL_VALUE))
    fmt = builder.format

    args = parser.parse(StringArgs("server add -o foo"), fmt)

    assert {} == args.arguments(False)
    assert {"option": "foo"} == args.options(False)


def test_parse_short_option_with_value2(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option", "o", flags=Option.OPTIONAL_VALUE))
    fmt = builder.format

    args = parser.parse(StringArgs("server add -ofoo"), fmt)

    assert {} == args.arguments(False)
    assert {"option": "foo"} == args.options(False)


def test_parse_short_option_fails_if_missing_value(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_option(Option("option", "o", flags=Option.REQUIRED_VALUE))
    fmt = builder.format

    with pytest.raises(CannotParseArgsException) as e:
        parser.parse(StringArgs("server add -o"), fmt)

    assert 'The "--option" option requires a value.' == str(e.value)


def test_option_fails_if_invalid_option(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    fmt = builder.format

    with pytest.raises(NoSuchOptionException) as e:
        parser.parse(StringArgs("server add --foo"), fmt)

    assert 'The "--foo" option does not exist.' == str(e.value)


def test_parse_option_stops_parsing_if_invalid_option_and_lenient(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    fmt = builder.format

    args = parser.parse(StringArgs("server add --foo bar"), fmt, True)

    assert {} == args.arguments(False)
    assert {} == args.options(False)


def test_parse_option_up_to_invalid_option_if_lenient(parser):
    builder = ArgsFormatBuilder()
    server = CommandName("server")
    add = CommandName("add")
    builder.add_command_names(server, add)
    builder.add_argument(Argument("argument"))
    fmt = builder.format

    args = parser.parse(StringArgs("server add bar --foo"), fmt, True)

    assert {"argument": "bar"} == args.arguments(False)
    assert {} == args.options(False)
