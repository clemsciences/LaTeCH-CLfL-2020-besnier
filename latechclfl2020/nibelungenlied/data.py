"""

"""

from sigurd.nib_augsburg.nib_reader import read_names, MAIN_LINKS, read_tei, \
    read_rivers, read_cities, read_regions_and_countries, read_peoples


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

    :return: annotated person names
    """
    nibelungen_names = read_names()
    return nibelungen_names


def get_nibelungenlied_annotated_places():
    """
    >>> annotated_places = get_nibelungenlied_annotated_places()
    >>> annotated_places["Donau"]
    ['Tvonowe', 'Tunawe', 'Tverne']

    >>> annotated_places["Metz"]
    ['Metzzen', 'Mezzen', 'Mezzin', 'Metzen']

    >>> annotated_places["Schwaben"]
    ['Swaben']

    :return: annotated places
    """
    d = {}
    d.update(read_rivers())
    d.update(read_cities())
    d.update(read_regions_and_countries())
    return d


def get_nibelungenlied_annotated_groups():
    """
    >>> annotated_places = get_nibelungenlied_annotated_groups()
    >>> annotated_places['Hunnen']
    ['Hunin', 'Hunen']

    :return: annotated groups
    """
    d = {}
    d.update(read_peoples())
    return d
