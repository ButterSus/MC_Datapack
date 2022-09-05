"""
Open source project by ButterSss
"""

from __future__ import annotations
import typing


if typing.TYPE_CHECKING:
    import PyKiwi as core


def main(self: core.PyKiwi, command: str):
    """
    Executes command
    """
    print(command)
