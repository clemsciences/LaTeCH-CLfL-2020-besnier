"""
Features extracted from character graphs that are used in the paper.
"""

import collections
from typing import Dict, Union

import networkx as nx
import matplotlib.pyplot as plt
from latechclfl2020.constants import PUNCTUATIONS
from latechclfl2020.models.texts import Work, make_dict
from latechclfl2020.models.scripts import load_generated_graph, merge_graphs

from latechclfl2020.nibelungenlied import data as nib_data
from latechclfl2020.volsunga import data as vol_data
from latechclfl2020.dlh import data as dlh_data

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def display_general_features():
    """
    >>> display_general_features()

    """

    # region number of tokens

    nib_tokens = [token for chapter in nib_data.get_nibelungen_book()
                  for paragraph in chapter
                  for sentence in paragraph
                  for token in sentence.split(" ")
                  if token not in PUNCTUATIONS]
    print(f"Number of tokens in the Nibelungenlied {len(nib_tokens)}")
    print(f"Number of unique tokens in the Nibelungenlied {len(set(nib_tokens))}")

    vol_tokens = [token for chapter in vol_data.get_volsunga_text()
                  for paragraph in chapter
                  for sentence in paragraph
                  for token in sentence
                  if token not in PUNCTUATIONS]
    print(f"Number of tokens in the the Völsunga saga {len(vol_tokens)}")
    print(f"Number of unique tokens in the Völsunga saga {len(set(vol_tokens))}")

    dlh_tokens = [token for book in dlh_data.get_parsed_dlh_books()
                  for paragraph in book
                  for sentence in paragraph
                  for token in sentence
                  if token not in PUNCTUATIONS]
    print(f"Number of tokens in the Decem Libri Historiarum {len(dlh_tokens)}")
    print(f"Number of unique tokens in the Decem Libri Historiarum {len(set(dlh_tokens))}")

    # endregion

    # region number of characters
    nib_n_characters = nib_data.get_nibelungenlied_annotated_names()
    print(f"Number of characters in the Nibelungenlied {len(nib_n_characters)}")
    vol_n_characters = vol_data.get_volsunga_annotated_names()
    print(f"Number of characters in the Völsunga saga {len(vol_n_characters)}")
    dlh_n_characters = dlh_data.get_lemmatised_dlh_person_names()
    print(f"Number of characters in the Decem Libri Historiarum {len(dlh_n_characters)}")
    # endregion

    # region graph analysis
    graphs = load_graphs_for_paper()
    display_graph_features(graphs[Work.NIB])
    display_graph_features(graphs[Work.VOL])
    display_graph_features(graphs[Work.DLH])
    # endregion


def show_(graph):

    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)  # degree sequence
    degree_count = collections.Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color="b")

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    gcc = graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0])
    pos = nx.spring_layout(graph)
    plt.axis("off")
    nx.draw_networkx_nodes(graph, pos, node_size=20)
    nx.draw_networkx_edges(graph, pos, alpha=0.4)
    plt.show()

    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    dmax = max(degree_sequence)

    plt.loglog(degree_sequence, "b-", marker="o")
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")

    # draw graph in inset
    plt.axes([0.45, 0.45, 0.45, 0.45])
    gcc = graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0])
    pos = nx.spring_layout(gcc)
    plt.axis("off")
    nx.draw_networkx_nodes(gcc, pos, node_size=20)
    nx.draw_networkx_edges(gcc, pos, alpha=0.4)
    plt.show()


def display_graph_features(graph: nx.Graph):
    print(graph)
    print(f"Number of nodes {len(graph)}")
    print(f"Number of edges {len(graph.edges)}")
    print(f"degrees {sort_pairs(graph.degree)}")
    print(f"degree_centrality {sort_dict(nx.degree_centrality(graph))}")
    print(f"eigenvector centrality {sort_dict(nx.eigenvector_centrality(graph))}")
    print(f"closeness centrality {sort_dict(nx.closeness_centrality(graph))}")
    print(f"betweeness centrality {sort_dict(nx.betweenness_centrality(graph))}")


