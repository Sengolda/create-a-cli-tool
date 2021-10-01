from __future__ import annotations

from typing import List, Union

import inspect

from ..cli import CLI, Command, Group


class Shard:
    """
    A class to sort commands in

    :param cli: Your CLI class.
    :type cli: cli.cli.CLI
    """

    def __init__(self, cli: CLI):
        self.cli: CLI = cli
        self.commands: List[Union[Command, Group]] = []

        self.__shard_cli_commands__ = [
            command
            for _, command in inspect.getmembers(self)
            if isinstance(command, (Command, Group))
        ]

    def _inject(self) -> List[Union[Command, Group]]:  # type: ignore
        self.commands.extend(self.__shard_cli_commands__)
        return self.commands
