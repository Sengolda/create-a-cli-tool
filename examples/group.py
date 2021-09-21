from cli.cli import CLI

my_cli = CLI("My Nice CLI tool!")


@my_cli.group(name="hi")
async def hi():
    print("Hello World!")


@hi.command(name="you", description="Are you cool?")
def you():
    print("Hi you, yes you are cool!")


my_cli.run()
