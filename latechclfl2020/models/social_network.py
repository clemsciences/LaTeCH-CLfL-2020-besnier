"""
Where social networks between texts are made.
"""
import itertools
import os
from typing import List, Dict
import networkx as nx
import matplotlib.pyplot as plt

from latechclfl2020 import utils, constants, PACKDIR
from latechclfl2020.models.languages import Language


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


class TextSocialNetwork(nx.Graph):

    def __init__(self, language=Language.latin):
        super().__init__(self)

        self.language = language
        self.text = None

        self.proper_nouns = []
        self.characters = []

        self.chapters = []

        self.chapter_directory = os.path.join(PACKDIR, "models", language.name)

    def load_text(self, text):
        self.text = text

    def load_proper_nouns(self, proper_nouns):
        self.proper_nouns = proper_nouns

    def load_character_names(self, character_names: Dict[str, List[str]]):
        self.characters = character_names

    @property
    def text_co_occurrences(self):
        """

        """
        if not self.characters:
            raise ValueError("Load character names")
        if not self.text:
            raise ValueError("Load text")

        possible_pairs = list(itertools.combinations(list(self.characters.keys()), 2))
        cooccurring = dict.fromkeys(possible_pairs, 0)
        return cooccurring

    @property
    def text_cooccurrences_by_chapter(self):
        """

        :return:
        """
        if not self.characters:
            raise ValueError("Load character names")
        if not self.text:
            raise ValueError("Load text")

        # possible_pairs = list(itertools.combinations(list(self.characters.keys()), 2))
        cooccurring = []
        return cooccurring

    def generate_graph_by_chapter(self, name):
        self.chapters = []
        for i, chapter_cooccurrences in enumerate(self.text_cooccurrences_by_chapter):
            chapter_graph = nx.Graph()
            for pair, weight in chapter_cooccurrences.items():
                chapter_graph.add_node(pair[0])
                chapter_graph.add_node(pair[1])
                if weight > 0:
                    chapter_graph.add_edge(pair[0], pair[1], weight=weight)
            self.chapters.append(chapter_graph)
            print(f"chapter {i + 1}")
            print(chapter_cooccurrences)
            pos = nx.spring_layout(chapter_graph, k=0.5, iterations=20)
            nx.draw(chapter_graph, node_color="gray", node_size=30, width=0.5,
                    edge_color="gray", with_labels=True, font_size=12, scale=2)
            plt.draw()

            if not os.path.exists(self.chapter_directory):
                os.mkdir(self.chapter_directory)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.png"), dpi=1000)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.pdf"))
            plt.clf()
        return self.chapters

    def generate_graph(self, name):
        self.name = name
        for pair, weight in self.text_co_occurrences.items():
            if weight > 1:
                self.add_edge(pair[0], pair[1], weight=weight)
        # ego_graph = nx.ego_graph(self, center)
        # edges, weights = zip(*nx.get_edge_attributes(ego_graph, "weight").items())
        #
        # pos = nx.spring_layout(ego_graph, k=0.5, iterations=40)
        # pos = nx.spring_layout(self, k=0.5, iterations=20)
        # nx.draw(self, pos=pos, node_color="gray", node_size=30, width=0.5,
        #         edge_color="gray", with_labels=True, font_size=5, scale=2)
        # plt.draw()
        # plt.savefig(f"{name}.png", dpi=1000)
        # plt.savefig(f"{name}.pdf")

    @property
    def text_occurrences(self):
        """

        """
        if not self.characters:
            raise ValueError("Load character names")
        if not self.text:
            raise ValueError("Load text")

        return dict.fromkeys(self.characters, 0)


