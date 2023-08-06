r"""
This is POC!

Just without P and O \o/
"""
from .executable import Executable


def __getattr__(name) -> Executable:
    return Executable(name)
