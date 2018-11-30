from clikit.api.args import Args
from clikit.api.command import Command
from clikit.api.io import IO

from clikit.ui.help import ApplicationHelp
from clikit.ui.help import CommandHelp


class HelpTextHandler:
    """
    Displays help as text format.
    """

    def handle(self, args, io, command):  # type: (Args, IO, Command) -> int
        application = command.application

        if args.is_argument_set("command"):
            the_command = application.get_command(args.argument("command"))

            usage = CommandHelp(the_command)
        else:
            usage = ApplicationHelp(application)

        usage.render(io)

        return 0
