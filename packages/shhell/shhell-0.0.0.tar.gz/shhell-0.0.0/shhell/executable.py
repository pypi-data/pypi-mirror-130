from types import FunctionType
from typing import TypeVar

from shhell.command import Command


T = TypeVar("T")


class Executable:
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, *args, **kwargs) -> Command:
        return Command(self.name, *args, **kwargs)

    @classmethod
    def from_dummy(cls: T, dummy_function: FunctionType) -> T:
        return cls(dummy_function.__name__)
