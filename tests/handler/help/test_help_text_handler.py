# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from clikit.api.args import Args
from clikit.args.string_args import StringArgs
from clikit.config.default_application_config import DefaultApplicationConfig
from clikit.console_application import ConsoleApplication


@pytest.fixture()
def app():
    config = DefaultApplicationConfig()
    config.set_display_name("The Application")
    config.set_version("1.2.3")

    with config.command("command") as c:
        with c.sub_command("add") as sc1:
            sc1.set_description('Description of "add"')
            sc1.add_argument("argument", 0, 'Description of "argument"')

        with c.sub_command("delete") as sc2:
            sc2.set_description('Description of "delete"')
            sc2.add_option("opt", "o", description='Description of "opt"')
            sc2.add_argument("sub-arg", description='Description of "sub-arg"')

    application = ConsoleApplication(config)

    return application


def test_render_for_application(app, io):
    help_command = app.get_command("help")
    handler = help_command.config.handler

    raw_args = StringArgs("")
    args = Args(help_command.args_format, raw_args)
    status = handler.handle(args, io, app.get_command("command"))

    expected = """\
The Application version 1.2.3

USAGE
  console [-h] [-q] [-v [<...>]] [-V] [--ansi] [--no-ansi] [-n] <command>
          [<arg1>] ... [<argN>]

ARGUMENTS
  <command>              The command to execute
  <arg>                  The arguments of the command

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal
                         output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

AVAILABLE COMMANDS
  command
  help                   Display the manual of a command

"""

    assert 0 == status
    assert expected == io.fetch_output()


def test_render_for_application_does_not_display_hidden_commands(app, io):
    app.get_command("command").config.hide()

    help_command = app.get_command("help")
    handler = help_command.config.handler

    raw_args = StringArgs("")
    args = Args(help_command.args_format, raw_args)
    status = handler.handle(args, io, app.get_command("command"))

    expected = """\
The Application version 1.2.3

USAGE
  console [-h] [-q] [-v [<...>]] [-V] [--ansi] [--no-ansi] [-n] <command>
          [<arg1>] ... [<argN>]

ARGUMENTS
  <command>              The command to execute
  <arg>                  The arguments of the command

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal
                         output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

AVAILABLE COMMANDS
  help                   Display the manual of a command

"""

    assert 0 == status
    assert expected == io.fetch_output()


def test_render_sub_command(app, io):
    help_command = app.get_command("help")
    handler = help_command.config.handler

    raw_args = StringArgs("command delete")
    args = Args(help_command.args_format, raw_args)
    args.set_argument("command", "command")
    status = handler.handle(args, io, app.get_command("command"))

    expected = """\
USAGE
  console command delete [-o] [<sub-arg>]

ARGUMENTS
  <sub-arg>              Description of "sub-arg"

OPTIONS
  -o (--opt)             Description of "opt"

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal
                         output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

"""

    assert 0 == status
    assert expected == io.fetch_output()


def test_render_parent_command_with_help_command_argument(app, io):
    help_command = app.get_command("help")
    handler = help_command.config.handler

    raw_args = StringArgs("help command")
    args = Args(help_command.args_format, raw_args)
    args.set_argument("command", "command")
    status = handler.handle(args, io, app.get_command("command"))

    expected = """\
USAGE
      console command
  or: console command add [<argument>]
  or: console command delete [-o] [<sub-arg>]

COMMANDS
  add
    Description of "add"

    <argument>           Description of "argument"

  delete
    Description of "delete"

    <sub-arg>            Description of "sub-arg"

    -o (--opt)           Description of "opt"

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal
                         output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

"""

    assert 0 == status
    assert expected == io.fetch_output()


def test_render_sub_command_with_help_command_argument(app, io):
    help_command = app.get_command("help")
    handler = help_command.config.handler

    raw_args = StringArgs("help command delete")
    args = Args(help_command.args_format, raw_args)
    args.set_argument("command", "command")
    status = handler.handle(args, io, app.get_command("command"))

    expected = """\
USAGE
  console command delete [-o] [<sub-arg>]

ARGUMENTS
  <sub-arg>              Description of "sub-arg"

OPTIONS
  -o (--opt)             Description of "opt"

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal
                         output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

"""

    assert 0 == status
    assert expected == io.fetch_output()


def test_render_parent_command_does_not_display_hidden_sub_commands(app, io):
    app.get_command("command").config.get_sub_command_config("delete").hide()

    help_command = app.get_command("help")
    handler = help_command.config.handler

    raw_args = StringArgs("help command")
    args = Args(help_command.args_format, raw_args)
    args.set_argument("command", "command")
    status = handler.handle(args, io, app.get_command("command"))

    expected = """\
USAGE
      console command
  or: console command add [<argument>]

COMMANDS
  add
    Description of "add"

    <argument>           Description of "argument"

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal
                         output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

"""

    assert 0 == status
    assert expected == io.fetch_output()
