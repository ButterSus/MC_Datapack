import typing
import warnings

from minecraft import constants

if typing.TYPE_CHECKING:
    from minecraft.core import Minecraft


_Scoreboard = typing.TypeVar('_Scoreboard', bound='Scoreboard')


class Scoreboard:
    framework: 'Minecraft'

    name: str
    criterion: str

    def __init__(self, name: str, criterion: str = 'dummy', isExternal: bool = False, showWarn: bool = True):
        self.criterion = criterion
        self.name = name
        if name.startswith('__') and showWarn:
            warnings.warn('Construction \'__\' in scoreboard name often be used for reserved namespaces')

        if not isExternal:
            self.framework.Commands.exec(f'scoreboard objectives add '
                                         f'{self.framework.settings.prefix_generated}{name} {criterion}')

    def show(self) -> _Scoreboard:
        self.framework.Commands.exec(
            f'scoreboard objectives setdisplay sidebar '
            f'{self.framework.settings.prefix_generated}{self.name}'
        )
        return self

    def hide(self) -> _Scoreboard:
        self.framework.Commands.exec(
            f'scoreboard objectives setdisplay sidebar'
        )
        return self


def getScoreboard(_framework: 'Minecraft'):
    class newClass(Scoreboard):
        framework = _framework
    return newClass
