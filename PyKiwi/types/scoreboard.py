"""
Open source project by ButterSss
"""

from __future__ import annotations
import typing

from PyKiwi.enums.scoreboard.criteria import Criteria

if typing.TYPE_CHECKING:
    import PyKiwi as core


class Scoreboard:
    """
    Scoreboard in minecraft
    """
    framework: core.PyKiwi
    task_name: str
    criteria: Criteria

    def __init__(self, task_name: str, criteria: Criteria):
        self.task_name = task_name
        self.criteria = criteria
        print('ok')


def getScoreboard(_framework: core.PyKiwi) -> typing.Type[Scoreboard]:
    class newClass(Scoreboard):
        framework = _framework
    return newClass
