import asyncio
import sys
from typing import Any, Callable, List, Optional, Union

from .commands import Command
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
        name: str,
        no_welcome_message: bool = False,
        command_not_found_message: str = "Command not found.",
    ) -> None:
        self.name: str = str(name)
        self.commands: List[Command] = [
            Command(
                name="help",
                func=self.show_help,
                description="Shows this message.",
            )
        ]
        self.no_welcome_message: bool = no_welcome_message
        self.command_not_found_message: str = command_not_found_message

    def command(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        aliases: List[Optional[Command]] = [],
    ) -> Callable[..., Any,]:
        """
        Make a command for your cli.

        Parameters
        -----------
        name: :class:`str`
            The name of the command, Default to the name of your function.
        description: :class:`str`
            The description of the command, Defaults to the function's doc.

        aliases: :class:`List[str]`
            A list of strings that contains the name of the aliases you want.
        """

        def decorator(
            func: Callable[
                ...,
                Any,
            ]
        ) -> Command:
            if asyncio.iscoroutinefunction(func):
                raise NoCorountines("Functions must not be coroutines.")

            if not name:
                cmd: Command = Command.from_function(func)
            else:
                cmd: Command = Command(name=name, func=func, description=description)  # type: ignore

            if cmd.name.count(" ") > 0:
                raise NameHasSpaces("Command cannot have spaces.")

            if cmd in self.commands:
                raise CommandAlreadyExists(f"The command named {cmd.name} already exists.")

            self.commands.append(cmd)
            if aliases:
                for alias in aliases:
                    self.commands.append(
                        Command(
                            name=alias,
                            func=func,
                            description=description,
                        )
                    )
            return cmd

        return decorator

    def group(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        aliases: List[Optional[Group]] = [],
    ) -> Callable[..., Any,]:
        """
        Make a command group for your cli.

        Parameters
        -----------
        name: :class:`str`
            The name of the group, Default to the name of your function.
        description: :class:`str`
            The description of the group, Defaults to the function's doc.

        aliases: :class:`List[str]`
            A list of strings that contains the name of the aliases you want.
        """

        def decorator(
            func: Callable[
                ...,
                Any,
            ]
        ) -> Group:
            if asyncio.iscoroutinefunction(func):
                raise RuntimeError("Functions must not be coroutines.")

            if not name:
                cmd: Group = Group.from_function(func)
            else:
                cmd: Group = Group(name=name, func=func, description=description)  # type: ignore

            if cmd.name.count(" ") > 0:
                raise NameHasSpaces("Command cannot have spaces.")

            if cmd in self.commands:
                raise CommandAlreadyExists(f"The group named {cmd.name} already exists.")

            self.commands.append(cmd)
            if aliases:
                for alias in aliases:
                    self.commands.append(
                        Group(
                            name=alias,
                            func=func,
                            description=description,
                        )
                    )
            return cmd

        return decorator

    def run(
        self,
        interactive: bool = True,
    ) -> None:
        """
        Run your cli.

        Parameters
        -----------
        interactive: :class:`bool`
            Pick if the cli should be interactive or not, if set to false you will do like ``python3 main.py command_name``.
        """

        if interactive:
            if not self.no_welcome_message:
                print("Welcome to " + self.name)

            args: List[str] = input(">>> ").split()
            while args and args[0] not in (
                "exit",
                "quit",
            ):
                cmd = self.get_command(args[0])
                if not cmd:
                    print(self.command_not_found_message)
                    args = input(">>> ").split()

                elif type(cmd) == Command:
                    print(type(cmd))
                    try:
                        cmd._func(*args[1:])
                    except TypeError as e:
                        cmd._func()
                    args: List[str] = input(">>> ").split()  # type: ignore

                elif type(cmd) == Group:
                    for subcmd in cmd.children:  # type: ignore
                        if subcmd.name == args[0]:
                            try:
                                subcmd._func(*args[2:])
                            except TypeError as e:
                                print(e)
                            args: List[str] = input(">>> ").split()  # type: ignore
                        else:
                            try:
                                cmd._func(*args[1:])
                            except TypeError:
                                cmd._func()
                            args: List[str] = input(">>> ").split()  # type: ignore

        else:
            cmd = self.get_command(sys.argv[1])  # type: ignore
            if not cmd:
                print(self.command_not_found_message)
                return

            if type(cmd) == Command:
                try:
                    cmd._func(*sys.argv[2:])
                except TypeError:
                    cmd._func()
            else:
                for subcmd in cmd:  # type: ignore
                    if subcmd.name == sys.argv[2]:
                        try:
                            subcmd._func(*sys.argv[2:])
                        except TypeError:
                            subcmd._func()
                        break
                    else:
                        try:
                            cmd._func(*sys.argv[1:])
                        except TypeError:
                            cmd._func()

    def get_command(self, name: str) -> Union[Group, Command]:  # type: ignore
        for command in self.commands:
            if command.name == name:
                return command  # type: ignore

    def remove_command(
        self,
        name: str,
    ) -> None:
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

    def show_help(
        self,
    ) -> None:
        for cmd in self.commands:
            print(f"{cmd.name} - {cmd.description}")

    def add_shard(
        self,
        shard,
    ):
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
