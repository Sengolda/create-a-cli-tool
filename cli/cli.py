from .commands import Command


class CLI:
    def __init__(
        self,
        name,
        no_welcome_message: bool = False,
        command_not_found_message="Command not found.",
    ):
        self.name = str(name)
        self.commands = []
        self.no_welcome_message = no_welcome_message
        self.command_not_found_message = command_not_found_message

    def command(self, name: str = None):
        def decorator(func):
            if not name:
                cmd = Command.from_function(func)
            else:
                cmd = Command(name=name, func=func)

            if cmd.name.count(" ") > 0:
                raise RuntimeError("Command cannot have spaces.")

            self.commands.append(cmd)
            return cmd

        return decorator

    def run(self):
        if not self.no_welcome_message:
            print("Welcome to " + self.name)

        args = input(">>> ")
        while len(args) > 0 and args not in ("exit", "quit"):
            cmd = self.get_command(args)
            if not cmd:
                print(self.command_not_found_message)
                return

            cmd._func()
            break

    def get_command(self, name: str):
        for command in self.commands:
            if command.name == name:
                return command
