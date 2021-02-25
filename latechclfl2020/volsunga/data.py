"""

"""
import codecs
import os
from norsecorpus import PACKDIR as NORSECORPUS_PACKDIR
from norsecorpus.reader import read_tei_words

from latechclfl2020 import PACKDIR
import latechclfl2020.utils as utils
import latechclfl2020.constants as constants
import latechclfl2020.models.ner as ner
from latechclfl2020.models.texts import Work

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


# region Völsunga saga

def get_volsunga_text():
    """
    >>> get_volsunga_text()[0][1][0][2]
    'at'

    :return:
    """
    path = os.path.join(NORSECORPUS_PACKDIR, "data", "heimskringla",
                        "Völsunga_saga", "tei")
    filename = "volsunga.xml"
    return read_tei_words(filename, path)
# endregion


# region proper nouns
# region preparation
def script_extract_volsunga_proper_nouns():
    """
    >>> script_extract_volsunga_proper_nouns()

    :return:
    """
    book = get_volsunga_text()
    tokens = [word for chapter in book for paragraph in chapter
              for sentence in paragraph for word in sentence]

    proper_nouns = ner.extract_proper_nouns(tokens)
    filename = os.path.join(PACKDIR,
                            Work.VOL.get_main_directory(),
                            constants.VOLSUNGA_PROPER_NOUNS)
    utils.save_pickle(filename, proper_nouns)


def get_volsunga_proper_nouns():
    """
    >>> proper_nouns = get_volsunga_proper_nouns()
    >>> proper_nouns[76]
    'Gautlands'

    :return:
    """
    filename = os.path.join(PACKDIR,
                            Work.VOL.get_main_directory(),
                            constants.VOLSUNGA_PROPER_NOUNS)
    return utils.read_pickle(filename)


def script_volsunga_clusterise_proper_nouns(proper_nouns):
    """
    >>> vol_proper_nouns = get_volsunga_proper_nouns()
    >>> script_volsunga_clusterise_proper_nouns(vol_proper_nouns)

    :param proper_nouns:
    :return:
    """
    proper_nouns = list(proper_nouns)
    volsunga_distance_matrix = ner.compute_distance_matrix(proper_nouns)
    lemmas = ner.compute_lemmatize_proper_nouns(volsunga_distance_matrix, proper_nouns)
    filename = os.path.join(PACKDIR,
                            Work.VOL.get_main_directory(),
                            constants.CLUSTERED_VOLSUNGA_PROPER_NOUNS)
    utils.save_pickle(filename, lemmas)


def get_volsunga_lemmatised_proper_nouns():
    """
    >>> lemmatised_proper_nouns = get_volsunga_lemmatised_proper_nouns()
    >>> sorted(list(lemmatised_proper_nouns[45]))
    ['Guðrún', 'Guðrúnu']

    :return:
    """
    filename = os.path.join(PACKDIR,
                            Work.VOL.get_main_directory(),
                            constants.CLUSTERED_VOLSUNGA_PROPER_NOUNS)
    return utils.read_pickle(filename)


def script_volsunga_prepare_clean_proper_nouns():
    """
    >>> script_volsunga_prepare_clean_proper_nouns()

    :return:
    """
    vlpp = get_volsunga_lemmatised_proper_nouns()
    filename = os.path.join(PACKDIR,
                            Work.VOL.get_main_directory(),
                            constants.RESULT_VOLSUNGA_PROPER_NOUNS)
    with codecs.open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join([" ".join(vlpp[number]) for number in vlpp]))
# endregion


# region annotations
def get_volsunga_clean_proper_nouns():
    """
    >>> clean_proper_nouns = get_volsunga_clean_proper_nouns()
    >>> clean_proper_nouns[45]
    ['Fáfni', 'Fáfnir', 'Fáfnis']

    :return: all proper nouns
    """
    filename = os.path.join(PACKDIR,
                            Work.VOL.get_main_directory(),
                            constants.RESULT_VOLSUNGA_PROPER_NOUNS)
    return utils.get_clean_proper_nouns_txt(filename)


def get_volsunga_annotated_names():
    """
    Names -> proper nouns of persons
    >>> annotated_names = get_volsunga_annotated_names()
    >>> annotated_names["Sigmundr"]
    ['Sigmundr', 'Sigmund', 'Sigmundi', 'Sigmundar']

    :return: annotated persons
    """
    volsunga_names_proper_nouns = os.path.join(
        PACKDIR,
        Work.VOL.get_main_directory(),
        constants.VOLSUNGA_CLEAN_NAMES_PROPER_NOUNS)
    return utils.get_annotated_proper_nouns_txt(volsunga_names_proper_nouns)


def get_volsunga_annotated_places():
    """
    >>> annotated_names = get_volsunga_annotated_places()
    >>> annotated_names["Frakkland"]
    ['Frakklands']

    :return: annotated places
    """
    volsunga_places_proper_nouns = os.path.join(
        PACKDIR,
        Work.VOL.get_main_directory(),
        constants.VOLSUNGA_CLEAN_PLACES_PROPER_NOUNS)
    return utils.get_annotated_proper_nouns_txt(volsunga_places_proper_nouns)


def get_volsunga_annotated_groups():
    """
    >>> annotated_names = get_volsunga_annotated_groups()
    >>> annotated_names['Hýnir']
    ['Hýnir']

    :return: annotated groupd
    """
    volsunga_groups_proper_nouns = os.path.join(
        PACKDIR,
        Work.VOL.get_main_directory(),
        constants.VOLSUNGA_CLEAN_GROUP_PROPER_NOUNS)
    return utils.get_annotated_proper_nouns_txt(volsunga_groups_proper_nouns)
# endregion
# endregion
