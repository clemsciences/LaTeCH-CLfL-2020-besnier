"""
Languages of texts used in the project
"""

import enum

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


class Language(enum.Enum):
    latin = enum.auto()
    middle_high_german = enum.auto()
    old_norse = enum.auto()
