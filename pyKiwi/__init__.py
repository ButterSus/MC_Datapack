"""
Thank you for using ButterSss's framework for Minecraft Datapacks!

DOCS: https://github.com/ButterSus/Kiwi/docs.md
"""

import sys

# pyKiwi
from pyKiwi.core import PyKiwi, Minecraft, Score, Scoreboard
from pyKiwi.enums.scoreboard.criteria import Criteria
PyKiwi._init_module = sys.modules[__name__]
