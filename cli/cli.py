import inspect
from typing import List, Optional, Union, TypeVar

from .commands import Command
from .commands import CommandGroup as Group

from .errors import *

T = TypeVar("T")
C = TypeVar("C", bound=Command)
G = TypeVar("G", bound=Group)


class ExtensionNotFound(Exception):
    pass


class CLI:
    """
    The CLI class it self, this will represent your cli.

    :param name: The name of your CLI
    :type name: str
    :param no_welcome_message: Choose if you want to display a welcome message or not.
    :type no_welcome_message: bool
    :param command_not_found_message: Pick whatever error message you want to print out when a command is not found.
    :type command_not_found_message: str
    """

    def __init__(
        self,
        name,
        no_welcome_message: bool = False,
        command_not_found_message="Command not found.",
    ):
        self.name = str(name)
        self.commands: List[C] = [
            Command(name="help", func=self.show_help, description="Shows this message.")
        ]
        self.no_welcome_message = no_welcome_message
        self.command_not_found_message = command_not_found_message

    def command(self, name: Optional[str] = None, description: Optional[str] = None):
        """
        Make a command for your cli.

        :param name: The name of the command, Default to the name of your function.
        :type name: str
        :param description: The description of the command, Defaults to the function's doc.
        :type description: str
        """

        def decorator(func: T) -> T:
            if inspect.iscoroutinefunction(func):
                raise NoCorountines("Functions must not be coroutines.")

            if not name:
                cmd: C = Command.from_function(func)
            else:
                cmd: C = Command(name=name, func=func, description=description)

            if cmd.name.count(" ") > 0:
                raise NameHasSpaces("Command cannot have spaces.")

            if cmd in self.commands:
                raise CommandAlreadyExists(
                    f"The command named {cmd.name} already exists."
                )

            self.commands.append(cmd)
            return cmd

        return decorator

    def group(self, name: Optional[str] = None, description: Optional[str] = None):
        """
        Make a command group for your cli.

        :param name: The name of the group, Default to the name of your function.
        :type name: str
        :param description: The description of the group, Defaults to the function's doc.
        :type description: str
        """

        def decorator(func: T) -> T:
            if inspect.iscoroutinefunction(func):
                raise RuntimeError("Functions must not be coroutines.")

            if not name:
                cmd: G = Group.from_function(func)
            else:
                cmd: G = Group(name=name, func=func, description=description)

            if cmd.name.count(" ") > 0:
                raise NameHasSpaces("Command cannot have spaces.")

            if cmd in self.commands:
                raise CommandAlreadyExists(
                    f"The group named {cmd.name} already exists."
                )

            self.commands.append(cmd)
            return cmd

        return decorator

    def run(self):
        """
        Run your cli.
        """

        if not self.no_welcome_message:
            print("Welcome to " + self.name)

        args = input(">>> ").split()
        while len(args) > 0 and args[0] not in ("exit", "quit"):
            cmd = self.get_command(args[0])
            if not cmd:
                print(self.command_not_found_message)
                return

            elif isinstance(cmd, Command) and len(args) == 1:
                cmd._func()
                break

            elif len(args) == 2:
                for subcmd in cmd:
                    if subcmd.name == args[1]:
                        subcmd._func()
                        break
                break

    def get_command(self, name: str) -> Union[C, G]:
        for command in self.commands:
            if command.name == name:
                return command

    def remove_command(self, name: str):
        """
        Remove a command.

        :param name: The name of the command.
        :type name: str
        """
        for cmd in self.commands:
            if cmd.name == name:
                self.commands.remove(cmd)

    def show_help(self) -> None:
        for cmd in self.commands:
            print(f"{cmd.name} - {cmd.description}")

    def add_shard(self, shard):
        """
        Add a shard to the cli.

        :param shard: The shard class you want to add.
        :type shard: cli.ext.shard.Shard
        """
        shard = shard
        shard._inject()
