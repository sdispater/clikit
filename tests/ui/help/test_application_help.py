from clikit import ConsoleApplication
from clikit.api.args import Args
from clikit.api.args.format import ArgsFormat
from clikit.api.args.format import Option
from clikit.api.config import ApplicationConfig
from clikit.args import ArgvArgs
from clikit.ui.help import ApplicationHelp


def test_render(io):
    config = ApplicationConfig("test-bin")
    config.set_display_name("The Application")
    config.add_argument(
        "global-argument", description='Description of "global-argument"'
    )
    config.add_option("global-option", description='Description of "global-option"')

    with config.command("command1") as c:
        c.set_description('Description of "command1"')

    with config.command("command2") as c:
        c.set_description('Description of "command2"')

    with config.command("longer-command3") as c:
        c.set_description('Description of "longer-command3"')

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
The Application

USAGE
  test-bin [--global-option] <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>        The command to execute
  <arg>            The arguments of the command

GLOBAL OPTIONS
  --global-option  Description of "global-option"

AVAILABLE COMMANDS
  command1         Description of "command1"
  command2         Description of "command2"
  longer-command3  Description of "longer-command3"

"""

    assert expected == io.fetch_output()


def test_sort_commands(io):
    config = ApplicationConfig("test-bin")
    config.set_display_name("The Application")
    config.create_command("command3")
    config.create_command("command1")
    config.create_command("command2")

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
The Application

USAGE
  test-bin <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>  The command to execute
  <arg>      The arguments of the command

AVAILABLE COMMANDS
  command1
  command2
  command3

"""

    assert expected == io.fetch_output()


def test_render_version(io):
    config = ApplicationConfig("test-bin", "1.2.3")
    config.set_display_name("The Application")

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
The Application version 1.2.3

USAGE
  test-bin <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>  The command to execute
  <arg>      The arguments of the command

"""

    assert expected == io.fetch_output()


def test_render_default_display_name(io):
    config = ApplicationConfig("test-bin")

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
Test Bin

USAGE
  test-bin <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>  The command to execute
  <arg>      The arguments of the command

"""

    assert expected == io.fetch_output()


def test_render_default_no_name(io):
    config = ApplicationConfig()

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
Console Tool

USAGE
  console <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>  The command to execute
  <arg>      The arguments of the command

"""

    assert expected == io.fetch_output()


def test_render_global_options_with_preferred_short_name(io):
    config = ApplicationConfig()
    config.add_option(
        "global-option", "g", Option.PREFER_SHORT_NAME, 'Description of "global-option"'
    )

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
Console Tool

USAGE
  console [-g] <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>             The command to execute
  <arg>                 The arguments of the command

GLOBAL OPTIONS
  -g (--global-option)  Description of "global-option"

"""

    assert expected == io.fetch_output()


def test_render_global_options_with_preferred_long_name(io):
    config = ApplicationConfig()
    config.add_option(
        "global-option", "g", Option.PREFER_LONG_NAME, 'Description of "global-option"'
    )

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
Console Tool

USAGE
  console [--global-option] <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>             The command to execute
  <arg>                 The arguments of the command

GLOBAL OPTIONS
  --global-option (-g)  Description of "global-option"

"""

    assert expected == io.fetch_output()


def test_render_description(io):
    config = ApplicationConfig()
    config.set_help("The help for {script_name}\n\nSecond paragraph")

    app = ConsoleApplication(config)
    help = ApplicationHelp(app)
    help.render(io)

    expected = """\
Console Tool

USAGE
  console <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>  The command to execute
  <arg>      The arguments of the command

DESCRIPTION
  The help for console
  
  Second paragraph

"""

    assert expected == io.fetch_output()
