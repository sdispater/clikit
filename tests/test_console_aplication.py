from typing import Generator

import pytest

from clikit import ConsoleApplication
from clikit.api.command.exceptions import CannotAddCommandException
from clikit.api.command.exceptions import NoSuchCommandException
from clikit.api.config import ApplicationConfig as BaseApplicationConfig
from clikit.api.config import CommandConfig
from clikit.api.io import IO
from clikit.api.io import Input
from clikit.api.io import Output
from clikit.args import StringArgs
from clikit.handler.callback_handler import CallbackHandler
from clikit.io.input_stream import StringInputStream
from clikit.io.output_stream import BufferedOutputStream
from clikit.resolver import DefaultResolver


class ApplicationConfig(BaseApplicationConfig):
    @property
    def default_command_resolver(self):
        return DefaultResolver()


@pytest.fixture()
def config():  # type: () -> Generator[ApplicationConfig]
    config = ApplicationConfig()
    config.set_catch_exceptions(False)
    config.set_terminate_after_run(False)
    config.set_io_factory(
        lambda app, args, input_stream, output_stream, error_stream: IO(
            Input(input_stream), Output(output_stream), Output(error_stream)
        )
    )

    yield config


def test_create(config):
    config.add_argument("argument")
    config.add_option("option", "o")

    app = ConsoleApplication(config)

    assert config == app.config
    fmt = app.global_args_format
    assert len(fmt.get_arguments()) == 1
    arg = fmt.get_argument("argument")
    assert arg.name == "argument"

    opt = fmt.get_option("option")
    assert opt.long_name == "option"
    assert opt.short_name == "o"


def test_get_commands(config):
    config1 = CommandConfig("command1")
    config2 = CommandConfig("command2")
    config.add_command_config(config1)
    config.add_command_config(config2)

    app = ConsoleApplication(config)

    assert len(app.commands) == 2
    assert app.commands.get("command1").name == config1.name
    assert app.commands.get("command2").name == config2.name


def test_get_commands_excludes_disabled_commands(config):
    enabled = CommandConfig("command1").enable()
    disabled = CommandConfig("command2").disable()
    config.add_command_config(enabled)
    config.add_command_config(disabled)

    app = ConsoleApplication(config)

    assert len(app.commands) == 1
    assert app.commands.get("command1").name == enabled.name


def test_get_command(config):
    config1 = CommandConfig("command1")
    config.add_command_config(config1)

    app = ConsoleApplication(config)

    command = app.get_command("command1")
    assert command.name == config1.name


def test_get_command_fails_if_command_not_found(config):
    app = ConsoleApplication(config)

    with pytest.raises(NoSuchCommandException):
        app.get_command("foobar")


def test_has_command(config):
    config1 = CommandConfig("command1")
    config.add_command_config(config1)

    app = ConsoleApplication(config)

    assert app.has_command(config1.name)


def test_has_commands(config):
    config1 = CommandConfig("command1")
    config.add_command_config(config1)

    app = ConsoleApplication(config)

    assert app.has_commands()


def test_has_no_commands(config):
    app = ConsoleApplication(config)

    assert not app.has_commands()


def test_get_named_commands(config):
    config1 = CommandConfig("command1")
    config2 = CommandConfig("command2")
    config3 = CommandConfig("command3")

    config2.anonymous()
    config3.default()

    config.add_command_config(config1)
    config.add_command_config(config2)
    config.add_command_config(config3)

    app = ConsoleApplication(config)

    assert len(app.named_commands) == 2


def test_has_named_commands(config):
    config1 = CommandConfig("command1")
    config.add_command_config(config1)

    app = ConsoleApplication(config)

    assert app.has_named_commands()


def test_has_no_named_commands(config):
    config1 = CommandConfig("command1")
    config1.anonymous()

    config.add_command_config(config1)

    app = ConsoleApplication(config)

    assert not app.has_named_commands()


def test_get_default_commands(config):
    config1 = CommandConfig("command1")
    config2 = CommandConfig("command2")
    config3 = CommandConfig("command3")

    config2.default()
    config3.default()

    config.add_command_config(config1)
    config.add_command_config(config2)
    config.add_command_config(config3)

    app = ConsoleApplication(config)

    assert len(app.default_commands) == 2


def test_has_no_default_commands(config):
    config1 = CommandConfig("command1")
    config.add_command_config(config1)

    app = ConsoleApplication(config)

    assert not app.has_default_commands()


def test_has_default_commands(config):
    config1 = CommandConfig("command1")
    config1.default()

    config.add_command_config(config1)

    app = ConsoleApplication(config)

    assert app.has_default_commands()


def test_fails_if_no_command_name(config):
    config.add_command_config(CommandConfig())

    with pytest.raises(CannotAddCommandException):
        ConsoleApplication(config)


def test_fails_if_duplicate_command_name(config):
    config.add_command_config(CommandConfig("command"))
    config.add_command_config(CommandConfig("command"))

    with pytest.raises(CannotAddCommandException):
        ConsoleApplication(config)


@pytest.mark.parametrize(
    "arg_string, config_callback",
    [
        # Simple command
        (
            "list",
            lambda config, callback: config.create_command("list").set_handler(
                CallbackHandler(callback)
            ),
        ),
        # Default command
        (
            "",
            lambda config, callback: config.create_command("list")
            .default()
            .set_handler(CallbackHandler(callback)),
        ),
        # Sub command
        (
            "server add",
            lambda config, callback: config.create_command("server")
            .create_sub_command("add")
            .set_handler(CallbackHandler(callback)),
        ),
        # Default sub command
        (
            "server",
            lambda config, callback: config.create_command("server")
            .create_sub_command("add")
            .default()
            .set_handler(CallbackHandler(callback)),
        ),
    ],
)
def test_run_command(config, arg_string, config_callback):
    def callback(_, io):
        io.write(io.read_line())
        io.error(io.read_line())

        return 123

    config_callback(config, callback)

    args = StringArgs(arg_string)
    input = StringInputStream("line1\nline2")
    output = BufferedOutputStream()
    error_output = BufferedOutputStream()

    app = ConsoleApplication(config)

    assert 123 == app.run(args, input, output, error_output)
    assert "line1\n" == output.fetch()
    assert "line2" == error_output.fetch()


def test_run_with_keyboard_interrupt(config):  # type: (ApplicationConfig) -> None
    def callback(_, io):
        raise KeyboardInterrupt()

    config.create_command("interrupted").set_handler(CallbackHandler(callback))
    app = ConsoleApplication(config)

    output = BufferedOutputStream()
    error_output = BufferedOutputStream()

    assert 1 == app.run(
        StringArgs("interrupted"), StringInputStream(""), output, error_output
    )

    assert "" == output.fetch()
    assert "" == error_output.fetch()
