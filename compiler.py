from dataclasses import dataclass
from instructions import Instructions
from inspect import signature
import pickle
import typing
import re

_Compiler = typing.TypeVar('_Compiler', bound='Compiler')


@dataclass
class Word:
    src: str
    text: str
    start: int
    end: int


class Functions:
    keys = {
        "push": Instructions.push
    }
    """
    compile functions
    """
    @classmethod
    def split(cls, src: _Compiler) -> None:
        src.buffer['split'] = []
        for word in re.finditer(r'\S+\s*', src.text):
            src.buffer['split'].append(Word(word.group(), word.group().strip(), word.start(), word.end()))

    @classmethod
    def parse(cls, src: _Compiler) -> None:
        for word in src.buffer['split']:
            word: Word
            if word.text in cls.keys.keys():
                src.result.append(cls.keys[word.text])

    @classmethod
    def arguments(cls, src: _Compiler) -> None:
        pass


class Compiler:
    """
    main
    """
    functions = [Functions.split, Functions.parse]
    buffer = dict()
    result = []
    text: str

    def __init__(self, text: str, functions=None):
        if functions is not None:
            self.functions = functions
        self.text = text
        self.__run__()
        with open("main.ciwi", "wb") as ciwiFile:
            pickle.dump(self.result, ciwiFile, pickle.HIGHEST_PROTOCOL)

    def __run__(self):
        for function in self.functions:
            if isinstance(function, typing.Callable):
                function(self)


if __name__ == '__main__':
    with open("main.kiwi", "r") as file:
        Compiler(file.read())
