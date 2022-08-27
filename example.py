from minecraft.core import *

Minecraft = Minecraft(
    settings=Settings(
        prefix_generated='hell_'
    )
)


Commands = Minecraft.Commands
Scoreboard = Minecraft.Scoreboard
Score = Minecraft.Score


@Commands.function
def pow2(a: Score):
    Commands.returning(a*a)


@Commands.function('load')
def main():
    Commands.print(f'{pow2(Score("A", 5))}')
    pass


Minecraft.compile()
