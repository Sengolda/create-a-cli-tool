from cli.cli import CLI

my_cli = CLI("My Nice CLI tool with no welcome messages!", no_welcome_message=True)


@my_cli.command(name="hi")
def hi():
    print("Hello World!")


my_cli.run()
