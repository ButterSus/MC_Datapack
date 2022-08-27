import typing
import warnings
from typing import Type

from minecraft import constants

if typing.TYPE_CHECKING:
    from minecraft.core import Minecraft


class Score:
    framework: 'Minecraft'

    name: str
    scoreboard: str

    def __init__(self, name: str, value: int = 0, scoreboard: str | 'Minecraft.Scoreboard' = None,
                 isExternal: bool = False, showWarn: bool = True):

        if scoreboard is None:
            scoreboard = f'{self.framework.settings.prefix_generated}{self.framework.settings.project_name}'

        if isinstance(scoreboard, self.framework.Scoreboard.__class__):
            scoreboard: 'Minecraft.Scoreboard'
            scoreboard = scoreboard.name

        self.name = name
        self.scoreboard = scoreboard
        if name.startswith('__') and showWarn:
            warnings.warn(
                'Construction \'__\' in variable name often be used for reserved values'
            )
        if isinstance(value, int):
            self.framework.Commands.exec(
                f'scoreboard players set '
            )
        if isinstance(value, self.__class__):
            print('self')


def _Score(_framework: 'Minecraft'):
    class newClass(Score):
        framework = _framework
    return newClass
