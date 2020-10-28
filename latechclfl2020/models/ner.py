"""
Named-entity recognition
"""
from collections import defaultdict
from typing import Set, List

import numpy as np
from cltk.text_reuse.levenshtein import Levenshtein
from sklearn.cluster import AgglomerativeClustering

from latechclfl2020 import utils, constants


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def extract_proper_nouns(tokens):
    """
    Proper nouns are tokens which only occur with the first character capitalised

    :param tokens:
    :return:
    """
    lower_tokens = set([token for token in tokens if token and len(token) > 0 and
                        not token[0].isupper()])

    capitalized_tokens = [token for token in tokens if token and len(token) > 0 and
                          token[0].isupper()]

    proper_nouns = set([token for token in capitalized_tokens
                        if token.lower() not in lower_tokens])

    proper_nouns = sorted(list(proper_nouns))
    return proper_nouns


def compute_distance_matrix(proper_nouns: List[str]):
    """
    Distance matrix with Levenshtein distance.

    :param proper_nouns: Items of proper_nouns must be unique
    :return:
    """
    levenshtein = Levenshtein()

    # We try to keep regroup different forms of a lemma
    distance_matrix = np.zeros((len(proper_nouns), len(proper_nouns)))

    for i in range(len(proper_nouns)):
        for j in range(len(proper_nouns)):
            distance_matrix[i, j] = levenshtein.Levenshtein_Distance(proper_nouns[i], proper_nouns[j])

    return distance_matrix


def compute_lemmatize_proper_nouns(distance_matrix, proper_nouns: List):
    """
    All inflected forms of a single word are grouped according to distance reasons.
    :param distance_matrix:
    :param proper_nouns:
    :return:
    """
    clustering_method = AgglomerativeClustering(n_clusters=None, affinity="precomputed", distance_threshold=3,
                                                linkage="average", compute_full_tree=True)
    # print(distance_matrix[:10, :10])
    # print(distance_matrix.shape)
    clustering_method.fit(distance_matrix)
    # print(clustering_method.labels_)
    # print(np.max(clustering_method.labels_))
    # print(len(clustering_method.labels_))

    lemmas = defaultdict(set)

    for i in range(distance_matrix.shape[0]):
        lemmas[clustering_method.labels_[i]].add(proper_nouns[i])

    return lemmas
