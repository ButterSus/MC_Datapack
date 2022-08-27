import typing
import warnings

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

    def exec(self, command: str) -> None:
        """
        Executes command
        """
        self.framework.temporary.function.append(command)

    def function(self, *attributes: typing.Callable | str) -> typing.Callable:
        """
        Use this decorator to make minecraft function
        """
        if isinstance(attributes[0], typing.Callable):
            # Generates function
            function: typing.Callable = attributes[0]
            function()

            # Writing function
            self.framework.generated.functions[function.__name__] = list(self.framework.temporary.function)
            self.framework.temporary.function.clear()

            # Check attributes
            for attribute in attributes[1::]:
                attribute: str = attribute.lower().strip()

                # Load
                if attribute in constants.attributes.load:
                    self.framework.generated.attributes['load'] = function.__name__
                    continue

                # Tick
                if attribute in constants.attributes.tick:
                    self.framework.generated.attributes['tick'] = function.__name__
                    continue

                warnings.warn(f'Wrong attribute {attribute}')
            return lambda: self.exec(f'function {self.framework.settings.prefix_generated}'
                                     f'{self.framework.settings.project_name}:'
                                     f'{function.__name__}')
        return lambda x: self.function(x, *attributes)
