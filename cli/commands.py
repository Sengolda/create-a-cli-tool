from typing import TypeVar, List

T = TypeVar("T")


class Command:
    def __init__(self, **kwargs):
        self.name = kwargs.pop("name", None) or str(self._func.__name__)
        self._func = kwargs.pop("func")
        self.description = kwargs.pop("description", None) or self._func.__doc__

    @classmethod
    def from_function(cls, function):
        return cls(func=function, name=function.__name__, description=function.__doc__)


C = TypeVar("C", bound=Command)


class CommandGroup(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children: List[C] = []

    def __iter__(self):
        return iter(self.children)

    def command(self, name: str = None, description: str = None) -> T:
        def decorator(func):
            if not name:
                command: C = Command.from_function(func)
            else:
                command: C = Command(name=name, func=func, description=description)

            if command.name.count(" ") > 0:
                raise RuntimeError("Command names cannot have spaces.")
            self.children.append(command)
            return command

        return decorator

    def get_subcommand(self, name: str):
        for command in self.children:
            if command.name == name:
                return command
