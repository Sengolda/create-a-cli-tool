class CommandAlreadyExists(BaseException):
    """Raised when multiple commands have the same name."""


class NameHasSpaces(BaseException):
    """Raised when a command name has spaces."""


class NoCorountines(BaseException):
    """Raised when a function is a coruntine."""
