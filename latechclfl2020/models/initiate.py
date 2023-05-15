"""
Download resources for the project.
"""
from cltk.data.fetch import FetchCorpus

import nltk

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def initiate():
    fc = FetchCorpus("lat")
    fc.import_corpus("lat_models_cltk")

    nltk.download("punkt")


if __name__ == "__main__":
    initiate()
