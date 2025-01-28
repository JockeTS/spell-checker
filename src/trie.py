""" Module for Trie class. """

from src.node import Node
from src.errors import SearchMiss

class Trie():
    """ Trie class. """
    default_dict = "static/frequency.txt"

    def __init__(self, word_list=None):
        """ Constructor. """

        self.root = None

        if word_list:
            for item in word_list:
                word, freq = item.split()
                self.add_word(word, freq)

    @classmethod
    def create_from_file(cls):
        """ Create new trie object populated with words from file. """

        with open(file=Trie.default_dict, mode="r", encoding="utf-8") as fd:

            word_list = [line.rstrip("\n") for line in fd.readlines()]

        return cls(word_list)

    def add_word(self, word, freq=1):
        """ Add a new word. """

        if self.root is None:
            self.root = Node()

        self._add_letter(self.root, word, freq)

    @classmethod
    def _add_letter(cls, node, word, freq, index=0):
        """ Add node representing a letter. """

        if index >= len(word):
            node.is_stop = True
            node.freq = freq
            return

        letter = word[index]

        # If node doesn't have node with current letter as child, create new node
        if not node.children.get(letter):
            new_node = Node(letter)
            node.children[letter] = new_node

        next_node = node.children.get(letter)

        cls._add_letter(next_node, word, freq, index + 1)

    def remove_word(self, word):
        """ Remove a word from trie. """

        if self.root is None or not self.root.children.get(word[0]):
            raise SearchMiss

        node = self.root.children.get(word[0])

        remove = self._remove_letter(node, word)

        if remove:
            self.root.children.pop(node.key)

    @classmethod
    def _remove_letter(cls, node, word, index=0, remove=True):
        """ Remove child node if appropriate. """

        if index >= len(word) - 1:
            if node.key != word[index] or not node.is_stop:
                raise ValueError

            node.is_stop = False

            if len(node.children) > 0:
                remove = False

            return remove

        if not node.children.get(word[index + 1]):
            raise SearchMiss

        next_node = node.children.get(word[index + 1])

        remove = cls._remove_letter(next_node, word, index + 1, remove)

        if remove:
            node.children.pop(next_node.key)

        if node.is_stop or len(node.children) >= 1:
            remove = False

        return remove

    def has_word(self, word):
        """ Check if trie contains word. """

        if self.root is None:
            raise SearchMiss

        return self._has_letter(self.root, word)

    @classmethod
    def _has_letter(cls, node, word, index=0):
        """ Check if letter exists at index. """

        letter = word[index]

        if not node.children.get(letter):
            raise SearchMiss

        if index >= len(word) - 1:
            if node.children.get(letter).is_stop:
                return True

            raise SearchMiss

        node = node.children[letter]

        return cls._has_letter(node, word, index + 1)

    def get_num_words(self):
        """ Return number of words in trie. """

        if self.root is None:
            return 0

        return self._count_words(self.root)

    @classmethod
    def _count_words(cls, node, count=0):
        """ Count stop nodes. """

        if node.is_stop:
            count += 1

        if len(node.children) == 0:
            return count

        for child in node.children.values():
            count = cls._count_words(child, count)

        return count

    def get_all_words(self):
        """ Return a list with all words in trie. """

        word_list = []

        self._append_word(self.root, word_list)

        return word_list

    @classmethod
    def _append_word(cls, node, lst, word=""):
        """ Append word to list. """

        if node.key:
            word += node.key

        if node.is_stop:
            lst.append(word)

        if len(node.children) == 0:
            return

        for child in node.children.values():
            cls._append_word(child, lst, word)

    def prefix_search(self, prefix):
        """ Return all words starting with prefix. """

        word_list = []

        if self.root is None:
            return word_list

        node = self.root

        for letter in prefix:
            if not node.children.get(letter):
                return word_list

            node = node.children.get(letter)

        self._prefix_search(node, word_list, prefix[:-1])

        def freq_sort(e):
            return float(e[1])

        word_list.sort(reverse=True, key=freq_sort)

        if len(word_list) > 10:
            word_list = word_list[:10]

        return word_list

    @classmethod
    def _prefix_search(cls, node, lst, word=""):
        """ Return all words starting with prefix (rec). """

        word += node.key

        if node.is_stop:
            lst.append((word, float(node.freq)))

        if len(node.children) == 0:
            return

        for child in node.children.values():
            cls._prefix_search(child, lst, word)

    def correct_spelling(self, input_word):
        """ * """

        if self.root is None:
            return []

        suggs = []

        try:
            self.has_word(input_word)
            suggs.append(input_word)
        except SearchMiss:
            # Input word is not in trie
            self._correct_spelling(self.root, suggs, input_word)

        suggs.sort()

        return suggs

    @classmethod
    def _correct_spelling(cls, node, suggs, input_word, current_word="", wrong=False):
        """ Give word suggestions based on input. """

        if len(current_word) == len(input_word):
            return

        if node.key:
            current_word += node.key

            if input_word[len(current_word) - 1] != current_word[-1]:
                if wrong:
                    return

                wrong = True
            else:
                wrong = False

        if node.is_stop and len(current_word) == len(input_word):
            if current_word[-1] == input_word[-1]:
                suggs.append(current_word)

        if len(node.children) == 0:
            return

        for child in node.children.values():
            cls._correct_spelling(child, suggs, input_word, current_word, wrong)

    def suffix_search(self, suffix):
        """ Return words with matching suffix. """

        if self.root is None:
            return []

        node = self.root
        lst = []

        self._suffix_search(node, suffix, lst)

        lst.sort()

        return lst

    @classmethod
    def _suffix_search(cls, node, suffix, lst, suffix_index=0, word=""):
        """ Return words with matching suffix (rec). """

        if node.key:
            word += node.key

            # Check if node key matches current letter in suffix
            if node.key == suffix[suffix_index]:

                # Check if current letter is the last in suffix
                if suffix_index == len(suffix) - 1:
                    # Add word to list if node is stop
                    if node.is_stop:
                        #print("adding to list: ", word)
                        lst.append(word)
                    # Reset suffix index
                    suffix_index = 0
                else:
                    suffix_index += 1
            else:
                suffix_index = 0

        # Return if node is leaf
        if len(node.children) == 0:
            return

        for child in node.children.values():
            cls._suffix_search(child, suffix, lst, suffix_index, word)

if __name__ == "__main__":
    trie = Trie.create_from_file()
