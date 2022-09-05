from __future__ import annotations
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
    This types stores all commands
    """
    framework: Minecraft

    def __init__(self, framework: Minecraft):
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

            isRecursive = False

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

                if attribute in constants.attributes.recursive:
                    isRecursive = True
                    continue

                warnings.warn(f'Wrong attribute {attribute}')

            if not isRecursive:
                self.framework.temporary.variables = list(filter(
                    lambda x: x.name.startswith(f'__{constants.argPrefix}'),
                    self.framework.temporary.variables
                ))

            # Return handling
            for i in range(len(self.framework.temporary.returning)):
                self.framework.Score(f'__{constants.returnPrefix}{i}', self.framework.temporary.returning[i],
                                     isPushable=False)

            # Adding stack pop
            for score in self.framework.temporary.variables.__reversed__():
                score.pop()

            # Writing function
            self.framework.generated.functions[function.__name__] = self.framework.temporary.function
            self.framework.temporary.function = []

            # Adding stack push
            for score in self.framework.temporary.variables:
                score.push()

            # Adding tArg assignment
            for i in range(len(fullArgSpec.args)):
                self.framework.Score(f'__{constants.argPrefix}{i}', isPushable=False,
                                     value=self.framework.Score(
                                         f'__{constants.tArgPrefix}{i}', isExternal=True, isPushable=False
                                     ))

            self.framework.generated.functions[function.__name__] \
                = self.framework.temporary.function + self.framework.generated.functions[function.__name__]
            self.framework.temporary.function = []

            print(*map(lambda x: x.name, self.framework.temporary.variables))

            self.framework.temporary.variables = list()

            _class = self

            class returnClass:
                length: int
                functionName: str
                returning = list()

                def __init__(self, length: int, functionExemplar: typing.Callable):
                    self.length = length
                    self.functionName = functionExemplar.__name__
                    for i in range(len(_class.framework.temporary.returning)):
                        self.returning.append(
                            _class.framework.Score(f'__{constants.returnPrefix}{i}', isExternal=True, isPushable=False)
                        )

                def function(self, *args):
                    for i in range(self.length):
                        _class.framework.Score(f'__{constants.tArgPrefix}{i}', args[i], isPushable=False)
                    _class.exec(f'function {_class.framework.prefixName}:'
                                f'{self.functionName}')
                    if len(self.returning) == 1:
                        return self.returning[0]
                    if not self.returning:
                        return None
                    return self.returning

            function = returnClass(len(fullArgSpec.args), function).function

            self.framework.temporary.returning = []

            return function
        return lambda x: self.function(x, *attributes)

    def print(self, string: str):
        """
        Value should be string
        To use <Score> you type something like that:
        Commands.print(f'Hello, {<Score>}')
        """
        values = list()
        start = 0
        for match in re.finditer(r'\$\{((.*):(.*))}', string):
            end = match.start()
            if string[start:end]:
                values.append(string[start:end])
            values.append(self.framework.Score(name=match.groups()[1],
                                               isExternal=True, isPushable=False,
                                               scoreboard=match.groups()[2]))
            start = match.end()
        if string[start:]:
            values.append(string[start:])
        result = list()
        for value in values:
            if isinstance(value, self.framework.Score):
                result.append({"score": {"objective": value.scoreboard.gameName, "name": value.name}})
            if isinstance(value, str):
                result.append({"text": value})
        self.exec(f'tellraw @a {json.dumps(result)}')

    def returning(self, *args):
        """
        - Returns link to RETURN register
        """
        self.framework.temporary.returning = list(args)
