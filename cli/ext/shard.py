from __future__ import annotations

import inspect
from ..cli import Command, CLI

class Shard:
    """
    A class to sort commands in
    """
    def __init__(self, cli: CLI):
        self.cli = cli

        self.__shard_cli_commands__ = [
            command for _, command in inspect.getmembers(self)
            if isinstance(command, Command)
        ]
    

    def _inject(self):
        for cmd in (self.__shard_cli_commands__):
            self.cli.commands.append(cmd)