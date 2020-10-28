"""

"""

from sigurd.nib_augsburg.nib_reader import read_names, MAIN_LINKS, read_tei


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def get_nibelungen_book():
    """
    >>> get_nibelungen_book()[0][0][0]
    'UNS IST> In alten'

    :return:
    """
    return read_tei(MAIN_LINKS[0])


def get_nibelungenlied_annotated_names():
    """
    >>> annotated_names = get_nibelungenlied_annotated_names()
    >>> annotated_names["Brünhild"]
    ["Prvnh'", 'Prvenhilde', 'Privnhilde', 'Prvnhilt', 'Prvonhilde', 'Prvnhilde', 'Prunhilt', 'Prunhilde']

    :return:
    """
    nibelungen_names = read_names()
    return nibelungen_names
