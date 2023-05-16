"""Module made to transform annotations into spaCy-usable training data
"""

from collections import defaultdict
import json
from typing import List, Dict

from latechclfl2020.models.initiate import initiate
from latechclfl2020.dlh.data import extract_parsed_dlh_books, get_lemmatised_dlh_person_names, \
    get_lemmatised_dlh_place_names

from latechclfl2020.volsunga.data import get_volsunga_text, get_volsunga_annotated_names, \
    get_volsunga_annotated_places, get_volsunga_annotated_groups

from latechclfl2020.nibelungenlied.data import get_nibelungen_book, get_nibelungenlied_annotated_names, \
    get_nibelungenlied_annotated_groups, get_nibelungenlied_annotated_places


initiate()


def invert_dictionary(dictionary):
    inverted_dictionary = defaultdict(list)
    for key, values in dictionary.items():
        for value in values:
            if len(value) > 0:
                inverted_dictionary[value].append(key)
    return inverted_dictionary


def add_found_items(sentence: str, tokenized_sentence: List[str], inverse_dictionary: Dict[str, List[str]], label: str):
    l = []
    for i in inverse_dictionary:
        if i in tokenized_sentence:

            if i:
                start = sentence.index(i)
                end = start + len(i)
                l.append(dict(token=i, lemma=inverse_dictionary[i], start=start, end=end, label=label))
            else:
                # print(repr(i), inverse_dictionary[name])
                pass
    return l


def extract_ner_annotation(sentences: List[List[str]], annotations: List[Dict]):
    data = defaultdict(list)
    for annotation in annotations:
        for tokenized_sentence in sentences:
            sentence = " ".join(tokenized_sentence)
            item = add_found_items(sentence, tokenized_sentence, annotation["d"], annotation["label"])
            if item:
                data[sentence].extend(item)
    return data


def save_serializable_data(data, filename: str):
    with open(filename, "w") as f:
        f.write(json.dumps(data))


# region DLH
def get_dlh_sentences(books):
    dlh_sentences = []
    for book in books:
        for chapter in book:
            for tokenized_sentence in chapter:
                dlh_sentences.append(tokenized_sentence)
    return dlh_sentences


dlh_books = extract_parsed_dlh_books()
dlh_d_person_names = get_lemmatised_dlh_person_names()
inverse_dlh_d_person_names = invert_dictionary(dlh_d_person_names)
dlh_d_place_names = get_lemmatised_dlh_place_names()
inverse_dlh_d_place_names = invert_dictionary(dlh_d_place_names)


dlh_data = extract_ner_annotation(get_dlh_sentences(dlh_books),
                                  [dict(label="PERSON", d=inverse_dlh_d_person_names),
                                   dict(label="LOC", d=inverse_dlh_d_place_names)])
save_serializable_data(dlh_data, "dlh_ner_data.json")
# endregion


# region Völsunga
def get_vol_sentences(book):
    vol_sentences = []
    for chapter in book:
        for paragraph in chapter:
            for tokenized_sentence in paragraph:
                vol_sentences.append(tokenized_sentence)
    return vol_sentences


vol_text = get_volsunga_text()

vol_d_person_names = get_volsunga_annotated_names()
inverse_vol_d_person_names = invert_dictionary(vol_d_person_names)

vol_d_place_names = get_volsunga_annotated_places()
inverse_vol_d_place_names = invert_dictionary(vol_d_place_names)

vol_d_group_names = get_volsunga_annotated_groups()
inverse_vol_d_group_names = invert_dictionary(vol_d_group_names)

vol_data = extract_ner_annotation(get_vol_sentences(vol_text),
                                  [dict(d=inverse_vol_d_person_names, label="PERSON"),
                                   dict(d=inverse_vol_d_place_names, label="LOC"),
                                   dict(d=inverse_vol_d_group_names, label="")])
save_serializable_data(vol_data, "vol_ner_data.json")
# print(vol_data)
# endregion


# region Niebelungenlied
def get_nib_sentences(book):
    nib_sentences = []
    for chapter in book:
        for tokenized_sentence in chapter:
            nib_sentences.append(tokenized_sentence)
    return nib_sentences


nib_book = get_nibelungen_book()

nib_d_person_names = get_nibelungenlied_annotated_names()
inverse_nib_d_person_names = invert_dictionary(nib_d_person_names)

nib_d_place_names = get_nibelungenlied_annotated_places()
inverse_nib_d_place_names = invert_dictionary(nib_d_place_names)

nib_d_group_names = get_nibelungenlied_annotated_groups()
inverse_nib_d_group_names = invert_dictionary(nib_d_group_names)

nib_data = extract_ner_annotation(get_nib_sentences(nib_book),
                                  [dict(d=inverse_nib_d_person_names, label="PERSON"),
                                   dict(d=inverse_nib_d_place_names, label="LOC"),
                                   dict(d=inverse_nib_d_group_names, label="")
                                   ])
save_serializable_data(nib_data, "nib_ner_data.json")
# endregion
