import inspect
from typing import List, Union

from ..cli import CLI, Command, Group


class Shard:
    """
    A class to sort commands in

    Parameters
    -----------
    cli: :class:`cli.cli.CLI`
        Your CLI class.
    """

    def __init__(self, cli: CLI):
        self.cli: CLI = cli
        self.commands: List[Union[Command, Group]] = []

        self.__shard_cli_commands__: List[Union[Command, Group]] = [
            command for _, command in inspect.getmembers(self) if isinstance(command, (Command, Group))
        ]

    def _inject(self) -> List[Union[Command, Group]]:  # type: ignore
        self.commands.extend(self.__shard_cli_commands__)
        return self.commands