class VolsungaSocialNetwork(TextSocialNetwork):
    def __init__(self):
        super().__init__(Language.old_norse)
        self.chapter_directory = os.path.join(PACKDIR, "models",
                                              constants.VOLSUNGA_GRAPHS_DIRECTORY)

    @property
    def text_co_occurrences(self):
        possible_pairs = list(itertools.combinations(list(self.characters.keys()), 2))
        cooccurring = dict.fromkeys(possible_pairs, 0)
        for chapter in self.text:
            for para in chapter:
                for sent in utils.partition(para, 5):
                    sent = [word for s in sent for word in s]
                    for pair in possible_pairs:
                        if utils.one_of_them_in(self.characters[pair[0]], sent) and utils.one_of_them_in(
                                self.characters[pair[1]], sent):
                            print(pair)
                            cooccurring[pair] += 1
        return cooccurring

    @property
    def text_cooccurrences_by_chapter(self):
        cooccurring_by_chapters = []
        for chapter in self.text:
            print("chapter")
            characters_present_in_chapter = set()
            # region where only characters present in current chapter are chosen
            tokens = [token for para in chapter for sent in para for token in sent]
            print(tokens[:5])
            for character in self.characters.keys():
                for character_inflected_form in self.characters[character]:
                    if character_inflected_form in tokens:
                        characters_present_in_chapter.add(character)
            # endregion
            possible_pairs = list(itertools.combinations(characters_present_in_chapter, 2))
            cooccurring = dict.fromkeys(possible_pairs, 0)
            for para in chapter:
                for sent in utils.partition(para, 5):
                    sent = [word for s in sent for word in s]
                    for pair in possible_pairs:
                        # print(sent, pair)
                        if utils.one_of_them_in(self.characters[pair[0]], sent) \
                                and utils.one_of_them_in(
                                self.characters[pair[1]], sent):
                            cooccurring[pair] += 1
            cooccurring_by_chapters.append(cooccurring)
        return cooccurring_by_chapters

    @property
    def text_occurrences(self):
        """

        """
        if not self.characters:
            raise ValueError("Load character names")
        if not self.text:
            raise ValueError("Load text")
        occurrences = super(VolsungaSocialNetwork, self).text_occurrences
        for character in self.characters:
            for chapter in self.text:
                for para in chapter:
                    for sent in para:
                        if utils.one_of_them_in(self.characters[character], sent):
                            occurrences[character] += 1
        return occurrences


class NibelungenliedSocialNetwork(TextSocialNetwork):
    def __init__(self):
        super().__init__(Language.middle_high_german)
        self.chapter_directory = os.path.join(PACKDIR, "models",
                                              constants.NIB_GRAPHS_DIRECTORY)

    @property
    def text_co_occurrences(self):
        possible_pairs = list(itertools.combinations(list(self.characters.keys()), 2))
        # print(possible_pairs)
        co_occurring = dict.fromkeys(possible_pairs, 0)
        for chapter in self.text:
            for para in utils.partition(chapter, 3*4):
                para = " ".join([" ".join(long_line) for long_line in para])
                for pair in possible_pairs:
                    if utils.one_of_them_in(self.characters[pair[0]], para) and \
                            utils.one_of_them_in(self.characters[pair[1]], para):
                        co_occurring[pair] += 1
        return co_occurring

    def generate_graph_by_chapter(self, name):
        self.chapters = []
        for i, chapter_cooccurrences in enumerate(self.text_cooccurrences_by_chapter):
            chapter_graph = nx.Graph()
            for pair, weight in chapter_cooccurrences.items():
                # chapter_graph.add_node(pair[0])
                # chapter_graph.add_node(pair[1])
                if weight > 0:
                    chapter_graph.add_edge(pair[0], pair[1], weight=weight)
            self.chapters.append(chapter_graph)
            print(f"chapter {i + 1}")
            print(chapter_cooccurrences)
            pos = nx.spring_layout(chapter_graph, k=0.5, iterations=20)
            nx.draw(chapter_graph, node_color="gray", node_size=30, width=0.5,
                    edge_color="gray", with_labels=True, font_size=5, scale=2)
            plt.draw()

            if not os.path.exists(self.chapter_directory):
                os.mkdir(self.chapter_directory)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.png"), dpi=1000)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.pdf"))
            plt.clf()
        return self.chapters

    @property
    def text_cooccurrences_by_chapter(self):
        cooccurring_by_chapters = []
        # print(len(self.text))
        # print(self.text)
        for chapter in self.text:
            # print("chapter")
            characters_present_in_chapter = set()
            # region where only characters present in current chapter are chosen
            tokens = [token for long_line in chapter for half_line in long_line for token in half_line.split(" ")]
            for character_lemma in self.characters:
                for character in self.characters[character_lemma]:
                    if character in tokens:
                        characters_present_in_chapter.add(character_lemma)
            # endregion
            possible_pairs = list(itertools.combinations(characters_present_in_chapter, 2))
            co_occurring = dict.fromkeys(possible_pairs, 0)
            for para in utils.partition(chapter, 4*3):  # this is the natural way to divide texts in
                para = " ".join([" ".join(long_line) for long_line in para])
                for pair in possible_pairs:
                    if utils.one_of_them_in(self.characters[pair[0]], para) \
                            and utils.one_of_them_in(
                            self.characters[pair[1]], para):
                        co_occurring[pair] += 1
            cooccurring_by_chapters.append(co_occurring)
        return cooccurring_by_chapters

    def generate_graph_by_chapter(self, name):
        self.chapters = []
        for i, chapter_cooccurrences in enumerate(self.text_cooccurrences_by_chapter):
            chapter_graph = nx.Graph()
            for pair, weight in chapter_cooccurrences.items():
                chapter_graph.add_node(pair[0])
                chapter_graph.add_node(pair[1])
                if weight > 0:
                    chapter_graph.add_edge(pair[0], pair[1], weight=weight)
            self.chapters.append(chapter_graph)
            print(f"chapter {i + 1}")
            print(chapter_cooccurrences)
            pos = nx.spring_layout(chapter_graph, k=0.5, iterations=20)
            nx.draw(chapter_graph, node_color="gray", node_size=30, width=0.5,
                    edge_color="gray", with_labels=True, font_size=10, scale=2)
            plt.draw()

            if not os.path.exists(self.chapter_directory):
                os.mkdir(self.chapter_directory)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.png"), dpi=1000)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.pdf"))
            plt.clf()
        return self.chapters

    @property
    def text_occurrences(self):
        """

        """
        if not self.characters:
            raise ValueError("Load character names")
        if not self.text:
            raise ValueError("Load text")
        occurrences = super(NibelungenliedSocialNetwork, self).text_occurrences
        for character in self.characters:
            for chapter in self.text:
                for para in utils.partition(chapter, 3 * 4):
                    para = " ".join([" ".join(long_line) for long_line in para])
                    if utils.one_of_them_in(self.characters[character], para):
                        occurrences[character] += 1
        return occurrences


