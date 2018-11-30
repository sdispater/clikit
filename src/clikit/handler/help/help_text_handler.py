from clikit.api.args import Args
from clikit.api.command import Command
from clikit.api.io import IO

from clikit.ui.help import ApplicationHelp


class HelpTextHandler:
    """
    Displays help as text format.
    """

    def handle(self, args, io, command):  # type: (Args, IO, Command) -> int
        application = command.application

        usage = ApplicationHelp(application)

        usage.render(io)

        return 0
