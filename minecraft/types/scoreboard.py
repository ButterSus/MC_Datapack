from __future__ import annotations
import typing
# noinspection PyUnresolvedReferences
import warnings

# noinspection PyUnresolvedReferences
from minecraft import constants

if typing.TYPE_CHECKING:
    from minecraft.core import Minecraft


_Scoreboard = typing.TypeVar('_Scoreboard', bound='Scoreboard')


class Scoreboard:
    framework: Minecraft

    name: str
    gameName: str
    criterion: str

    def __init__(self, name: str, criterion: str = 'dummy', *,
                 isConst: bool = False, isExternal: bool = False):
        self.name = name
        self.gameName = self.framework.settings.prefix_generated + name
        self.criterion = criterion

        if isConst:
            self.framework.generated.scoreboards.add(self)
            return

        if isExternal:
            return

        self.framework.Commands.exec(f'scoreboard objectives add '
                                     f'{self.gameName} {self.criterion}')

    def show(self) -> _Scoreboard:
        self.framework.Commands.exec(
            f'scoreboard objectives setdisplay sidebar '
            f'{self.gameName}'
        )
        return self

    def hide(self) -> _Scoreboard:
        self.framework.Commands.exec(
            f'scoreboard objectives setdisplay sidebar'
        )
        return self

    def __hash__(self) -> int:
        return self.name.__hash__()+self.criterion.__hash__()*10+self.framework.prefixName.__hash__()

    def __eq__(self, other: _Scoreboard) -> bool:
        return self.__hash__() == other.__hash__()
