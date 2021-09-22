# Notes for [Basic CLI Commands]

### Code:
```py
# Importing ClI Tool
from cli.cli import CLI 

# Naming Your CLI Tool
my_cli = CLI("My Nice CLI tool!")

# Creating CLI Command
@my_cli.command(name="hi", description="Say hello!") # Setting Name & Description
def hi(): # Creating Command Function
    print("Hello World!") # Implementing Command Function

# Running CLI
my_cli.run()
```