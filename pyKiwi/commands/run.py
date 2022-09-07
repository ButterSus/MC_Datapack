"""
Open source project by ButterSss
"""

from __future__ import annotations
import typing


if typing.TYPE_CHECKING:
    import pyKiwi.core as core


def run(self: core.PyKiwi, command: str):
    self.Compiler.append(command)


def main(self: core.PyKiwi, command: str):
    return lambda: run(self, command)
