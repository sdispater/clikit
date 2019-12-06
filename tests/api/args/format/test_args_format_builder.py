import pytest

from clikit.api.args.exceptions import CannotAddArgumentException
from clikit.api.args.exceptions import CannotAddOptionException
from clikit.api.args.exceptions import NoSuchArgumentException
from clikit.api.args.exceptions import NoSuchOptionException
from clikit.api.args.format import ArgsFormat
from clikit.api.args.format import ArgsFormatBuilder
from clikit.api.args.format import Argument
from clikit.api.args.format import Option
from clikit.api.args.format.command_name import CommandName
from clikit.api.args.format.command_option import CommandOption


@pytest.fixture()
def base_format_builder():
    return ArgsFormatBuilder()


@pytest.fixture()
def base_format():
    return ArgsFormat()


@pytest.fixture()
def builder(base_format):
    return ArgsFormatBuilder(base_format)


def test_add_command_name(builder):
    server = CommandName("server")
    add = CommandName("add")

    builder.add_command_name(server)
    builder.add_command_name(add)

    assert [server, add] == builder.get_command_names()


def test_add_command_names(builder):
    server = CommandName("server")
    add = CommandName("add")

    builder.add_command_names(server, add)

    assert [server, add] == builder.get_command_names()


def test_set_command_names(builder):
    builder.add_command_name(CommandName("cluster"))

    server = CommandName("server")
    add = CommandName("add")

    builder.set_command_names(server, add)

    assert [server, add] == builder.get_command_names()


def test_has_command_names(builder):
    assert not builder.has_command_names()
    assert not builder.has_command_names(False)

    builder.add_command_name(CommandName("cluster"))

    assert builder.has_command_names()
    assert builder.has_command_names(False)


