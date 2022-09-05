"""
Thank you for using ButterSss's framework for Minecraft Datapacks!

DOCS: https://github.com/ButterSus/Kiwi/docs.md
"""

import sys

# PyKiwi
from PyKiwi.core import PyKiwi, Minecraft, Score, Scoreboard
from PyKiwi.enums.scoreboard.criteria import Criteria
PyKiwi._init_module = sys.modules[__name__]
