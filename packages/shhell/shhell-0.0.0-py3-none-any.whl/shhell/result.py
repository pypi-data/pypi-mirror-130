from typing import Generic

from shhell.typehints import CommandT


class ExecutionResult(Generic[CommandT]):
    """
    Dunno how I want result to look like yet. We'll see.
    """

    command: CommandT
