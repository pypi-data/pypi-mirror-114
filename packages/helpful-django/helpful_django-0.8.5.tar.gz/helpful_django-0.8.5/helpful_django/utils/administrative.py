import logging
from typing import Callable

from . import errors


class AdminCommandLine:
    def __init__(self, argv: list[str]):
        self.argv = argv[1:]
        self.logger = logging.getLogger(__name__)
        self.registered_commands: list[Callable] = [
            self.initialize
        ]

    def initialize(self):
        pass

    def run(self):
        try:
            argv = self.argv[0]
        except IndexError:
            raise errors.NoCommandInputException()

        command_names = [command.__name__ for command in self.registered_commands]
        if argv not in command_names:
            self.logger.error(
                f'Command not found: {argv}\n' + '\n'.join(command_names)
            )
            raise errors.CommandNotFoundException(
                argv,
                command_names
            )
        eval(f'self.{argv}()')
