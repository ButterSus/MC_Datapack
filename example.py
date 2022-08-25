from minecraft import Minecraft, Score


Minecraft.init(name='const', version='1.18.2', directory='./')


@Minecraft.function
def factorial(x: Score):
    @Minecraft.condition(x == 1)
    def _():
        Minecraft.returnment(1)
    Minecraft.returnment(factorial(x - 1) * x)


Minecraft.end()
