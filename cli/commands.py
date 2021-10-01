from typing import List, TypeVar, Any, Type, Callable
from .errors import CommandAlreadyExists

T = TypeVar("T")
C = TypeVar("C", bound="Command")


class Command:
    def __init__(self, **kwargs):
        self.name = kwargs.pop("name", None) or str(self._func.__name__)
        self._func = kwargs.pop("func")
        self.description = kwargs.pop("description", None) or self._func.__doc__

    @classmethod
    def from_function(cls, function):
        return cls(func=function, name=function.__name__, description=function.__doc__)


class CommandGroup(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children: List[Command] = []

    def __iter__(self):
        return iter(self.children)

    def command(self, name: str = None, description: str = None):
        def decorator(func: T) -> Command:
            if not name:
                command: Command = Command.from_function(func)
            else:
                command: Command = Command(name=name, func=func, description=description)  # type: ignore

            if command.name.count(" ") > 0:
                raise RuntimeError("Command names cannot have spaces.")

            if command in self.children:
                raise CommandAlreadyExists(
                    f"A command named {command.name} is already in {self.name} group."
                )

            self.children.append(command)
            return command

        return decorator

    def get_subcommand(self, name: str):
        for command in self.children:
            if command.name == name:
                return command
