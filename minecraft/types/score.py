import typing
import warnings

from minecraft import constants

if typing.TYPE_CHECKING:
    from minecraft.core import Minecraft


_Score = typing.TypeVar('_Score', bound='Score')


class Score:
    """
    Scoreboard variable
    """
    class Score:
        framework: 'Minecraft'
        name: str

        def __init__(self, name: str, value: int | _Score = 0, scoreboard: str = None,
                     isExternal: bool = False, showWarn: bool = True):
            if scoreboard is None:
                scoreboard = f'{self.framework.settings.prefix_generated}{self.framework.settings.project_name}'
            self.name = name
            if name.startswith('__') and showWarn:
                warnings.warn('Construction \'__\' in variable name often be used for reserved values')
            if isinstance(value, int):
                self.framework.Commands.exec()
            if isinstance(value, self.__class__):
                pass

    def __new__(cls, framework: 'Minecraft'):
        cls.Score.framework = framework
        return cls.Score


