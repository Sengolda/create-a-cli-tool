from cli.cli import CLI
from cli.ext import shard

my_cli = CLI("My Nice CLI tool!")


class MyShard(shard.Shard):
    def __init__(self):
        super().__init__(my_cli)

    @my_cli.command(name="hi")
    def hi():  # NOTE: Do not put `self` here.
        print("Hello World!")


my_cli.add_shard(MyShard())

my_cli.run()
