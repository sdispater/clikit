from clikit.api.command import Command
from clikit.api.command import CommandCollection
from clikit.api.config.command_config import CommandConfig
from clikit.utils.command import find_similar_command_names


def test_find_similar_command_names():
    foobar_config = CommandConfig("foobar")
    bar_config = CommandConfig("bar")
    barfoo_config = CommandConfig("barfoo")
    fooo_config = CommandConfig("fooo")
    names = find_similar_command_names(
        "foo",
        CommandCollection(
            [
                Command(foobar_config),
                Command(bar_config),
                Command(barfoo_config),
                Command(fooo_config),
            ]
        ),
    )

    assert ["fooo", "foobar", "barfoo"] == names
