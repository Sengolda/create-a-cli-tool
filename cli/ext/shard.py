from __future__ import annotations

import inspect

from ..cli import CLI, Command


class Shard:
    """
    A class to sort commands in

    :param cli: Your CLI class.
    :type cli: cli.cli.CLI
    """

    def __init__(self, cli: CLI):
        self.cli = cli

        self.__shard_cli_commands__ = [
            command
            for _, command in inspect.getmembers(self)
            if isinstance(command, Command)
        ]

    def _inject(self):
        for cmd in self.__shard_cli_commands__:
            self.cli.commands.append(cmd)
