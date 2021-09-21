from .commands import Command, CommandGroup as Group
import inspect


class CLI:
    def __init__(
        self,
        name,
        no_welcome_message: bool = False,
        command_not_found_message="Command not found.",
    ):
        self.name = str(name)
        self.commands = [
            Command(name="help", func=self.show_help, description="Shows this message.")
        ]
        self.no_welcome_message = no_welcome_message
        self.command_not_found_message = command_not_found_message

    def command(self, name: str = None, description: str = None):
        def decorator(func):
            if inspect.iscoroutinefunction(func):
                raise RuntimeError("Functions must not be coroutines.")

            if not name:
                cmd = Command.from_function(func)
            else:
                cmd = Command(name=name, func=func, description=description)

            if cmd.name.count(" ") > 0:
                raise RuntimeError("Command cannot have spaces.")

            self.commands.append(cmd)
            return cmd

        return decorator

    def group(self, name: str = None, description: str = None):
        def decorator(func):
            if inspect.iscoroutinefunction(func):
                raise RuntimeError("Functions must not be coroutines.")

            if not name:
                cmd = Group.from_function(func)
            else:
                cmd = Group(name=name, func=func, description=description)
            self.commands.append(cmd)
            return cmd

        return decorator

    def run(self):
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

    def get_command(self, name: str):
        for command in self.commands:
            if command.name == name:
                return command

    def remove_command(self, name: str):
        for cmd in self.commands:
            if cmd.name == name:
                self.commands.remove(cmd)

    def show_help(self):
        for cmd in self.commands:
            print(f"{cmd.name} - {cmd.description}")
