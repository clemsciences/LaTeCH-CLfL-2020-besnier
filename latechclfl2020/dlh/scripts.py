"""

"""
import codecs
import os
from collections import defaultdict

from latechclfl2020 import utils, constants, PACKDIR
from latechclfl2020.models.texts import Work
from latechclfl2020.dlh.data import compute_clusterise_proper_nouns,\
    get_parsed_dlh_books, get_clusterised_proper_nouns, choose_lemma_from_forms

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def script_dlh_lemmatise_proper_nouns():
    """
    >>> script_dlh_lemmatise_proper_nouns()

    :return:
    """
    clusterised_proper_nouns = get_clusterised_proper_nouns()
    l = []
    for i in clusterised_proper_nouns:
        proper_noun_group = clusterised_proper_nouns[i]
        l.append({choose_lemma_from_forms(proper_noun_group): proper_noun_group})
    filename = os.path.join(PACKDIR,
                            Work.DLH.get_main_directory(),
                            constants.LEMMATISED_DLH_PROPER_NOUNS)
    utils.save_annotated_proper_nouns_txt(filename, l)


def script_find_book_occurrence():
    """
    >>> script_find_book_occurrence()

    :return:
    """
    d = defaultdict(list)
    annotated_proper_nouns = utils.get_annotated_proper_nouns_txt(constants.LEMMATISED_DLH_CLEAN_PERSON_NAMES)
    dlh_books = get_parsed_dlh_books()
    for i, book in enumerate(dlh_books):
        for j, para in enumerate(book):
            for k, sentence in enumerate(para):
                for lemma in annotated_proper_nouns:
                    for form in annotated_proper_nouns[lemma]:
                        if form in sentence:
                            d[form].append(f"{i+1}-{j+1}-{k+1}")

    filename = os.path.join(PACKDIR,
                            Work.DLH.get_main_directory(),
                            "dlh_lemma_occurrences.txt")
    with codecs.open(filename, "w", encoding="utf-8") as f:
        l = []
        for item in d:
            line = f"{item}: ({len(d[item])}) "+" ".join(d[item])
            l.append(line)
        f.write("\n".join(l))


def script_find_where_character_occurs():
    """
    >>> script_find_where_character_occurs()

    :return:
    """

    d = defaultdict(list)
    annotated_proper_nouns = utils.get_annotated_proper_nouns_txt(constants.LEMMATISED_DLH_CLEAN_PERSON_NAMES)
    dlh_books = get_parsed_dlh_books()
    for i, book in enumerate(dlh_books):
        for j, para in enumerate(book):
            for k, sentence in enumerate(para):
                for lemma in annotated_proper_nouns:
                    for form in annotated_proper_nouns[lemma]:
                        if form in sentence:
                            d[form].append(f"{i + 1}-{j + 1}-{k + 1}")

    filename = os.path.join(PACKDIR,
                            Work.DLH.get_main_directory(),
                            "dlh_clean_lemma_occurrences.txt")
    with codecs.open(filename, "w", encoding="utf-8") as f:
        l = []
        for item in d:
            line = f"{item}: ({len(d[item])}) " + " ".join(d[item])
            l.append(line)
        f.write("\n".join(l))


if __name__ == "__main__":
    script_dlh_lemmatise_proper_nouns()
