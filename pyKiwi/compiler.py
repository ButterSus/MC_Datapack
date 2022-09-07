"""
Open source project by ButterSss
"""

from __future__ import annotations

import os
import json
import shutil
import typing


if typing.TYPE_CHECKING:
    import pyKiwi as core


class Compiler:
    """
    Compiler for Kiwi framework
    """
    pack_format: int
    wasCompiled = False
    temporary_stack: list = list()
    framework: core.PyKiwi

    def __init__(self, framework: core.PyKiwi):
        self.framework = framework

    def append(self, command: str):
        self.temporary_stack.append(command)

    def compile(self):
        if self.wasCompiled:
            return
        self.wasCompiled = True
        if os.path.exists(self.framework.settings.project_name):
            shutil.rmtree(self.framework.settings.project_name)
        os.chdir(self.framework.settings.directory)
        os.mkdir(self.framework.settings.project_name)
        os.chdir(self.framework.settings.project_name)
        version = list(map(int, self.framework.settings.version.split('.')))
        version = [version[i] if i < len(version) else 0 for i in range(3)]
        match version:
            case [1, 13, x] if 2 >= x >= 0:
                self.pack_format = 4
            case [1, 14, x] if 4 >= x >= 0:
                self.pack_format = 4
            case [1, 15, x] if 2 >= x >= 0:
                self.pack_format = 5
            case [1, 16, x] if 1 >= x >= 0:
                self.pack_format = 5
            case [1, 16, x] if 5 >= x >= 2:
                self.pack_format = 6
            case [1, 17, x] if 1 >= x >= 0:
                self.pack_format = 7
            case [1, 18, x] if 1 >= x >= 0:
                self.pack_format = 8
            case [1, 18, 2]:
                self.pack_format = 9
            case [1, 19, x] if 2 >= x >= 0:
                self.pack_format = 10
            case _:
                self.pack_format = -1
        with open('pack.mcmeta', 'w') as file:
            file.write(
                json.dumps(
                    {
                        "pack": {
                            "pack_format": self.pack_format,
                            "description": self.framework.settings.description
                        }
                    },
                    indent=4
                )
            )
