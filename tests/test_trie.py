#!/usr/bin/env python3
#pylint: disable=protected-access

""" Module for testing class Trie. """

import unittest
from src.trie import Trie
from src.errors import SearchMiss

class TestTrie(unittest.TestCase):
    """ Submodule for unit tests, inherits from unittest.TestCase. """

    def setUp(self):
        """ Standard setup before every test case is run. """
        # Arrange
        self.trie = Trie.create_from_file()

    def tearDown(self):
        """ Clean up after every test case. """
        self.trie = None

    def test_create_from_file(self):
        """ Test that create_from_file works as expected. """

        self.assertEqual(self.trie.get_num_words(), 25402)

        self.assertTrue(self.trie.has_word("many"))
        self.assertTrue(self.trie.has_word("between"))
        self.assertTrue(self.trie.has_word("together"))

    def test_create_empty(self):
        """ Test creating empty trie. """

        trie2 = Trie()
        self.assertEqual(trie2.get_num_words(), 0)

        with self.assertRaises(SearchMiss) as _:
            trie2.has_word("many")
            trie2.has_word("between")
            trie2.has_word("together")

    def test_add_word(self):
        """ Test adding a new word. """

        with self.assertRaises(SearchMiss) as _:
            self.trie.has_word("moonwalk")

        self.trie.add_word("moonwalk")

        self.assertTrue(self.trie.has_word("moonwalk"))

    def test_remove_existing_word(self):
        """ Test removing existing word from trie. """

        self.assertTrue(self.trie.has_word("understand"))

        self.trie.remove_word("understand")

        with self.assertRaises(SearchMiss) as _:
            self.trie.has_word("understand")

    def test_remove_non_existing_word(self):
        """ Test removing a word not in trie. """

        with self.assertRaises(SearchMiss) as _:
            self.trie.remove_word("moonwalk")

    def test_get_all_words(self):
        """ Test getting list of all words. """

        wrd_lst = self.trie.get_all_words()

        self.assertEqual(len(wrd_lst), 25402)

        self.assertEqual(wrd_lst[0], "that")
        self.assertEqual(wrd_lst[12000], "cervix")
        self.assertEqual(wrd_lst[-1], "xhosa")

    def test_prefix_search(self):
        """ Test that prefix search returns expected results. """

        wrd_lst = self.trie.prefix_search("ba")

        ctl_lst = [('back', 740270.0), ('battle', 108781.0), ('bank', 66981.4),
                   ('based', 46717.2), ('bare', 46386.5), ('base', 39900.8),
                   ('band', 39397.7), ('ball', 39180.9), ('banks', 37623.1),
                   ('baby', 37208.6)]

        self.assertEqual(wrd_lst, ctl_lst)

    def test_prefix_search_no_matches(self):
        """ Test that a prefix search with no matches returns empty list. """

        self.assertEqual(self.trie.prefix_search("xyz"), [])
