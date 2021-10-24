# Notes for [CLI Shards]

- Shards lets you sort commands in classes.

```py
# Importing ClI Tool Maker
from cli.cli import CLI
# Importing the CLI tool Maker's shards.
from cli.ext import shard

# Naming Your CLI Tool
my_cli = CLI("My Nice CLI tool!")


# Naming your shard.
class MyShard(shard.Shard): # this is required to be a subclass.
    def __init__(self):
        super().__init__(my_cli) # this line is also required.

    @my_cli.command(name="hi") # Creating CLI Command
    def hi():  # NOTE: Do not put `self` here.
        print("Hello World!")


my_cli.add_shard(MyShard()) # Adding the shard to the cli.

my_cli.run() # running the cli.
```
