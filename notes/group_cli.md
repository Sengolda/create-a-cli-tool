# Notes for [Group CLI Commands]

- Grouped CLI Commands helps to make better commands by creating sub-commands to the main command

### Code:
```py
# Importing CLI Tool Maker
from cli.cli import CLI

# Naming CLI Tool 
my_cli = CLI("My Nice CLI tool!")

# Syntax To Create CLI Group Commands
@my_cli.group(name="hi")
async def hi():
    print("Hello World!")

# Sub-Command For The Main Group Command
@hi.command(name="you", description="Are you cool?")
def you():
    print("Hi you, yes you are cool!")

# Running CLI
my_cli.run()
```
