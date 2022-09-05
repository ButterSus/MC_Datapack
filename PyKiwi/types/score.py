"""
Open source project by ButterSss
"""

from __future__ import annotations
import typing


if typing.TYPE_CHECKING:
    import PyKiwi as core


class Score:
    """
    Score from scoreboard in minecraft
    """
    framework: core.PyKiwi

    def __init__(self):
        pass


def getScore(_framework: core.PyKiwi) -> typing.Type[Score]:
    class newClass(Score):
        framework = _framework
    return newClass
