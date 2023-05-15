

from collections import defaultdict

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


# region DLH
books = extract_parsed_dlh_books()

d_person_names = get_lemmatised_dlh_person_names()
inverse_d_person_names = invert_dictionary(d_person_names)
print(d_person_names)
print(inverse_d_person_names)
# person_names = {name for i in d_person_names for name in i}
d_place_names = get_lemmatised_dlh_place_names()
inverse_d_place_names = invert_dictionary(d_place_names)
print(inverse_d_place_names)

dlh_sentences = []
for book in books:
    for chapter in book:
        for sentence in chapter:
            dlh_sentences.append(" ".join(sentence))

dlh_data = defaultdict(list)
for sentence in dlh_sentences:
    for name in inverse_d_person_names:
        if name in sentence:
            if name:
                dlh_data[sentence].append(dict(token=name, lemma=inverse_d_person_names[name]))
            else:
                print(repr(name), inverse_d_person_names[name])

    for place in inverse_d_place_names:
        if place in sentence:
            if place:
                dlh_data[sentence].append(dict(lemma=inverse_d_place_names[place], token=place))
            else:
                print(repr(place), inverse_d_place_names[place])


# endregion


# region Völsupaa
v_text = get_volsunga_text()
print(v_text)
vol_sentences = []
for chapter in v_text:
    for sentence in chapter:
        vol_sentences.append(" ".join(sentence))



# endregion

# region Niebelungenlied

# endregion
