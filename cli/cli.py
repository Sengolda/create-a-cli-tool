import inspect
from typing import List, Optional, Union, TypeVar, Callable, Any

from .commands import Command, T
from .commands import CommandGroup as Group

from .errors import *


class CLI:
    """
    The CLI class it self, this will represent your cli.

    Parameters
    -----------
    name: :class:`str`
        The name of your CLI
    no_welcome_message: :class:`bool`
        Choose if you want to display a welcome message or not.
    command_not_found_message: :class:`str`
        Pick whatever error message you want to print out when a command is not found.
    """

    def __init__(
        self,
        name,
        no_welcome_message: bool = False,
        command_not_found_message="Command not found.",
    ):
        self.name = str(name)
        self.commands: List[Command] = [
            Command(name="help", func=self.show_help, description="Shows this message.")
        ]
        self.no_welcome_message = no_welcome_message
        self.command_not_found_message = command_not_found_message

    def command(
        self, name: Optional[str] = None, description: Optional[str] = None
    ) -> Callable[[T], Command]:
        """
        Make a command for your cli.

        Parameters
        -----------
        name: :class:`str`
            The name of the command, Default to the name of your function.
        description: :class:`str`
            The description of the command, Defaults to the function's doc.
        """

        def decorator(func: Callable[..., Any]) -> Command:
            if inspect.iscoroutinefunction(func):
                raise NoCorountines("Functions must not be coroutines.")

            if not name:
                cmd: Command = Command.from_function(func)
            else:
                cmd: Command = Command(name=name, func=func, description=description)  # type: ignore

            if cmd.name.count(" ") > 0:
                raise NameHasSpaces("Command cannot have spaces.")

            if cmd in self.commands:
                raise CommandAlreadyExists(
                    f"The command named {cmd.name} already exists."
                )

            self.commands.append(cmd)
            return cmd

        return decorator  # type: ignore

    def group(
        self, name: Optional[str] = None, description: Optional[str] = None
    ) -> Callable[..., Any]:
        """
        Make a command group for your cli.

        Parameters
        -----------
        name: :class:`str`
            The name of the group, Default to the name of your function.
        description: :class:`str`
            The description of the group, Defaults to the function's doc.
        """

        def decorator(func: Callable[..., Any]) -> Group:
            if inspect.iscoroutinefunction(func):
                raise RuntimeError("Functions must not be coroutines.")

            if not name:
                cmd: Group = Group.from_function(func)
            else:
                cmd: Group = Group(name=name, func=func, description=description)  # type: ignore

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
                for subcmd in cmd:  # pylint: disable=not-an-iterable
                    if subcmd.name == args[1]:
                        subcmd._func()
                        break
                break

    def get_command(self, name: str) -> Union[Group, Command]:  # type: ignore
        for command in self.commands:
            if command.name == name:
                return command  # type: ignore

    def remove_command(self, name: str):
        """
        Remove a command.

        Parameters
        -----------
        name: :class:`str`
            The name of the command that you want to remove.
        """
        for cmd in self.commands:
            if cmd.name == name:
                self.commands.remove(cmd)
                break

    def show_help(self) -> None:
        for cmd in self.commands:
            print(f"{cmd.name} - {cmd.description}")

    def add_shard(self, shard):
        """
        Add a shard to the cli.

        Parameters
        -----------
        shard: :class:`cli.cli.ext.shard.Shard`
            The shard you want to add
        """
        shard = shard
        _shard_cmds = shard._inject()
        for cmd in _shard_cmds:
            self.commands.append(cmd)
