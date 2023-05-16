

from collections import defaultdict
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


def add_found_items(sentence: str, tokenized_sentence: List[str], inverse_dictionary: Dict[str, List[str]]):
    l = []
    for i in inverse_dictionary:
        if i in tokenized_sentence:

            if i:
                start = sentence.index(i)
                end = start + len(i)
                # vol_data[" ".join(tokenized_sentence)]\
                l.append(dict(token=i, lemma=inverse_dictionary[i], start=start, end=end))
            else:
                # print(repr(i), inverse_dictionary[name])
                pass
    return l


def extract_ner_annotation(sentences: List[List[str]], inverse_dictionaries: List[Dict[str, List[str]]]):
    data = defaultdict(list)
    for inverse_d in inverse_dictionaries:
        for tokenized_sentence in sentences:
            sentence = " ".join(tokenized_sentence)
            item = add_found_items(sentence, tokenized_sentence, inverse_d)
            if item:
                data[sentence].extend(item)
    return data


# region DLH
dlh_books = extract_parsed_dlh_books()

dlh_d_person_names = get_lemmatised_dlh_person_names()
inverse_dlh_d_person_names = invert_dictionary(dlh_d_person_names)
# print(dlh_d_person_names)
# print(inverse_dlh_d_person_names)
# person_names = {name for i in d_person_names for name in i}
dlh_d_place_names = get_lemmatised_dlh_place_names()
inverse_dlh_d_place_names = invert_dictionary(dlh_d_place_names)
# print(inverse_dlh_d_place_names)

dlh_sentences = []
for book in dlh_books:
    for chapter in book:
        for tokenized_sentence in chapter:
            dlh_sentences.append(tokenized_sentence)

dlh_data = extract_ner_annotation(dlh_sentences, [inverse_dlh_d_person_names, inverse_dlh_d_place_names])
# dlh_data = defaultdict(list)
# for tokenized_sentence in dlh_sentences:
#     for name in inverse_dlh_d_person_names:
#         if name in tokenized_sentence:
#             if name:
#                 dlh_data[" ".join(tokenized_sentence)].append(dict(token=name, lemma=inverse_dlh_d_person_names[name]))
#             else:
#                 print(repr(name), inverse_dlh_d_person_names[name])
#
#     for place in inverse_dlh_d_place_names:
#         if place in tokenized_sentence:
#             if place:
#                 dlh_data[" ".join(tokenized_sentence)].append(dict(lemma=inverse_dlh_d_place_names[place], token=place))
#             else:
#                 print(repr(place), inverse_dlh_d_place_names[place])


# endregion


# region Völsunga
vol_text = get_volsunga_text()
# print(vol_text)
# print(len(vol_text))
# print(len(vol_text[0]))

vol_sentences = []
for chapter in vol_text:
    for paragraph in chapter:
        for tokenized_sentence in paragraph:
            vol_sentences.append(tokenized_sentence)
# print(vol_sentences)

vol_d_person_names = get_volsunga_annotated_names()
inverse_vol_d_person_names = invert_dictionary(vol_d_person_names)
# print(vol_d_person_names)
# print(inverse_vol_d_person_names)

vol_d_place_names = get_volsunga_annotated_places()
inverse_vol_d_place_names = invert_dictionary(vol_d_place_names)
# print(inverse_vol_d_place_names)

vol_d_group_names = get_volsunga_annotated_groups()
inverse_vol_d_group_names = invert_dictionary(vol_d_group_names)
# print(inverse_vol_d_group_names)

vol_data = extract_ner_annotation(vol_sentences,
                                  [inverse_vol_d_person_names,
                                   inverse_vol_d_place_names,
                                   inverse_vol_d_group_names])
# vol_data = defaultdict(list)
# for tokenized_sentence in vol_sentences:
#     sentence = " ".join(tokenized_sentence)
#     vol_data[sentence].extend(add_found_items(tokenized_sentence, inverse_vol_d_person_names))
#     vol_data[sentence].extend(add_found_items(tokenized_sentence, inverse_vol_d_place_names))
#     vol_data[sentence].extend(add_found_items(tokenized_sentence, inverse_vol_d_group_names))

# for name in inverse_vol_d_person_names:
#     if name in sentence:
#         if name:
#             vol_data[" ".join(sentence)].append(dict(token=name, lemma=inverse_vol_d_person_names[name]))
#         else:
#             print(repr(name), inverse_vol_d_person_names[name])

# for place in inverse_vol_d_place_names:
#     if place in tokenized_sentence:
#         if place:
#             vol_data[" ".join(tokenized_sentence)].append(dict(lemma=inverse_vol_d_place_names[place], token=place))
#         else:
#             print(repr(place), inverse_vol_d_place_names[place])
# for group in inverse_vol_d_group_names:
#     if group in tokenized_sentence:
#         if group:
#             vol_data[" ".join(tokenized_sentence)].append(dict(lemma=inverse_vol_d_place_names[group], token=group))
#         else:
#             print(repr(group), inverse_vol_d_place_names[group])
print(vol_data)
# endregion

# region Niebelungenlied
nib_book = get_nibelungen_book()
# print(nib_book)
nib_sentences = []
for chapter in nib_book:
    for tokenized_sentence in chapter:
        vol_sentences.append(tokenized_sentence)


nib_d_person_names = get_nibelungenlied_annotated_names()
inverse_nib_d_person_names = invert_dictionary(nib_d_person_names)
# print(nib_d_person_names)
# print(inverse_nib_d_person_names)

nib_d_place_names = get_nibelungenlied_annotated_places()
inverse_nib_d_place_names = invert_dictionary(nib_d_place_names)
# print(inverse_nib_d_place_names)

nib_d_group_names = get_nibelungenlied_annotated_groups()
inverse_nib_d_group_names = invert_dictionary(nib_d_group_names)
# print(inverse_nib_d_group_names)


nib_data = extract_ner_annotation(nib_sentences, [inverse_nib_d_person_names,
                                                  inverse_nib_d_place_names,
                                                  inverse_nib_d_group_names
                                                  ])
# nib_data = defaultdict(list)
# for tokenized_sentence in nib_sentences:
#     sentence = " ".join(tokenized_sentence)
#     nib_data[sentence].extend(add_found_items(tokenized_sentence, inverse_nib_d_person_names))
#     nib_data[sentence].extend(add_found_items(tokenized_sentence, inverse_nib_d_place_names))
#     nib_data[sentence].extend(add_found_items(tokenized_sentence, inverse_nib_d_group_names))

# for name in inverse_nib_d_person_names:
#     if name in tokenized_sentence:
#         if name:
#             nib_data[" ".join(tokenized_sentence)].append(dict(token=name, lemma=inverse_nib_d_person_names[name]))
#         else:
#             print(repr(name), inverse_nib_d_person_names[name])

# for place in inverse_nib_d_place_names:
#     if place in tokenized_sentence:
#         if place:
#             nib_data[" ".join(tokenized_sentence)].append(dict(lemma=inverse_nib_d_place_names[place], token=place))
#         else:
#             print(repr(place), inverse_nib_d_place_names[place])

# for group in inverse_nib_d_group_names:
#     if group in tokenized_sentence:
#         if group:
#             nib_data[" ".join(tokenized_sentence)].append(dict(lemma=inverse_nib_d_place_names[group], token=group))
#         else:
#             print(repr(group), inverse_nib_d_place_names[group])
# print(nib_data)
# endregion
