from minecraft.core import *

Minecraft = Minecraft(
    settings=Settings(
        project_name='example'
    )
)


Commands = Minecraft.Commands
Scoreboard = Minecraft.Scoreboard
Score = Minecraft.Score


@Commands.function
def pow2(a: Score):
    return a*a


@Commands.function
def main():
    for i in range(100):
        Commands.print(f'Hello, my variable is ', pow2(Score(f"{i}", i)), '!')


Minecraft.compile()
