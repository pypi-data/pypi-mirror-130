from typing import Any

from shhell.result import ExecutionResult
from shhell.typehints import CommandT


class Command:
    """
    Remembers executable and given args.
    Allows to execute the command and retrieve the result.
    May be used as an argument value for another shhell command.
    """

    def __init__(self, executable: str, *args: Any, **kwargs: Any) -> None:
        """Just remember given args, we're going to build command when we actually will need to"""
        self.executable = executable
        self.args = args
        self.kwargs = kwargs

    def run(self: CommandT, *args, **kwargs) -> ExecutionResult[CommandT]:
        """Execute command in sync mode and return it's result"""

    async def start(self: CommandT) -> ExecutionResult[CommandT]:
        """Execute command in async mode and return it's result"""

    def __await__(self):
        """Allow to simply await CMD instance"""
        return self.start().__await__()

    def __or__(self, other):
        ...

    def __le__(self, other):
        ...

    ...
