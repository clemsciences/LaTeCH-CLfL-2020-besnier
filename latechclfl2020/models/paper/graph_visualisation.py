"""
Generates 3 ego-graphs of Brynhildr from DLH, VÖL and NIB.
"""

import networkx as nx
import matplotlib.pyplot as plt

from latechclfl2020.models.paper.corpus_observation import load_graphs_for_paper
from latechclfl2020.models.texts import make_dict, Work


def script_generates_brynhildr_ego_graphs():
    graphs = load_graphs_for_paper()

    brynhildr = make_dict(vol="Brynhildr", nib="Brünhild", dlh="Brunichilde")
    for work in Work:
        name = brynhildr[work]
        ego_graph = nx.ego_graph(graphs[work], name)
        pos = nx.spring_layout(ego_graph, k=0.5, iterations=40)
        nx.draw(ego_graph, pos=pos, node_color="gray", node_size=30, width=0.5,
                edge_color="gray", with_labels=True, font_size=10)
        plt.draw()
        plt.savefig(f"{name}.png", dpi=1000)
        plt.clf()


if __name__ == "__main__":
    script_generates_brynhildr_ego_graphs()
