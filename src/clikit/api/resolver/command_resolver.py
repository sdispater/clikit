from typing import TYPE_CHECKING

from clikit.api.args import RawArgs

from .resolved_command import ResolvedCommand


if TYPE_CHECKING:
    from clikit.api.application import Application


class CommandResolver(object):
    """
    Returns the command to execute for the given console arguments.
    """

    def resolve(
        self, args, application
    ):  # type: (RawArgs, Application) -> ResolvedCommand
        raise NotImplementedError()