def compute_orders_for_paper(graphs: Dict[Work, nx.Graph], correspondences):
    d = {}
    for work in Work:
        print("\n")
        graph = graphs[work]
        characters = [c[work] for c in correspondences if c]
        degree_centrality = sort_dict(nx.degree_centrality(graph))
        eigenvector_centrality = sort_dict(nx.eigenvector_centrality(graph))
        closeness_centrality = sort_dict(nx.closeness_centrality(graph))
        betweeness_centrality = sort_dict(nx.betweenness_centrality(graph))
        print("number of characters", len(betweeness_centrality))
        print("Character [degree rank, eigenvector centrality rank, closeness centrality rank, "
              "betweeness centrality rank, betweeness centrality rank]")
        d[work] = {}
        for charac in characters:
            if charac:
                order_degree = [i+1 for i, j in enumerate(degree_centrality) if j[0] == charac]
                order_eigenvector = [i+1 for i, j in enumerate(eigenvector_centrality) if j[0] == charac]
                order_closeness = [i+1 for i, j in enumerate(closeness_centrality) if j[0] == charac]
                order_betweeness = [i+1 for i, j in enumerate(betweeness_centrality) if j[0] == charac]
                d[work][charac] = [*order_degree, *order_eigenvector, *order_closeness, *order_betweeness]
                print(charac, d[work][charac])
    return d


def sort_dict(dictionary: dict):
    return sorted([(key, value) for (key, value) in dictionary.items()], key=lambda x: x[1], reverse=True)


def sort_pairs(pairs: list):
    return sorted([(key, value) for (key, value) in pairs], key=lambda x: x[1], reverse=True)


def load_graphs_for_paper():
    nib_graph = load_generated_graph(Work.NIB)
    vol_graph = load_generated_graph(Work.VOL)
    dlh_graph_chap = load_generated_graph(Work.DLH, True)
    dlh_graph_for_analysis = merge_graphs(dlh_graph_chap.chapters[1:4])
    graphs = make_dict(vol=vol_graph, nib=nib_graph, dlh=dlh_graph_for_analysis)
    return graphs


def analyze_characters(character_lemmata: Dict[Work, Union[str, None]], graphs: Dict[Work, nx.Graph]):
    d = {}
    for work in Work:
        if character_lemmata[work] is not None:
            lemma = character_lemmata[work]
            graph = graphs[work]
            if lemma in graph:
                neighbours = []
                for neighbour in graph.neighbors(lemma):
                    neighbours.append(neighbour)
                    # analyse_character(neighbour, graph)
                # print(graphs[work].degree)
                centrality_features = analyse_character(lemma, graph)
                # print(work, lemma, centrality_features, f"degree {len(neighbours)} neighbours: {neighbours}")
                d[work] = [lemma, *centrality_features, len(neighbours)]
    return d


def analyse_character(character_lemma: Union[str, None], graph: nx.Graph, verbose=False):
    if character_lemma:
        degree_centrality = [value for (key, value) in nx.degree_centrality(graph).items()
                             if key == character_lemma]
        eigenvector_centrality = [value for (key, value) in nx.eigenvector_centrality(graph).items()
                                  if key == character_lemma]
        closeness_centrality = [value for (key, value) in nx.closeness_centrality(graph).items()
                                if key == character_lemma]
        betweeness_centality = [value for (key, value) in nx.betweenness_centrality(graph).items()
                                if key == character_lemma]
        if verbose:
            print("degree centrality", character_lemma, *degree_centrality)
            print("eigenvector centrality", character_lemma, *eigenvector_centrality)
            print("closeness centrality", character_lemma, *closeness_centrality)
            print("betweeness centrality", character_lemma, *betweeness_centality)
        return [*degree_centrality,
                *eigenvector_centrality,
                *closeness_centrality,
                *betweeness_centality]


# region table
def make_line(line):
    res = []
    for work in [Work.DLH, Work.VOL, Work.NIB]:
        if work in line:
            l = ["%.2f" % item if isinstance(item, float)
                 else str(item) for item in line[work]]
            res.append(" & ".join(l))
        else:
            res.append(" & ".join(["missing", "-", "-", "-", "-", "-"]))
    return " & ".join(res)+" \\\\ \\hline \n"


def make_table(lines, caption):
    table_start = """
    \\begin{table}
    \\begin{center}
    \\caption{"""+caption+"""}
    \\resizebox{\\textwidth}{!}{%
    \\label{tab:results}
    \\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
    \\hline
    \\multicolumn{6}{|c|}{\\textbf{DLH}} & \\multicolumn{6}{|c|}{\\textbf{VÖL}} & \\multicolumn{6}{|c|}{\\textbf{NIB}} \\\\ \\hline\n
    Name & d & e & c & b & n & Name & d & e & c & b & n & Name & d & e & c & b & n \\\\\\hline 
    
    """
    table_end = """
    \\hline
    \\end{tabular}}
    \\end{center}
    \\end{table}
    """

    return table_start+"\n".join([make_line(line) for line in lines])+table_end
# endregion


if __name__ == "__main__":
    display_general_features()
