"""
Utils functions
"""
import codecs
import pickle
from typing import Iterable, List, Dict, Set


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def remove_punctuation(text):
    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.replace(";", "")
    text = text.replace("?", "")
    text = text.replace("!", "")
    text = text.replace(":", "")
    text = text.replace("'", "")
    text = text.replace('"', "")
    return text


def read_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def save_pickle(filename, data):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def get_clean_proper_nouns_txt(filename):
    """

    :param filename:
    :return:
    """
    with codecs.open(filename, "r", encoding="utf-8") as f:
        lines = f.read()
        l = []
        for line in lines.split("\n"):
            l.append(line.strip().split(" "))
        return l


def get_annotated_proper_nouns_txt(filename, with_comments=False):
    """

    :param filename:
    :param with_comments:
    :return:
    """
    with codecs.open(filename, "r", encoding="utf-8") as f:
        lines = f.read()
        d = {}
        for line in lines.split("\n"):
            if not line or (len(line) > 0 and line.startswith("#")):
                continue
            comment_index = line.strip().find("#")
            if 0 <= comment_index < len(line)-1:
                comment = line[comment_index+1:].strip()
                l_line = line[:comment_index].strip().split(":")
            else:
                comment = ""
                l_line = line.strip().split(":")
            # print(l_line)
            if len(l_line) < 2:
                continue
            lemma = l_line[0].strip()
            if lemma:
                if with_comments:
                    d[lemma] = {"forms": l_line[1].strip().split(" "), "comment": comment}
                else:
                    d[lemma] = l_line[1].strip().split(" ")
        return d


def save_annotated_proper_nouns_txt(filename, annotated_proper_nouns: List[Dict[str, Set[str]]]):
    lines = []
    for annotated_proper_noun in annotated_proper_nouns:
        line = ""
        for lemma in annotated_proper_noun:
            if lemma:
                line += "".join(lemma)+": "+" ".join(annotated_proper_noun[lemma])
        lines.append(line)
    with codecs.open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines)+"\n")


def one_of_them_in(l1, l2):
    for i in l1:
        if i in l2:
            return True
    return False


def partition(l, l_size):
    """
    >>> list(partition(["Un", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept"], 3))
    [['Un', 'Deux', 'Trois'], ['Quatre', 'Cinq', 'Six'], ['Sept']]

    :param l:
    :param l_size:
    :return:
    """
    for i in range(0, len(l), l_size):
        yield l[i:i+l_size]


def has_at_least_endings(forms: Iterable[str], endings: List[str], n) -> bool:
    i = 0
    for form in forms:
        for ending in endings:
            if form.endswith(ending):
                i += 1
    return i >= n
