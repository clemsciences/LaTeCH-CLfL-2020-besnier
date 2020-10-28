"""

"""

import latechclfl2020.volsunga.data as volsunga_data

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def script_preparation():
    volsunga_data.script_extract_volsunga_proper_nouns()
    proper_nouns = volsunga_data.get_volsunga_proper_nouns()
    volsunga_data.script_volsunga_clusterise_proper_nouns(proper_nouns)

    volsunga_data.script_volsunga_prepare_clean_proper_nouns()


if __name__ == "__main__":
    script_preparation()
