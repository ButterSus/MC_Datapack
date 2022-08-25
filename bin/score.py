import typing
import warnings

_Score = typing.TypeVar('_Score', bound='Score')
if typing.TYPE_CHECKING:
    from bin.lol import Minecraft


class Score:
    _name: str
    _constantValues: typing.Set[int] = list()

    def __init__(self, name: str, value: int | _Score | None = 0):
        self._name = name
        if value is not None:
            if name.startswith('__'):
                warnings.warn('We don\'t recommend you to use \'__\' construction in variable name,'
                              ' it can make errors', RuntimeWarning)
            if isinstance(value, int):
                value: int
                Minecraft.do(f'scoreboard players set {self._name} {Minecraft._namespace} {value}')
            if isinstance(value, Score):
                value: Score
                Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                             f'= {value._name} {Minecraft._namespace}')

    def set(self, other: int | _Score):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players set {self._name} {Minecraft._namespace} {other}')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'= {other._name} {Minecraft._namespace}')

    def __iadd__(self, other: int | _Score):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players add {self._name} {Minecraft._namespace} {other}')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'+= {other._name} {Minecraft._namespace}')
        return self

    def __add__(self, other: int | _Score):
        iter = 0
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players add __{calculatorPrefix}{iter} {Minecraft._namespace} {other}')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)

        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'+= {other._name} {Minecraft._namespace}')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)

    def __isub__(self, other: int | _Score):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players remove {self._name} {Minecraft._namespace} {other}')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'-= {other._name} {Minecraft._namespace}')
        return self

    def __sub__(self, other: int | _Score):
        iter = 0
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players remove __{calculatorPrefix}{iter} {Minecraft._namespace} {other}')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)

        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'-= {other._name} {Minecraft._namespace}')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)

    def __imul__(self, other: int | _Score):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'*= __{other} {Minecraft._namespace}')
            if other not in self.__class__._constantValues:
                try:
                    Minecraft._functions[Minecraft._specialFunctions["load"]]\
                        .insert(0, f'scoreboard players set __{other} {Minecraft._namespace} {other}')
                except KeyError:
                    raise RuntimeError('To use multiplication operator you need to declare load function')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'*= {other._name} {Minecraft._namespace}')
        return self

    def __mul__(self, other: int | _Score):
        iter = 0
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'*= __{other} {Minecraft._namespace}')
            if other not in self.__class__._constantValues:
                try:
                    Minecraft._functions[Minecraft._specialFunctions["load"]]\
                        .insert(0, f'scoreboard players set __{other} {Minecraft._namespace} {other}')
                except KeyError:
                    raise RuntimeError('To use multiplication operator you need to declare load function')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)

        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'*= {other._name} {Minecraft._namespace}')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)

    def __idiv__(self, other: int | _Score):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'/= __{other} {Minecraft._namespace}')
            if other not in self.__class__._constantValues:
                try:
                    Minecraft._functions[Minecraft._specialFunctions["load"]]\
                        .insert(0, f'scoreboard players set __{other} {Minecraft._namespace} {other}')
                except KeyError:
                    raise RuntimeError('To use division operator you need to declare load function')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'/= {other._name} {Minecraft._namespace}')
        return self

    def __truediv__(self, other: int | _Score):
        iter = 0
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'/= __{other} {Minecraft._namespace}')
            if other not in self.__class__._constantValues:
                try:
                    Minecraft._functions[Minecraft._specialFunctions["load"]]\
                        .insert(0, f'scoreboard players set __{other} {Minecraft._namespace} {other}')
                except KeyError:
                    raise RuntimeError('To use division operator you need to declare load function')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)

        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'= {self._name} {Minecraft._namespace}')
            Minecraft.do(f'scoreboard players operation __{calculatorPrefix}{iter} {Minecraft._namespace} '
                         f'/= {other._name} {Minecraft._namespace}')
            return self.__class__(f'__{calculatorPrefix}{iter}', None)