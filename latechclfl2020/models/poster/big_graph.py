"""

"""

import itertools
import networkx as nx
import matplotlib.pyplot as plt

from latechclfl2020.models.languages import Language
from latechclfl2020.models.reconstruction import correspondences
from latechclfl2020.models.social_network import TextSocialNetwork
from latechclfl2020.models.texts import Work
from latechclfl2020.models.scripts import load_generated_graph, merge_graphs


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def generate_full_graph():
    graphs = merge_graphs([*load_generated_graph(Work.DLH, True).chapters[1:4],
                           load_generated_graph(Work.NIB),
                           load_generated_graph(Work.VOL)])

    names = set()
    for correspondence in correspondences:
        for w1, w2 in itertools.combinations(correspondence, 2):
            if correspondence[w1] and correspondence[w2]:
                names.add(correspondence[w1])
                names.add(correspondence[w2])
                graphs.add_edge(correspondence[w1], correspondence[w2])
    # nodes = graphs.nodes
    # for node in nodes:
    #     if node not in names:
    names_to_remove = [node for node in graphs if node not in names]
    graphs.remove_nodes_from(names_to_remove)

    nx.draw(graphs, node_color="gray", node_size=30, width=0.5,
            edge_color="gray", with_labels=True, font_size=10, scale=2)
    plt.draw()
    plt.savefig(f"all_characters.png", dpi=1000)


def generate_graph_with_only_compared_characters(graph: TextSocialNetwork):
    names = set()
    for correspondence in correspondences:
        for w1, w2 in itertools.combinations(correspondence, 2):
            if w1.get_language() == graph.language and correspondence[w1]:
                names.add(correspondence[w1])
            elif w2.get_language() == graph.language and correspondence[w2]:
                names.add(correspondence[w2])
    print(names)
    names_to_remove = [node for node in graph if node not in names]
    graph.remove_nodes_from(names_to_remove)

    nx.draw(graph, node_color="gray", node_size=30, width=0.5,
            edge_color="gray", with_labels=True, font_size=10, scale=1)
    plt.draw()
    plt.savefig(f"{graph.name}_matching_character.png", dpi=250)
    plt.clf()


if __name__ == "__main__":
    graphs = [merge_graphs(load_generated_graph(Work.DLH, True).chapters[1:4]),
              load_generated_graph(Work.NIB),
              load_generated_graph(Work.VOL)]
    graphs[0].language = Language.latin
    graphs[0].name = "DLH"
    for graph in graphs:
        generate_graph_with_only_compared_characters(graph)

