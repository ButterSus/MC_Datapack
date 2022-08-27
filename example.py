from minecraft.core import *

Minecraft = Minecraft(
    settings=Minecraft.Settings(
        directory='./',
        description='generated by Butter\'s compiler',
        project_name='untitled',
        prefix_generated=''
    )
)


Commands = Minecraft.Commands
Scoreboard = Minecraft.Scoreboard
Score = Minecraft.Score


@Commands.function('load')
def main():
    Score('a')
    HP = Scoreboard('HP', 'Health')
    HP.hide()


Minecraft.compile()
