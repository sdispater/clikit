import sys

import pytest

from clikit.args import ArgvArgs


@pytest.fixture()
def argv():
    original_argv = sys.argv

    yield

    sys.argv = original_argv


def test_create(argv):
    sys.argv = ("console", "server", "add", "--port", "80", "localhost")
    args = ArgvArgs()

    assert args.script_name == "console"
    assert ["server", "add", "--port", "80", "localhost"] == args.tokens


def test_create_with_custom_tokens(argv):
    sys.argv = ("console", "server", "add", "localhost")
    args = ArgvArgs(["console", "server", "add", "--port", "80", "localhost"])

    assert args.script_name == "console"
    assert ["server", "add", "--port", "80", "localhost"] == args.tokens


def test_has_token():
    args = ArgvArgs(["console", "server", "add", "--port", "80", "localhost"])

    assert args.has_token("server")
    assert args.has_token("add")
    assert args.has_token("--port")
    assert args.has_token("80")
    assert args.has_token("localhost")
    assert not args.has_token("console")
    assert not args.has_token("foo")


def test_has_option_token():
    args = ArgvArgs(
        [
            "console",
            "server",
            "add",
            "--port",
            "80",
            "localhost",
            "--",
            "-h",
            "--test",
            "remainder",
        ]
    )

    assert args.has_option_token("server")
    assert args.has_option_token("add")
    assert args.has_option_token("--port")
    assert args.has_option_token("80")
    assert args.has_option_token("localhost")
    assert not args.has_option_token("console")
    assert not args.has_option_token("-h")
    assert not args.has_option_token("--test")
    assert not args.has_option_token("remainder")


def test_to_string():
    args = ArgvArgs(["console", "server", "add", "--port", "80", "localhost"])

    assert "console server add --port 80 localhost" == args.to_string()
    assert "console server add --port 80 localhost" == args.to_string(True)
    assert "server add --port 80 localhost" == args.to_string(False)
