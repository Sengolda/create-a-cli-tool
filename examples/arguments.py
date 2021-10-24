from cli.cli import CLI

my_cli = CLI("My Nice CLI tool!")

@my_cli.command(name="hello")
def e(name):
    print("Hi! {} How are you doing?".format(name))


my_cli.run()
