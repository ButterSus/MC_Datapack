import typing
import warnings
import json
import re
import inspect

from minecraft import constants

if typing.TYPE_CHECKING:
    from core import Minecraft


class Commands:
    """
    This class stores all commands
    """
    framework: 'Minecraft'

    def __init__(self, framework: 'Minecraft'):
        self.framework = framework

    def exec(self, command: str, *, whereToPlace: str = None) -> None:
        """
        Executes command
        """
        if whereToPlace is None:
            self.framework.temporary.function.append(command)
        else:
            self.framework.generated.functions[whereToPlace].append(command)

    def function(self, *attributes: typing.Callable | str) -> typing.Callable:
        """
        Use this decorator to make minecraft function
        """
        if isinstance(attributes[0], typing.Callable):
            function: typing.Callable = attributes[0]

            # Generates function
            fullArgSpec = inspect.getfullargspec(function)
            function(*[self.framework.Score(f'__{constants.argPrefix}{i}', isExternal=True) for i in range(
                len(fullArgSpec.args)
            )])

            # Return handling
            for i in range(len(self.framework.temporary.returning)):
                self.framework.Score(f'__{constants.returnPrefix}{i}', self.framework.temporary.returning[i])

            # Adding stack pop
            for i in range(len(fullArgSpec.args) - 1, -1, -1):
                self.framework.Score(f'__{constants.argPrefix}{i}', isExternal=True).pop()

            # Writing function
            self.framework.generated.functions[function.__name__] = self.framework.temporary.function
            self.framework.temporary.function = []

            # Adding stack push
            for i in range(len(fullArgSpec.args)):
                arg = self.framework.Score(f'__{constants.argPrefix}{i}', isExternal=True)
                arg.push()
                arg.set(self.framework.Score(f'__{constants.tArgPrefix}{i}', isExternal=True))

            self.framework.generated.functions[function.__name__] \
                = self.framework.temporary.function + self.framework.generated.functions[function.__name__]
            self.framework.temporary.function = []

            # Check attributes
            for attribute in attributes[1::]:
                attribute: str = attribute.lower().strip()

                # Load
                if attribute in constants.attributes.load:
                    self.framework.generated.attributes['load'].append(function.__name__)
                    continue

                # Tick
                if attribute in constants.attributes.tick:
                    self.framework.generated.attributes['tick'].append(function.__name__)
                    continue

                warnings.warn(f'Wrong attribute {attribute}')

            _class = self

            class returnClass:
                length: int
                returning = list()

                def __init__(self, length: int):
                    self.length = length
                    for i in range(len(_class.framework.temporary.returning)):
                        self.returning.append(
                            _class.framework.Score(f'__{constants.returnPrefix}{i}', isExternal=True)
                        )

                def function(self, *args):
                    for i in range(self.length):
                        _class.framework.Score(f'__{constants.tArgPrefix}{i}', args[i])
                    _class.exec(f'function {_class.framework.settings.prefix_generated}'
                                f'{_class.framework.settings.project_name}:'
                                f'{function.__name__}')
                    if len(self.returning) == 1:
                        return self.returning[0]
                    if not self.returning:
                        return None
                    return self.returning

            function = returnClass(len(fullArgSpec.args)).function

            self.framework.temporary.returning = []

            return function
        return lambda x: self.function(x, *attributes)

    def print(self, value: str):
        values = list()
        start = 0
        for match in re.finditer(r'\$\{((.*):(.*))}', value):
            end = match.start()
            if value[start:end]:
                values.append(value[start:end])
            values.append(self.framework.Score(name=match.groups()[1],
                                               isExternal=True,
                                               scoreboard=match.groups()[2]))
            start = match.end()
        if value[start:]:
            values.append(value[start:])
        result = list()
        for value in values:
            if isinstance(value, self.framework.Score):
                value: Minecraft.Score
                result.append({"score": {"objective": value.scoreboard.gameName, "name": value.name}})
            if isinstance(value, str):
                value: str
                result.append({"text": value})
        self.exec(f'tellraw @a {json.dumps(result)}')

    def returning(self, *args):
        """
        - To not to break basic principles of return statements, make sure that you are not changing return value.
        """
        self.framework.temporary.returning = list(args)