def test_has_command_names_with_base_definition(base_format_builder):
    base_format_builder.add_command_name(CommandName("server"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_command_names()
    assert not builder.has_command_names(False)

    builder.add_command_name(CommandName("add"))

    assert builder.has_command_names()
    assert builder.has_command_names(False)


def test_get_command_names(builder):
    server = CommandName("server")
    add = CommandName("add")

    builder.add_command_name(server)
    builder.add_command_name(add)

    assert [server, add] == builder.get_command_names()
    assert [server, add] == builder.get_command_names(False)


def test_get_command_names_with_base_definition(base_format_builder):
    server = CommandName("server")
    add = CommandName("add")

    base_format_builder.add_command_name(server)

    builder = ArgsFormatBuilder(base_format_builder.format)
    builder.add_command_name(add)

    assert [server, add] == builder.get_command_names()
    assert [add] == builder.get_command_names(False)


def test_add_command_option(builder):
    option = CommandOption("option")

    builder.add_command_option(option)

    assert [option] == builder.get_command_options()


def test_add_command_option_preserves_existing_options(builder):
    option1 = CommandOption("option1")
    option2 = CommandOption("option2")

    builder.add_command_option(option1)
    builder.add_command_option(option2)

    assert [option1, option2] == builder.get_command_options()


def test_add_command_fails_if_option_with_same_long_name_as_other_command_option(
    builder,
):
    builder.add_option(CommandOption("option", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_command_option(CommandOption("option", "b"))


def test_add_command_fails_if_option_with_same_long_name_as_other_option(builder):
    builder.add_option(Option("option", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_command_option(CommandOption("option", "b"))


def test_add_command_fails_if_option_with_same_long_name_as_option_in_base_format(
    base_format_builder,
):
    base_format_builder.add_option(Option("option", "a"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddOptionException):
        builder.add_command_option(CommandOption("option", "b"))


def test_add_command_fails_if_option_with_same_short_name_as_other_command_option(
    builder,
):
    builder.add_option(CommandOption("option", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_command_option(CommandOption("option2", "a"))


def test_add_command_fails_if_option_with_same_short_name_as_other_option(builder):
    builder.add_option(CommandOption("option", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_command_option(CommandOption("option2", "a"))


def test_add_command_fails_if_option_with_same_short_name_as_alias_of_other_option(
    builder,
):
    builder.add_option(CommandOption("option1", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_command_option(CommandOption("option2", "b", ["a"]))


def test_add_command_fails_if_option_with_same_short_name_as_option_in_base_format(
    base_format_builder,
):
    base_format_builder.add_option(Option("option", "a"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddOptionException):
        builder.add_command_option(CommandOption("option2", "a"))


def test_add_optional_argument(builder):
    arg = Argument("argument")

    builder.add_argument(arg)

    assert {"argument": arg} == builder.get_arguments()


def test_add_required_argument(builder):
    arg = Argument("argument", Argument.REQUIRED)

    builder.add_argument(arg)

    assert {"argument": arg} == builder.get_arguments()


def test_argument_preserves_existing_arguments(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    builder.add_argument(arg1)
    builder.add_argument(arg2)

    assert {"argument1": arg1, "argument2": arg2} == builder.get_arguments()


def test_fail_if_adding_required_argument_after_optional_argument(builder):
    builder.add_argument(Argument("argument1"))

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument2", Argument.REQUIRED))


def test_fail_if_adding_required_argument_after_optional_argument_in_base_definition(
    base_format_builder,
):
    base_format_builder.add_argument(Argument("argument1"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument2", Argument.REQUIRED))


def test_fail_if_adding_required_argument_after_multi_valued_argument(builder):
    builder.add_argument(Argument("argument1", Argument.MULTI_VALUED))

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument2", Argument.REQUIRED))


def test_fail_if_adding_required_argument_after_multi_valued_argument_in_base_definition(
    base_format_builder,
):
    base_format_builder.add_argument(Argument("argument1", Argument.MULTI_VALUED))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument2", Argument.REQUIRED))


def test_fail_if_adding_optional_argument_after_multi_valued_argument(builder):
    builder.add_argument(Argument("argument1", Argument.MULTI_VALUED))

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument2"))


def test_fail_if_adding_optional_argument_after_multi_valued_argument_in_base_definition(
    base_format_builder,
):
    base_format_builder.add_argument(Argument("argument1", Argument.MULTI_VALUED))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument2"))


def test_fail_if_adding_argument_with_existing_name(builder):
    builder.add_argument(Argument("argument", Argument.REQUIRED))

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument", Argument.OPTIONAL))


def test_fail_if_adding_argument_with_existing_name_in_base_definition(
    base_format_builder,
):
    base_format_builder.add_argument(Argument("argument", Argument.REQUIRED))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddArgumentException):
        builder.add_argument(Argument("argument", Argument.OPTIONAL))


def test_add_arguments(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")
    arg3 = Argument("argument3")

    builder.add_argument(arg1)
    builder.add_arguments(arg2, arg3)

    assert {
        "argument1": arg1,
        "argument2": arg2,
        "argument3": arg3,
    } == builder.get_arguments()


def test_set_arguments(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")
    arg3 = Argument("argument3")

    builder.add_argument(arg1)
    builder.set_arguments(arg2, arg3)

    assert {"argument2": arg2, "argument3": arg3} == builder.get_arguments()


def test_get_argument(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    builder.add_arguments(arg1, arg2)

    assert arg1 == builder.get_argument("argument1")
    assert arg2 == builder.get_argument("argument2")


def test_get_argument_from_base_definition(base_format_builder):
    arg = Argument("argument")
    base_format_builder.add_argument(arg)

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert arg == builder.get_argument("argument")


def test_get_argument_fails_if_unknown_name(builder):
    with pytest.raises(NoSuchArgumentException):
        builder.get_argument("foo")


def test_get_argument_by_position(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    builder.add_arguments(arg1, arg2)

    assert arg1 == builder.get_argument(0)
    assert arg2 == builder.get_argument(1)


def test_get_argument_by_position_from_base_definition(base_format_builder):
    arg = Argument("argument")
    base_format_builder.add_argument(arg)

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert arg == builder.get_argument(0)


def test_get_argument_by_position_fails_if_unknown_position(builder):
    with pytest.raises(NoSuchArgumentException):
        builder.get_argument(0)


def test_get_argument_fails_if_in_base_definition_but_include_base_disabled(
    base_format_builder,
):
    arg = Argument("argument")
    base_format_builder.add_argument(arg)

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(NoSuchArgumentException):
        builder.get_argument("argument", False)


def test_get_arguments(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    builder.add_arguments(arg1, arg2)

    assert {"argument1": arg1, "argument2": arg2} == builder.get_arguments()


def test_get_arguments_with_base_arguments(base_format_builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    base_format_builder.add_argument(arg1)

    builder = ArgsFormatBuilder(base_format_builder.format)

    builder.add_argument(arg2)

    assert {"argument1": arg1, "argument2": arg2} == builder.get_arguments()
    assert {"argument2": arg2} == builder.get_arguments(False)


def test_has_argument(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    builder.add_arguments(arg1, arg2)

    assert builder.has_argument("argument1")
    assert builder.has_argument("argument2")


def test_has_argument_from_base_definition(base_format_builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")
    base_format_builder.add_argument(arg1)

    builder = ArgsFormatBuilder(base_format_builder.format)
    builder.add_argument(arg2)

    assert builder.has_argument("argument1")
    assert builder.has_argument("argument2")
    assert builder.has_argument("argument2", False)
    assert not builder.has_argument("argument1", False)


def test_has_argument_at_position(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    builder.add_arguments(arg1, arg2)

    assert builder.has_argument(0)
    assert builder.has_argument(1)


def test_has_argument_at_position_from_base_definition(base_format_builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")
    base_format_builder.add_argument(arg1)

    builder = ArgsFormatBuilder(base_format_builder.format)
    builder.add_argument(arg2)

    assert builder.has_argument(0)
    assert builder.has_argument(1)
    assert not builder.has_argument(1, False)
    assert builder.has_argument(0, False)


def test_has_arguments(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")

    builder.add_arguments(arg1, arg2)

    assert builder.has_arguments()
    assert builder.has_arguments()


def test_has_arguments_with_base_definition(base_format_builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2")
    base_format_builder.add_argument(arg1)

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_arguments()
    assert not builder.has_arguments(False)

    builder.add_argument(arg2)

    assert builder.has_arguments()
    assert builder.has_arguments(False)


def test_has_multi_valued_argument(builder):
    arg1 = Argument("argument1")
    arg2 = Argument("argument2", Argument.MULTI_VALUED)

    builder.add_argument(arg1)

    assert not builder.has_multi_valued_argument()

    builder.add_argument(arg2)

    assert builder.has_multi_valued_argument()


def test_has_multi_valued_argument_with_base_definition(base_format_builder):
    base_format_builder.add_argument(Argument("argument", Argument.MULTI_VALUED))

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_multi_valued_argument()
    assert not builder.has_multi_valued_argument(False)


def test_has_optional_argument(builder):
    arg1 = Argument("argument1", Argument.REQUIRED)
    arg2 = Argument("argument2", Argument.OPTIONAL)

    builder.add_argument(arg1)

    assert not builder.has_optional_argument()

    builder.add_argument(arg2)

    assert builder.has_optional_argument()


def test_has_optional_argument_with_base_definition(base_format_builder):
    base_format_builder.add_argument(Argument("argument", Argument.OPTIONAL))

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_optional_argument()
    assert not builder.has_optional_argument(False)


def test_has_required_argument(builder):
    arg = Argument("argument", Argument.REQUIRED)

    assert not builder.has_required_argument()

    builder.add_argument(arg)

    assert builder.has_required_argument()


def test_has_required_argument_with_base_definition(base_format_builder):
    base_format_builder.add_argument(Argument("argument", Argument.REQUIRED))

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_required_argument()
    assert not builder.has_required_argument(False)


def test_add_option(builder):
    opt = Option("option")

    builder.add_option(opt)

    assert {"option": opt} == builder.get_options()


def test_add_option_preserve_existing_options(builder):
    opt1 = Option("option1")
    opt2 = Option("option2")

    builder.add_option(opt1)
    builder.add_option(opt2)

    assert {"option1": opt1, "option2": opt2} == builder.get_options()


def test_add_option_fails_if_same_long_name(builder):
    builder.add_option(Option("option", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("option", "b"))


def test_add_option_fails_if_same_long_name_as_command_option(builder):
    builder.add_option(CommandOption("option", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("option", "b"))


def test_add_option_fails_if_same_long_name_as_command_option_alias(builder):
    builder.add_command_option(CommandOption("option", "a", ["alias"]))

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("alias", "b"))


def test_add_option_fails_if_same_long_name_in_base_format(base_format_builder):
    base_format_builder.add_option(Option("option", "a"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("option", "b"))


def test_add_option_fails_if_same_long_name_as_command_option_in_base_format(
    base_format_builder,
):
    base_format_builder.add_option(Option("option", "a"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("option", "b"))


def test_add_option_fails_if_same_long_name_as_command_option_alias_in_base_format(
    base_format_builder,
):
    base_format_builder.add_command_option(CommandOption("option", "a", ["alias"]))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("alias", "b"))


def test_add_option_fails_if_same_short_name(builder):
    builder.add_option(Option("option1", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("option2", "a"))


def test_add_option_fails_if_same_short_name_as_command_option(builder):
    builder.add_option(CommandOption("option1", "a"))

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("option1", "a"))


def test_add_option_fails_if_same_short_name_in_base_format(base_format_builder):
    base_format_builder.add_option(Option("option1", "a"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(CannotAddOptionException):
        builder.add_option(Option("option2", "a"))


def test_add_options(builder):
    opt1 = Option("option1")
    opt2 = Option("option2")
    opt3 = Option("option3")

    builder.add_option(opt1)
    builder.add_options(opt2, opt3)

    assert {"option1": opt1, "option2": opt2, "option3": opt3} == builder.get_options()


def test_set_options(builder):
    opt1 = Option("option1")
    opt2 = Option("option2")
    opt3 = Option("option3")

    builder.add_option(opt1)
    builder.set_options(opt2, opt3)

    assert {"option2": opt2, "option3": opt3} == builder.get_options()


def test_get_options(builder):
    opt1 = Option("option1")
    opt2 = Option("option2")

    builder.add_options(opt1, opt2)

    assert {"option1": opt1, "option2": opt2} == builder.get_options()


def test_get_options_with_base_format(base_format_builder):
    opt1 = Option("option1")
    opt2 = Option("option2")

    base_format_builder.add_option(opt1)

    builder = ArgsFormatBuilder(base_format_builder.format)

    builder.add_option(opt2)

    assert {"option1": opt1, "option2": opt2} == builder.get_options()
    assert {"option2": opt2} == builder.get_options(False)


def test_get_option(builder):
    opt = Option("option")

    builder.add_option(opt)

    assert opt == builder.get_option("option")


def test_get_option_from_base_format(base_format_builder):
    opt = Option("option")

    base_format_builder.add_option(opt)

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert opt == builder.get_option("option")


def test_get_option_by_short_name(builder):
    opt = Option("option", "o")

    builder.add_option(opt)

    assert opt == builder.get_option("o")


def test_get_option_by_short_name_from_base_format(base_format_builder):
    opt = Option("option", "o")

    base_format_builder.add_option(opt)

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert opt == builder.get_option("o")


def test_get_option_fails_with_unknown_name(builder):
    with pytest.raises(NoSuchOptionException):
        builder.get_option("foo")


def test_get_option_fails_if_in_base_format_but_include_base_disabled(
    base_format_builder,
):
    base_format_builder.add_option(Option("option"))

    builder = ArgsFormatBuilder(base_format_builder.format)

    with pytest.raises(NoSuchOptionException):
        builder.get_option("option", False)


def test_has_option(builder):
    opt = Option("option")

    builder.add_option(opt)

    assert builder.has_option("option")


def test_has_option_from_base_format(base_format_builder):
    opt = Option("option")

    base_format_builder.add_option(opt)

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_option("option")
    assert not builder.has_option("option", False)


def test_has_option_by_short_name(builder):
    opt = Option("option", "o")

    builder.add_option(opt)

    assert builder.has_option("o")


def test_has_option_by_short_name_from_base_format(base_format_builder):
    opt = Option("option", "o")

    base_format_builder.add_option(opt)

    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_option("o")
    assert not builder.has_option("o", False)


def test_has_options(builder):
    assert not builder.has_options()
    assert not builder.has_options(False)

    builder.add_option(Option("option"))

    assert builder.has_options()
    assert builder.has_options(False)


def test_has_options_with_base_format(base_format_builder):
    base_format_builder.add_option(Option("option"))
    builder = ArgsFormatBuilder(base_format_builder.format)

    assert builder.has_options()
    assert not builder.has_options(False)

    builder.add_option(Option("option2"))

    assert builder.has_options()
    assert builder.has_options(False)
