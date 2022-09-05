"""
Open source project by ButterSss
"""

from __future__ import annotations
from multipledispatch import dispatch
import typing

import PyKiwi.commands.execute


if typing.TYPE_CHECKING:
    import PyKiwi as core


class Minecraft:
    """
    Contains all minecraft types and functions
    """
    framework: core.PyKiwi

    def __init__(self, framework: core.PyKiwi):
        self.framework = framework

    def function(self, *args: typing.Callable | str):
        return lambda x: self.function(x, *args)

    execute = PyKiwi.commands.execute.main
