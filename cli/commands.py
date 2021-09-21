class Command:
    def __init__(self, **kwargs):
        self.name = kwargs.pop("name", None) or str(self._func.__name__)
        self._func = kwargs.pop("func")

    @classmethod
    def from_function(cls, function):
        return cls(func=function, name=function.__name__)


class CommandGroup(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children = []

    def __iter__(self):
        return iter(self.children)

    def command(self, name: str = None):
        def decorator(func):
            if not name:
                command = Command.from_function(func)
            else:
                command = Command(name=name, func=func)

            if command.name.count(" ") > 0:
                raise RuntimeError("Command names cannot have spaces.")
            self.children.append(command)
            return command

        return decorator

    def get_subcommand(self, name: str):
        for command in self.children:
            if command.name == name:
                return command
