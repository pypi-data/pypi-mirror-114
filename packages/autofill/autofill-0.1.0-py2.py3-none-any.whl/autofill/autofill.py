"""Main module."""
from typing import Optional, List


class TrieNode:
    """ Node in Trie data structure """

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.counter = 0
        self.limit = None


def trie_factory():
    """Creates a trienode object"""
    return TrieNode()


class Trie:
    """Trie data structure"""

    def __init__(self):
        self.root = trie_factory()
        self.autocomplete_list = []
        self.top_k_list = []
        self.cur_word = None

    def build_trie(self, words: List) -> None:
        """Build Trie"""
        for word in words:
            self.insert(word)

    def insert(self, words: str) -> None:
        """Insert a word in to trie"""
        node = self.root
        # for word in words:
        for char in words:
            if char not in node.children:
                node.children[char] = trie_factory()
            node = node.children[char]

        node.is_end = True

    def _dfs(
        self,
        node: TrieNode,
        word: str,
        limit: Optional[int] = None,
        used_for: str = "autocomplete",
    ) -> None:
        """Depth first search on trie tree"""

        if limit is not None and used_for == "autocomplete":
            if len(self.autocomplete_list) == limit:
                return

        if node.is_end:
            if used_for == "autocomplete":
                node.counter += 1
                self.autocomplete_list.append(word)
            elif used_for == "top_k":
                self.top_k_list.append((word, node.counter))

        for char, _node in node.children.items():
            new_word = "".join([word, char])
            self._dfs(_node, new_word, limit, used_for)

    def search_prefix(self, word: str, limit: Optional[int] = None) -> List:
        """Search based on word prefix"""
        if self.cur_word == word:
            return self.autocomplete_list
        self.cur_word = word
        self.autocomplete_list = []
        node = self.root

        for char in word:
            if char not in node.children:
                return self.autocomplete_list
            node = node.children[char]

        self._dfs(node, word, limit)
        return self.autocomplete_list

    def top_matches(self, k: int = 10) -> List:
        """Return top k match words"""
        self.top_k_list = []
        self._dfs(self.root, "", used_for="top_k")
        self.top_k_list = sorted(self.top_k_list, key=lambda k: k[1], reverse=True)
        # result = [result[0] for result in self.top_k_list]
        return self.top_k_list[:k]


class Autocomplete(Trie):
    """Main class that do autocomplete"""
    def __init__(self):
        super().__init__()


_auto = Autocomplete()


def register_words(words: List):
    """Add list words to the autocomplete"""
    _auto.build_trie(words)


def search(word: str, limit: Optional[int] = None):
    """Prefix search a word"""
    return _auto.search_prefix(word, limit)


def find_top_k_matches(k: int = 10):
    """Find top k words from previous search matches"""
    return _auto.top_matches(k)


__all__ = ["register_words", "search", "find_top_k_matches"]

