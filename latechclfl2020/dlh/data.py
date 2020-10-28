"""
Retrieves results about Name-entity recognition
"""


import os
import codecs
from functools import lru_cache
from typing import List, Set

from cltk.tokenize.latin.sentence import SentenceTokenizer
from cltk.tokenize.latin.word import WordTokenizer

import numpy as np

from latechclfl2020.models.texts import Work
from latechclfl2020 import utils, PACKDIR
from latechclfl2020 import constants
import latechclfl2020.models.ner as ner


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]

latin_sentence_tokenizer = SentenceTokenizer()
latin_word_tokenizer = WordTokenizer()


# region book
@lru_cache()
def extract_parsed_dlh_books(verbose=False) -> List[List[List[List[str]]]]:
    """
    TXT files to str
    >>> books = extract_parsed_dlh_books()
    >>> len(books)
    10

    :return: list of books ; a book is a list of paragraphs ;
    a paragraph is a list of sentences ; a sentence is a list of word
    """
    directory = os.path.join(PACKDIR,
                             Work.DLH.get_main_directory(),
                             "gregory_of_tours_txt")

    retrieved_texts = []
    book_filenames = os.listdir(directory)
    book_filenames = sorted(book_filenames, key=lambda x: int(x.split(".")[0]))
    for filename in book_filenames:
        if verbose:
            print(filename)
        with codecs.open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
            text = f.read()
            lines = [[latin_word_tokenizer.tokenize(utils.remove_punctuation(sentence))
                      for sentence in latin_sentence_tokenizer.tokenize(line.strip())]
                     for line in text.split("\n") if line.strip()]
        retrieved_texts.append(lines)
    return retrieved_texts


def save_dlh_books():
    """
    >>> save_dlh_books()

    :return:
    """
    books = extract_parsed_dlh_books()
    dlh_books_path = os.path.join(PACKDIR,
                                  Work.DLH.get_main_directory(),
                                  constants.DLH_BOOKS)
    utils.save_pickle(dlh_books_path, books)


def get_parsed_dlh_books():
    """
    >>> parsed_books = get_parsed_dlh_books()
    >>> len(parsed_books)
    10

    :return:
    """
    dlh_books_path = os.path.join(PACKDIR,
                                  Work.DLH.get_main_directory(),
                                  constants.DLH_BOOKS)
    if not os.path.exists(dlh_books_path):
        save_dlh_books()
    return utils.read_pickle(dlh_books_path)
# endregion


def compute_clusterise_proper_nouns(proper_nouns):
    """

    :param proper_nouns:
    :return:
    """
    distance_matrix = ner.compute_distance_matrix(proper_nouns)
    filename = os.path.join(PACKDIR,
                            Work.DLH.get_main_directory(),
                            constants.DISTANCE_PROPER_NOUNS_DLH)
    np.save(filename, distance_matrix)
    mat = np.load(filename+".npy")
    lemmas = ner.compute_lemmatize_proper_nouns(mat, proper_nouns)
    print(lemmas)
    return lemmas


def get_clusterised_proper_nouns():
    """
    >>> len(get_clusterised_proper_nouns())
    1138

    :return:
    """
    dlh_proper_nouns_path = os.path.join(PACKDIR,
                                         Work.DLH.get_main_directory(),
                                         constants.CLUSTERISED_PROPER_NOUNS_DLH)
    return utils.read_pickle(dlh_proper_nouns_path)


def choose_lemma_from_forms(forms: Set[str]) -> str:
    """
    >>> clusterised_proper_nouns = get_clusterised_proper_nouns()
    >>> choose_lemma_from_forms(clusterised_proper_nouns[3])
    'Cavellonum'

    :param forms:
    :return:
    """

    for form in forms:
        if form.endswith("us"):
            return form
        elif form.endswith("um"):
            return form
        elif form.endswith("a"):
            return form
    return list(forms)[0]


def get_lemmatised_dlh_proper_nouns():
    """
    >>> get_lemmatised_dlh_proper_nouns()['Burgundia']
    ['Burgundias', 'Burgundiam', 'Burgundiae', 'Burgundia', 'Burgundio']


    """
    file_path = os.path.join(PACKDIR,
                             Work.DLH.get_main_directory(),
                             constants.LEMMATISED_DLH_PROPER_NOUNS)
    return utils.get_annotated_proper_nouns_txt(file_path)


def get_lemmatised_dlh_person_names():
    """
    >>> get_lemmatised_dlh_person_names()['Chlodovechus']
    ['Chlodovechus', 'Chlodovechi', 'Chlodovechum', 'Chlodovecho']


    """
    file_path = os.path.join(PACKDIR,
                             Work.DLH.get_main_directory(),
                             constants.LEMMATISED_DLH_CLEAN_PERSON_NAMES)
    return utils.get_annotated_proper_nouns_txt(file_path)


def get_lemmatised_dlh_place_names():
    """
        >>> get_lemmatised_dlh_place_names()['Ligeris']
        ['Ligeris', 'Ligerem']

        """
    file_path = os.path.join(PACKDIR,
                             Work.DLH.get_main_directory(),
                             constants.LEMMATISED_DLH_CLEAN_PLACES)
    return utils.get_annotated_proper_nouns_txt(file_path)
