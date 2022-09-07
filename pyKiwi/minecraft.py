"""
Open source project by ButterSss
"""

from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    import pyKiwi.core as core

from pyKiwi.commands.run import main as command_run


class Minecraft:
    """
    Contains all minecraft types and functions
    """
    framework: core.PyKiwi

    def __init__(self, framework: core.PyKiwi):
        self.framework = framework

    def function(self, *args: str | typing.Callable):
        if args and isinstance(args[0], typing.Callable):
            function: typing.Callable = args[0]
            args: typing.List[str] = list(args[1:])
            function()
            return
        return lambda x: self.function(x, *args)

    run = command_run
