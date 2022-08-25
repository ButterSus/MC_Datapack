from minecraft import Minecraft, Int

Minecraft.init('example', '1.19.2')


@Minecraft.function('setup')
def setup():
    pass


@Minecraft.function('update')
def main():
    A = Int('a', 5)
    A.set(A * 6)


Minecraft.end()
