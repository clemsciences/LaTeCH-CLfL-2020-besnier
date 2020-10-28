"""
Scripts to generate character graphs

"""
import os
from typing import List

from latechclfl2020 import PACKDIR

from latechclfl2020.models.texts import Work
from latechclfl2020.models.social_network import TextSocialNetwork
from latechclfl2020.nibelungenlied import data as nib_data
from latechclfl2020.volsunga import data as vol_data
from latechclfl2020.dlh import data as dlh_data
from latechclfl2020.models import social_network

import networkx as nx
# import netcomp as nc


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def load_graph_data(work: Work):
    """
    From work to character graphs directly from texts.
    :param work: work
    :return: character graph
    """
    network = social_network.TextSocialNetwork()
    if work == Work.NIB:
        network = social_network.NibelungenliedSocialNetwork()
        network.load_text(nib_data.get_nibelungen_book())
        network.load_character_names(
            nib_data.get_nibelungenlied_annotated_names())
    elif work == Work.VOL:
        network = social_network.VolsungaSocialNetwork()
        network.load_text(vol_data.get_volsunga_text())
        network.load_character_names(vol_data.get_volsunga_annotated_names())
    elif work == Work.DLH:
        network = social_network.DLHSocialNetwork()
        network.load_text(dlh_data.get_parsed_dlh_books())
        network.load_character_names(dlh_data.get_lemmatised_dlh_person_names())
    return network


def generate_graph(work: Work, by_chapter=False):
    """

    :param work: work
    :param by_chapter: are character graphs computed by chatper?
    """
    network = load_graph_data(work)
    if by_chapter:
        network.generate_graph_by_chapter(work.name)
    else:
        network.generate_graph(work.name)
    directory = os.path.join(PACKDIR, "models", work.get_graph_directory())
    filename = os.path.join(directory, work.get_graph_filename(by_chapter))
    if not os.path.exists(os.path.join(PACKDIR, "models", work.get_graph_directory())):
        os.mkdir(directory)
    nx.write_gpickle(network, filename)


def load_generated_graph(work: Work, by_chapter=False) -> TextSocialNetwork:
    """
    Load graphs that were already saved.

    :param work: work
    :param by_chapter: are character graphs computed by chatper?
    :return:
    """
    filename = os.path.join(PACKDIR, "models", work.get_graph_directory(),
                            work.get_graph_filename(by_chapter))
    return nx.read_gpickle(filename)


def merge_graphs(graphs: List[nx.Graph]):
    """

    :param graphs: list of graphs
    :return: the merged graphs
    """
    result = nx.Graph()
    for g in graphs:
        result = nx.compose(result, g)
    return result


def generate_graphs():
    """
    Generate all possible graphs for DLH, VÖL and NIB.
    """
    generate_graph(Work.NIB)
    generate_graph(Work.NIB, True)

    generate_graph(Work.VOL)
    generate_graph(Work.VOL, True)

    generate_graph(Work.DLH)
    generate_graph(Work.DLH, True)


if __name__ == "__main__":
    generate_graphs()
