"""
Where works are defined.
"""

import enum
import latechclfl2020.models.languages as lng
import latechclfl2020.constants as constants


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


class Work(enum.Enum):
    NIB = "Nibelungenlied"
    VOL = "Völsunga saga"
    DLH = "Decem Libri Historiarum"

    def get_language(self):
        if self == Work.NIB:
            return lng.Language.middle_high_german
        elif self == Work.VOL:
            return lng.Language.old_norse
        elif self == Work.DLH:
            return lng.Language.latin

    def get_graph_filename(self, by_chapter=False):
        if self == Work.NIB:
            return constants.NIB_GRAPH_BY_CHAPTER if by_chapter \
                else constants.NIB_GRAPH
        elif self == Work.VOL:
            return constants.VOL_GRAPH_BY_CHAPTER if by_chapter \
                else constants.VOL_GRAPH
        elif self == Work.DLH:
            return constants.DLH_GRAPH_BY_CHAPTERS if by_chapter \
                else constants.DLH_GRAPH

    def get_graph_directory(self):
        if self == Work.NIB:
            return constants.NIB_GRAPHS_DIRECTORY
        elif self == Work.VOL:
            return constants.VOLSUNGA_GRAPHS_DIRECTORY
        elif self == Work.DLH:
            return constants.DLH_GRAPHS_DIRECTORY

    def get_main_directory(self):
        if self == Work.NIB:
            return constants.NIB_DIRECTORY
        elif self == Work.VOL:
            return constants.VOL_DIRECTORY
        elif self == Work.DLH:
            return constants.DLH_DIRECTORY


def make_dict(vol=None, nib=None, dlh=None):
    return {Work.VOL: vol, Work.NIB: nib, Work.DLH: dlh}
