from __future__ import annotations
import typing

from minecraft import constants

if typing.TYPE_CHECKING:
    from minecraft.core import Minecraft


_Score = typing.TypeVar('_Score', bound='Score')


class Score:
    framework: Minecraft

    name: str
    scoreboard: Minecraft.Scoreboard

    def __init__(self, name: str, value: int | _Score = 0, scoreboard: str | Minecraft.Scoreboard = None, *,
                 isExternal: bool = False, whereToPlace: str = None, isPushable: bool = True):
        if scoreboard is None:
            scoreboard = self.framework.Scoreboard(
                name=f'{self.framework.settings.project_name}',
                isExternal=True
            )

        if isinstance(scoreboard, str):
            scoreboard = self.framework.Scoreboard(
                name=f'{scoreboard}',
                isExternal=True
            )

        self.name = name
        self.scoreboard = scoreboard

        if isPushable:
            self.framework.temporary.variables.append(self)

        if isExternal:
            return

        if isinstance(value, int):
            self.framework.Commands.exec(
                f'scoreboard players set {self.name} '
                f'{self.scoreboard.gameName} {value}',
                whereToPlace=whereToPlace
            )

        if isinstance(value, self.__class__):
            self.framework.Commands.exec(
                f'scoreboard players operation {self.name} {self.scoreboard.gameName} = '
                f'{value.name} {value.scoreboard.gameName}',
                whereToPlace=whereToPlace
            )

    @staticmethod
    def _getIteratorOne(name: str) -> int:
        try:
            if name.startswith(f'__{constants.tempPrefix}'):
                return int(name[len(constants.tempPrefix) + 2:]) + 1
            return 0
        except ValueError:
            raise RuntimeError('Dummkopf!')

    @staticmethod
    def _getIterator(*names: str) -> int:
        return max([Score._getIteratorOne(name) for name in names])

    def push(self):
        self.framework.Commands.exec(
            f'execute store result storage {self.framework.prefixName} '
            f'__{constants.argPrefix} int 1 run scoreboard players get {self.name} {self.scoreboard.gameName}'
        )

        self.framework.Commands.exec(
            f'data modify storage '
            f'{self.framework.prefixName} __{constants.stackName} append from storage '
            f'{self.framework.prefixName} __{constants.argPrefix}'
        )

    def pop(self):
        self.framework.Commands.exec(
            f'execute store result score {self.name} {self.scoreboard.gameName} run data get storage '
            f'{self.framework.prefixName} __{constants.stackName}[-1]'
        )

        self.framework.Commands.exec(
            f'data remove storage {self.framework.prefixName} __{constants.stackName}[-1]'
        )

    def _newConst(self, value: int) -> _Score:
        if f'__{constants.constPrefix}{value}' in self.framework.generated.scores:
            return Score(f'__{constants.constPrefix}{value}', isExternal=True,
                         whereToPlace=f'__{constants.setupFunctionName}')
        return Score(f'__{constants.constPrefix}{value}', value,
                     whereToPlace=f'__{constants.setupFunctionName}')

    @staticmethod
    def _extendedOperatorTemplate(action: str, operation: str) -> typing.Callable[[int | _Score], _Score]:
        def template(self, value: int | _Score) -> _Score:
            if isinstance(value, int):
                value: int
                self.framework.Commands.exec(
                    f'scoreboard players {action} {self.name} {self.scoreboard.gameName} {value}'
                )
            if isinstance(value, self.__class__):
                value: _Score
                self.framework.Commands.exec(
                    f'scoreboard players operation {self.name} {self.scoreboard.gameName} {operation} '
                    f'{value.name} {value.scoreboard.gameName}'
                )
            return self
        return template

    set = _extendedOperatorTemplate('set', '=')
    _add = _extendedOperatorTemplate('add', '+=')
    _sub = _extendedOperatorTemplate('remove', '-=')

    def __iadd__(self, value: int | _Score) -> _Score:
        return self._add(value)

    def __isub__(self, value: int | _Score) -> _Score:
        return self._sub(value)

    def __add__(self, other: int | _Score) -> _Score:
        name = other.name if isinstance(other, self.__class__) else ''
        iterator = self._getIterator(self.name, name)
        TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
        TMP.__iadd__(other)
        return TMP

    def __sub__(self, other: int | _Score) -> _Score:
        name = other.name if isinstance(other, self.__class__) else ''
        iterator = self._getIterator(self.name, name)
        TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
        TMP.__isub__(other)
        return TMP

    @staticmethod
    def _operatorTemplate(operation: str) -> typing.Callable[[_Score], _Score]:
        def template(self, value: _Score) -> _Score:
            value: _Score
            self.framework.Commands.exec(
                f'scoreboard players operation {self.name} {self.scoreboard.gameName} {operation} '
                f'{value.name} {value.scoreboard.gameName}'
            )
            return self
        return template

    _mul = _operatorTemplate('*=')
    _div = _operatorTemplate('/=')
    _mod = _operatorTemplate('%=')

    def __imul__(self, value: int | _Score) -> _Score:
        if isinstance(value, int):
            return self.__imul__(self._newConst(value))
        return self._mul(value)

    def __itruediv__(self, value: _Score) -> _Score:
        if isinstance(value, int):
            return self.__itruediv__(self._newConst(value))
        return self._div(value)

    def __imod__(self, value: _Score) -> _Score:
        if isinstance(value, int):
            return self.__imod__(self._newConst(value))
        return self._mod(value)

    def __mul__(self, other: int | _Score) -> _Score:
        name = other.name if isinstance(other, self.__class__) else ''
        iterator = self._getIterator(self.name, name)
        if isinstance(other, int):
            other: int
            TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
            TMP.__imul__(self._newConst(other))
            return TMP
        if isinstance(other, self.__class__):
            other: _Score
            TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
            TMP.__imul__(other)
            return TMP

    def __truediv__(self, other: int | _Score) -> _Score:
        name = other.name if isinstance(other, self.__class__) else ''
        iterator = self._getIterator(self.name, name)
        if isinstance(other, int):
            other: int
            TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
            TMP.__itruediv__(self._newConst(other))
            return TMP
        if isinstance(other, self.__class__):
            other: _Score
            TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
            TMP.__itruediv__(other)
            return TMP

    def __mod__(self, other: int | _Score) -> _Score:
        name = other.name if isinstance(other, self.__class__) else ''
        iterator = self._getIterator(self.name, name)
        if isinstance(other, int):
            other: int
            TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
            TMP.__imod__(self._newConst(other))
            return TMP
        if isinstance(other, self.__class__):
            other: _Score
            TMP = Score(f'__{constants.tempPrefix}{iterator}', self)
            TMP.__imod__(other)
            return TMP

    def __str__(self) -> str:
        return f'${{{self.name}:{self.scoreboard.name}}}'

    def __hash__(self) -> int:
        return self.name.__hash__()+self.scoreboard.__hash__()

    def __eq__(self, other: _Score) -> bool:
        return self.__hash__() == other.__hash__()
