import typing
import warnings

from minecraft import constants

if typing.TYPE_CHECKING:
    from minecraft.core import Minecraft


_Scoreboard = typing.TypeVar('_Scoreboard', bound='Scoreboard')


class Scoreboard:
    """
    Scoreboard variable
    """
    class Scoreboard:
        framework: 'Minecraft'
        criterion: str
        name: str

        def __init__(self, name: str, criterion: str = 'dummy', isExternal: bool = False, showWarn: bool = True):
            self.criterion = criterion
            self.name = name
            if name.startswith('__') and showWarn:
                warnings.warn('Construction \'__\' in scoreboard name often be used for reserved namespaces')
            self.framework.Commands.exec(f'scoreboard objectives add '
                                         f'{self.framework.settings.prefix_generated}{name} {criterion}')

        def show(self) -> None:
            self.framework.Commands.exec(f'scoreboard objectives setdisplay sidebar '
                                         f'{self.framework.settings.prefix_generated}{self.name}')

        def hide(self) -> None:
            self.framework.Commands.exec(f'scoreboard objectives setdisplay sidebar')

    def __new__(cls, framework: 'Minecraft'):
        cls.Scoreboard.framework = framework
        return cls.Scoreboard


