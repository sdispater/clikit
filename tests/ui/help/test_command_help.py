from __future__ import unicode_literals

from clikit import ConsoleApplication
from clikit.api.args.format import Argument
from clikit.api.args.format import Option
from clikit.api.config import ApplicationConfig
from clikit.ui.help import CommandHelp


nbsp = "\u00A0"


def test_render(io):
    config = ApplicationConfig()
    config.set_name("test-bin")
    config.add_argument("global-argument", 0, 'Description of "global-argument"')
    config.add_option("global-option", None, 0, 'Description of "global-option"')

    with config.command("command") as c:
        c.set_description('Description of "command"')
        c.set_help(
            'Help of "command {command_name} of {script_name}"\n\nSecond paragraph'
        )
        c.add_alias("command-alias")
        c.add_argument("argument", 0, 'Description of "argument"')
        c.add_option("option", None, 0, 'Description of "option"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command [--option] [<global-argument>] [<argument>]

  aliases: command-alias

ARGUMENTS
  <global-argument>  Description of "global-argument"
  <argument>         Description of "argument"

OPTIONS
  --option           Description of "option"

GLOBAL OPTIONS
  --global-option    Description of "global-option"

DESCRIPTION
  Help of "command command of test-bin"
  
  Second paragraph

"""

    assert expected == io.fetch_output()


def test_render_required_argument(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.add_argument("argument", Argument.REQUIRED, 'Description of "argument"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command <argument>

ARGUMENTS
  <argument>  Description of "argument"

"""

    assert expected == io.fetch_output()


def test_render_option_with_optional_value(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.add_option("option", None, Option.OPTIONAL_VALUE, 'Description of "option"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command [--option{}[<...>]]

OPTIONS
  --option  Description of "option"

""".format(
        nbsp
    )

    assert expected == io.fetch_output()


def test_render_option_with_optional_value_short_name_preferred(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.add_option("option", "o", Option.OPTIONAL_VALUE, 'Description of "option"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command [-o{}[<...>]]

OPTIONS
  -o (--option)  Description of "option"

""".format(
        nbsp
    )

    assert expected == io.fetch_output()


def test_render_option_with_optional_value_long_name_preferred(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.add_option(
            "option",
            "o",
            Option.OPTIONAL_VALUE | Option.PREFER_LONG_NAME,
            'Description of "option"',
        )

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command [--option{}[<...>]]

OPTIONS
  --option (-o)  Description of "option"

""".format(
        nbsp
    )

    assert expected == io.fetch_output()


def test_render_option_with_required_value(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.add_option("option", None, Option.REQUIRED_VALUE, 'Description of "option"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command [--option{}<...>]

OPTIONS
  --option  Description of "option"

""".format(
        nbsp
    )

    assert expected == io.fetch_output()


def test_render_option_with_default_value(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.add_option(
            "option", None, Option.OPTIONAL_VALUE, 'Description of "option"', "Default"
        )

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command [--option{}[<...>]]

OPTIONS
  --option  Description of "option" (default: "Default")

""".format(
        nbsp
    )

    assert expected == io.fetch_output()


def test_render_option_with_named_value(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.add_option(
            "option",
            None,
            Option.OPTIONAL_VALUE,
            'Description of "option"',
            value_name="value",
        )

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
  test-bin command [--option{}[<value>]]

OPTIONS
  --option  Description of "option"

""".format(
        nbsp
    )

    assert expected == io.fetch_output()


def test_render_command_with_sub_commands(io):
    config = ApplicationConfig()
    config.set_name("test-bin")
    config.add_option(
        "global-option", "g", description='Description of "global-option"'
    )

    with config.command("command") as c:
        c.add_argument("argument", 0, 'Description of "argument"')
        c.add_option("option", None, 0, 'Description of "option"')

        with c.sub_command("add") as sc1:
            sc1.set_description('Description of "add"')
            sc1.add_argument("sub-argument1", 0, 'Description of "sub-argument1"')
            sc1.add_argument("sub-argument2", 0, 'Description of "sub-argument2"')
            sc1.add_option("sub-option1", "o", 0, 'Description of "sub-option1"')
            sc1.add_option("sub-option2", None, 0, 'Description of "sub-option2"')

        with c.sub_command("delete") as sc2:
            sc2.set_description('Description of "delete"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
      test-bin command [--option] [<argument>]
  or: test-bin command add [-o] [--sub-option2] [<argument>] [<sub-argument1>]
                           [<sub-argument2>]
  or: test-bin command delete [<argument>]

ARGUMENTS
  <argument>            Description of "argument"

COMMANDS
  add
    Description of "add"

    <sub-argument1>     Description of "sub-argument1"
    <sub-argument2>     Description of "sub-argument2"

    -o (--sub-option1)  Description of "sub-option1"
    --sub-option2       Description of "sub-option2"

  delete
    Description of "delete"

OPTIONS
  --option              Description of "option"

GLOBAL OPTIONS
  -g (--global-option)  Description of "global-option"

"""

    assert expected == io.fetch_output()


def test_sort_sub_commands(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        c.create_sub_command("sub3")
        c.create_sub_command("sub1")
        c.create_sub_command("sub2")

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
      test-bin command
  or: test-bin command sub3
  or: test-bin command sub1
  or: test-bin command sub2

COMMANDS
  sub1

  sub2

  sub3

"""

    assert expected == io.fetch_output()


def test_render_command_with_default_sub_command(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        with c.sub_command("add") as sc1:
            sc1.default()
            sc1.set_description('Description of "add"')
            sc1.add_argument("argument", 0, 'Description of "argument"')

        with c.sub_command("delete") as sc2:
            sc2.set_description('Description of "delete"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
      test-bin command [add] [<argument>]
  or: test-bin command delete

COMMANDS
  add
    Description of "add"

    <argument>  Description of "argument"

  delete
    Description of "delete"

"""

    assert expected == io.fetch_output()


def test_render_command_with_anonymous_sub_command(io):
    config = ApplicationConfig()
    config.set_name("test-bin")

    with config.command("command") as c:
        with c.sub_command("add") as sc1:
            sc1.anonymous()
            sc1.set_description('Description of "add"')
            sc1.add_argument("argument", 0, 'Description of "argument"')

        with c.sub_command("delete") as sc2:
            sc2.set_description('Description of "delete"')

    app = ConsoleApplication(config)
    help = CommandHelp(app.get_command("command"))
    help.render(io)

    expected = """\
USAGE
      test-bin command [<argument>]
  or: test-bin command delete

COMMANDS
  delete
    Description of "delete"

"""

    assert expected == io.fetch_output()
