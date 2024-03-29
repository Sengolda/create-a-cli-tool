from __future__ import annotations

from typing import TYPE_CHECKING

from .errors import CommandAlreadyExists

if TYPE_CHECKING:
    from typing import Any, Callable, Iterator, List, Optional, Type, TypeVar

    T = TypeVar("T")
    C = TypeVar(
        "C",
        bound="Command",
    )


__all__ = (
    "Command",
    "CommandGroup",
)


class Command:
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        self.name: str = kwargs.pop(
            "name",
            None,
        ) or str(self._func.__name__)
        self._func: Callable = kwargs.pop("func")
        self.description: Optional[str] = (
            kwargs.pop(
                "description",
                None,
            )
            or self._func.__doc__
        )

    @classmethod
    def from_function(
        cls: Type[C],
        function: Callable[
            ...,
            Any,
        ],
    ) -> C:
        return cls(
            func=function,
            name=function.__name__,
            description=function.__doc__,
        )


class CommandGroup(Command):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.children: List[Command] = []

    def __iter__(
        self,
    ) -> Iterator:
        return iter(self.children)

    def command(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        aliases: List[Optional[Command]] = [],
    ) -> Callable[..., Any,]:
        def decorator(
            func: Callable[
                ...,
                Any,
            ]
        ) -> Command:
            if not name:
                command: Command = Command.from_function(func)
            else:
                command: Command = Command(name=name, func=func, description=description)  # type: ignore

            if command.name.count(" ") > 0:
                raise RuntimeError("Command names cannot have spaces.")

            if command in self.children:
                raise CommandAlreadyExists(f"A command named {command.name} is already in {self.name} group.")

            self.children.append(command)
            if aliases:
                for alias in aliases:
                    self.children.append(
                        Command(
                            name=alias,
                            func=func,
                            description=description,
                        )
                    )
            return command

        return decorator

    def get_subcommand(self, name: str) -> Optional[Command]:  # type: ignore
        for command in self.children:
            if command.name == name:
                return command
