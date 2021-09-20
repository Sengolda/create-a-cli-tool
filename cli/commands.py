class Command:
    def __init__(self, **kwargs):
        self.name = kwargs.pop("name", None) or str(self._func.__name__)
        self._func = kwargs.pop("func")

    @classmethod
    def from_function(cls, function):
        return cls(func=function, name=function.__name__)
