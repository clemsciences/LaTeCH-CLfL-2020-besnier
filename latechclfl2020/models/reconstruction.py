"""
Correspondences found by philologists in between DLH, VÖL and NIB.
They are used to look at their evolution over time.
"""

from latechclfl2020.models.texts import make_dict
from latechclfl2020.models.paper.corpus_observation import analyze_characters, \
    make_table, load_graphs_for_paper, compute_orders_for_paper


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


correspondences = [
    make_dict(vol="Sigurðr", nib="Siegfried", dlh="Sygiberthus"),
    make_dict(vol="Gunnarr", nib="Gunther", dlh="Guntharius"),
    make_dict(vol="Brynhildr", nib="Brünhild", dlh="Brunichilde"),
    make_dict(vol="Sigmundr", nib="Siegmund", dlh="Sigimundus"),
    make_dict(vol="Atli", nib="Etzel", dlh="Attila"),
    make_dict(nib="Alberich", dlh="Alaricus"),
    make_dict(nib="Dietrich", dlh="Theodoricus"),
    make_dict(vol="Grímhildr", nib="Kriemhild"),
    make_dict(vol="Reginn", dlh="Ragnacharius"),
    make_dict(vol="Fáfnir", dlh="Farro"),
]

character_feature_ranks = compute_orders_for_paper(load_graphs_for_paper(), correspondences)


features_lines = []
graphs = load_graphs_for_paper()
for correspondence in correspondences:
    features_lines.append(analyze_characters(correspondence, graphs))

table = make_table(features_lines, "Graph features for 10 characters that occur at least in two of the three "
                                   "studied texts. Here d is for degree centrality, e for eigenvector centrality, "
                                   "c for closeness centrality, b for betweeness centrality and "
                                   "n for the number of neighbours (i.e. the degree).")
print(character_feature_ranks)
print(table)
