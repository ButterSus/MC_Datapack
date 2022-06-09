from instructions import Program
import typing
import pickle


if __name__ == '__main__':
    with open("main.ciwi", "rb") as ciwiFile:
        result: list = pickle.load(ciwiFile)
    Program = Program()
    for cmd in result:
        if isinstance(cmd, typing.Callable):
            cmd(Program)
