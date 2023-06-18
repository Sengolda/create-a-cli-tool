import pytest

from cli import CLI, Command
from cli.errors import NameHasSpaces, NoCorountines


@pytest.fixture(scope="session")
def cli():
    return CLI("Test CLI")


def get_output(capfd):
    out, _ = capfd.readouterr()
    return out


def test_get_command(cli):
    @cli.command()
    def hello():
        """Says hi"""
        print("hi")

    command = cli.get_command("hello")
    assert command
    assert command.name == "hello"
    assert command.description == "Says hi"

    command = cli.get_command("hi")
    assert command is None


def test_basic_command_execution(cli, capfd):
    cli.get_command("hello")._func()
    assert "hi\n" == get_output(capfd)


def test_command_from_function():
    def command_with_doc():
        """this has a doc"""
        return

    command = Command.from_function(command_with_doc)
    assert command.description == command_with_doc.__doc__
    assert command.name == command_with_doc.__name__

    def command_without_doc():
        return

    command = Command.from_function(command_without_doc)
    assert command.description is None
    assert command.name == command_without_doc.__name__


def test_groups(cli, capfd):
    @cli.group(name="testgroup")
    def group():
        return

    @group.command()
    def hello():
        print("Hello from the test group!")

    command = group.get_subcommand("hello")
    assert command is not None
    assert command.name == "hello"
    command._func()
    assert "Hello from the test group!" in get_output(capfd)


def test_errors(cli):
    @cli.group(name="testgroupforerrors")
    def group():
        return

    with pytest.raises(NoCorountines):

        @cli.command()
        async def coro():
            return

    with pytest.raises(NameHasSpaces):

        @cli.command(name="hi hi")
        def hi():
            return


def test_aliases(cli):
    @cli.command(aliases=["y"])
    def x():
        print("I have an alias called y!")

    assert len([command for command in cli.commands if command.name in ("x", "y")]) == 2


def test_help(cli, capfd):
    cli.get_command("help")._func()
    out = get_output(capfd)

    assert "help - Shows this message" in out
    assert "x" in out
    assert "hello" in out
    assert "testgroup" in out

    assert "coro" not in out
    assert "hi hi" not in out
