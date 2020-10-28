"""
Download resources for the project.
"""

from cltk.corpus.utils.importer import CorpusImporter

import nltk

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]

if __name__ == "__main__":
    ci = CorpusImporter("latin")
    ci.import_corpus("latin_models_cltk")

    nltk.download("punkt")
