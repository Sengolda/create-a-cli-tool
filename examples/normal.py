from cli.cli import CLI

my_cli = CLI("My Nice CLI tool!")


@my_cli.command(name="hi", description="Say hello!")
def hi():
    print("Hello World!")


my_cli.run()