class DLHSocialNetwork(TextSocialNetwork):
    def __init__(self):
        super().__init__(Language.latin)
        self.chapter_directory = os.path.join(PACKDIR,
                                              "models",
                                              constants.DLH_GRAPHS_DIRECTORY)

    @property
    def text_co_occurrences(self):
        possible_pairs = list(itertools.combinations(list(self.characters.keys()), 2))
        cooccurring = dict.fromkeys(possible_pairs, 0)
        for chapter in self.text:
            for para in chapter:
                for sent in utils.partition(para, 5):
                    sent = [word for s in sent for word in s]
                    for pair in possible_pairs:
                        if utils.one_of_them_in(self.characters[pair[0]], sent) and utils.one_of_them_in(
                                self.characters[pair[1]], sent):
                            cooccurring[pair] += 1
        return cooccurring

    @property
    def text_cooccurrences_by_chapter(self):
        cooccurring_by_chapters = []
        for book in self.text:
            print("chapter")
            characters_present_in_chapter = set()
            # region where only characters present in current chapter are chosen
            tokens = [token for para in book for sent in para for token in sent]
            print(tokens[:5])
            for character in self.characters.keys():
                for character_inflected_form in self.characters[character]:
                    if character_inflected_form in tokens:
                        characters_present_in_chapter.add(character)
            # endregion
            print(list(characters_present_in_chapter)[:5])
            possible_pairs = list(itertools.combinations(characters_present_in_chapter, 2))
            cooccurring = dict.fromkeys(possible_pairs, 0)
            for para in book:
                for sent in utils.partition(para, 5):
                    sent = [word for s in sent for word in s]
                    for pair in possible_pairs:
                        # print(sent, pair)
                        if utils.one_of_them_in(self.characters[pair[0]], sent) \
                                and utils.one_of_them_in(
                                self.characters[pair[1]], sent):
                            cooccurring[pair] += 1
            cooccurring_by_chapters.append(cooccurring)
        return cooccurring_by_chapters

    def generate_graph_by_chapter(self, name):
        self.chapters = []
        for i, chapter_cooccurrences in enumerate(self.text_cooccurrences_by_chapter):
            chapter_graph = nx.Graph()
            for pair, weight in chapter_cooccurrences.items():
                # chapter_graph.add_node(pair[0])
                # chapter_graph.add_node(pair[1])
                if weight > 0:
                    chapter_graph.add_edge(pair[0], pair[1], weight=weight)
            self.chapters.append(chapter_graph)
            print(f"chapter {i + 1}")
            print(chapter_cooccurrences)
            pos = nx.spring_layout(chapter_graph, k=0.5, iterations=20)
            nx.draw(chapter_graph, node_color="gray", node_size=30, width=0.5,
                    edge_color="gray", with_labels=True, font_size=5, scale=2)
            plt.draw()
            if not os.path.exists(self.chapter_directory):
                os.mkdir(self.chapter_directory)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.png"), dpi=1000)
            plt.savefig(os.path.join(self.chapter_directory, f"{name}_{i + 1}.pdf"))
            plt.clf()
        return self.chapters

    @property
    def text_occurrences(self):
        """

        """
        if not self.characters:
            raise ValueError("Load character names")
        if not self.text:
            raise ValueError("Load text")
        occurrences = super(DLHSocialNetwork, self).text_occurrences
        for character in self.characters:
            for book in self.text:
                for para in book:
                    for sent in para:
                        sent = [word for s in sent for word in s]
                        if utils.one_of_them_in(self.characters[character], sent):
                            occurrences[character] += 1
        return occurrences
