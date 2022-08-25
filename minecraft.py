import os
import typing
import shutil
import json
import warnings

calculatorPrefix = 'TMP'


_Minecraft = typing.TypeVar('_Minecraft', bound='Minecraft')


class Minecraft:
    _description: str
    _pack_format: int
    _namespace: str
    _specialFunctions: typing.Dict[str, str] = dict()
    _functions: typing.Dict[str, typing.List[str]] = dict()
    _generatedFunction: typing.List[str] = list()

    @classmethod
    def init(cls, name: str, version: str = '1.19.2', description=""):
        version = list(map(int, version.split('.')))
        version = [version[i] if i < len(version) else 0 for i in range(3)]
        match version:
            case[1, 13, x] if 2 >= x >= 0:
                cls._pack_format = 4
            case[1, 14, x] if 4 >= x >= 0:
                cls._pack_format = 4
            case[1, 15, x] if 2 >= x >= 0:
                cls._pack_format = 5
            case[1, 16, x] if 1 >= x >= 0:
                cls._pack_format = 5
            case[1, 16, x] if 5 >= x >= 2:
                cls._pack_format = 6
            case[1, 17, x] if 1 >= x >= 0:
                cls._pack_format = 7
            case[1, 18, x] if 1 >= x >= 0:
                cls._pack_format = 8
            case [1, 18, 2]:
                cls._pack_format = 9
            case [1, 19, x] if 2 >= x >= 0:
                cls._pack_format = 10
            case _:
                raise RuntimeError(f'Wrong version of Minecraft: {".".join(list(map(str, version)))}')
        cls._description = description
        cls._namespace = name
        if os.path.exists(cls._namespace):
            shutil.rmtree(cls._namespace)
        os.mkdir(cls._namespace)
        os.chdir(cls._namespace)
        os.mkdir('data')
        os.mkdir(f'data/{cls._namespace}')
        os.mkdir(f'data/{cls._namespace}/functions')
        os.mkdir(f'data/minecraft')
        os.mkdir(f'data/minecraft/tags')
        os.mkdir(f'data/minecraft/tags/functions')

    @classmethod
    def end(cls) -> None:
        with open('pack.mcmeta', 'w') as file:
            file.write(json.dumps({"pack": {
                "pack_format": cls._pack_format,
                "description": cls._description
            }}))
        for name, function in cls._functions.items():
            name: str
            function: typing.List[str]
            with open(f'data/{cls._namespace}/functions/{name}.mcfunction', 'w') as file:
                file.write('\n'.join(function))

    @classmethod
    def function(cls, *f: typing.Any) -> typing.Any:
        if isinstance(f[0], typing.Callable):
            args: typing.List[str] = list(f[1:])
            f: typing.Callable = f[0]
            f()
            cls._functions[f.__name__] = cls._generatedFunction
            cls._generatedFunction = []
            for arg in args:
                match arg.lower().strip():
                    case "tick" | "update" | "loop":
                        if "tick" in cls._specialFunctions.keys():
                            raise RuntimeError(f'You already have tick function with name '
                                               f'{cls._specialFunctions["tick"]}')
                        with open('data/minecraft/tags/functions/tick.json', 'w') as file:
                            file.write(json.dumps({
                                "replace": False,
                                "values": [f'{cls._namespace}:{f.__name__}']
                            }))
                        cls._specialFunctions["tick"] = f.__name__
                    case "load" | "setup" | "main":
                        if "load" in cls._specialFunctions.keys():
                            raise RuntimeError(f'You already have load function with name '
                                               f'{cls._specialFunctions["load"]}')
                        with open('data/minecraft/tags/functions/load.json', 'w') as file:
                            file.write(json.dumps({
                                "replace": False,
                                "values": [f'{cls._namespace}:{f.__name__}']
                            }))
                        cls._specialFunctions["load"] = f.__name__
            return lambda: cls.do(f'function {cls._namespace}:{f.__name__}')
        return lambda x: cls.function(x, *f)

    @classmethod
    def do(cls, command: str) -> None:
        cls._generatedFunction.append(command)

    @classmethod
    def print(cls, *value: typing.List[typing.Any]) -> None:
        cls.do(f'say {value[0]}')


_Int = typing.TypeVar('_Int', bound='Int')


class Int:
    _name: str
    _constantValues: typing.Set[int] = list()

    def __init__(self, name: str, value: int | None = 0):
        self._name = name
        if value is not None:
            if name.startswith('__'):
                warnings.warn('We don\'t recommend you to use \'__\' construction in variable name,'
                              ' it can make errors', RuntimeWarning)
            Minecraft.do(f'scoreboard players set {self._name} {Minecraft._namespace} {value}')

    def set(self, other: int | _Int):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players set {self._name} {Minecraft._namespace} {other}')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'= {other._name} {Minecraft._namespace}')

    def __iadd__(self, other: int | _Int):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players add {self._name} {Minecraft._namespace} {other}')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'+= {other._name} {Minecraft._namespace}')

    def __add__(self, other: int | _Int):
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

    def __isub__(self, other: int | _Int):
        if isinstance(other, int):
            Minecraft.do(f'scoreboard players remove {self._name} {Minecraft._namespace} {other}')
        if isinstance(other, self.__class__):
            Minecraft.do(f'scoreboard players operation {self._name} {Minecraft._namespace} '
                         f'-= {other._name} {Minecraft._namespace}')

    def __sub__(self, other: int | _Int):
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

    def __imul__(self, other: int | _Int):
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

    def __mul__(self, other: int | _Int):
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

    def __idiv__(self, other: int | _Int):
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

    def __mul__(self, other: int | _Int):
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