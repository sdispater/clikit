# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from contextlib import contextmanager

import pytest

from clikit.api.args import Args
from clikit.api.args.format import Argument
from clikit.args.string_args import StringArgs
from clikit.config.default_application_config import DefaultApplicationConfig
from clikit.console_application import ConsoleApplication
from clikit.io.output_stream import BufferedOutputStream


@pytest.fixture()
def app():
    config = DefaultApplicationConfig()
    config.set_catch_exceptions(True)
    config.set_terminate_after_run(False)
    config.set_display_name("The Application")
    config.set_version("1.2.3")

    with config.command("command") as c:
        with c.sub_command("run") as sc:
            sc.set_description('Description of "run"')
            sc.add_argument("args", Argument.MULTI_VALUED, 'Description of "argument"')

    application = ConsoleApplication(config)

    return application


def func_spy():
    def decorator(func):
        def wrapper(*args, **kwargs):
            decorator.called = True
            return func(*args, **kwargs)

        return wrapper

    decorator.called = False
    return decorator


@contextmanager
def help_spy(help_command):
    spy = func_spy()
    original = help_command.config.handler.handle
    try:
        help_command.config.handler.handle = spy(original)
        yield spy
    finally:
        help_command.config.handler.handle = original


@pytest.mark.parametrize(
    "args",
    [
        "command run --help",
        "command run --help --another",
        "command run --help -- whatever",
        "command run -h",
        "command run -h --another",
        "command run -h -- whatever",
    ],
)
def test_help_option(app, args):
    help_command = app.get_command("help")
    with help_spy(help_command) as spy:
        app.run(StringArgs(args))
        assert spy.called, "help command not called"


@pytest.mark.parametrize(
    "args",
    [
        "command run -- whatever --help",
        "command run -- whatever -h",
        "command run -- --help",
    ],
)
def test_help_option_ignored(app, args):
    help_command = app.get_command("help")
    with help_spy(help_command) as spy:
        app.run(StringArgs(args))
        assert not spy.called, "help command called"
