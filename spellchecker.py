from typing import List
from dictionary import Dictionary
from string import ascii_lowercase

import operator


class SpellChecker:
    def __init__(self, algorithm='edit_distance', dictionary: Dictionary | None = None) -> None:

        if algorithm == 'edit_distance':
            self.get_score = self.edit_distance

        elif algorithm == 'edit_distance_recursive':
            self.get_score = self.edit_distance_recursive

        elif algorithm == 'edit_distance_dp':
            self.get_score = self.edit_distance_dp

        if dictionary:
            self.dictionary = dictionary
        else:
            dct = Dictionary()
            dct.add_from_file('dictionaries/english.txt')
            self.dictionary = dct

    def edit_distance(self, word1: str, word2: str,
                      a=-1, b=-1, memory: List[List[int]] = []) -> int:
        if a == -1:
            a = len(word1)
        if b == -1:
            b = len(word2)

        if not memory:
            memory = [[-1 for _ in range(b + 1)] for _ in range(a + 1)]

        if a == 0:
            memory[a][b] = b
            return b

        if b == 0:
            memory[a][b] = a
            return a

        if memory[a][b] != -1:
            return memory[a][b]

        if word1[a - 1] == word2[b - 1]:
            if memory[a][b] != -1:
                memory[a][b] = memory[a - 1][b - 1]
                return memory[a][b]

            else:
                memory[a][b] = self.edit_distance(word1, word2, a - 1, b - 1, memory)
                return memory[a][b]

        best_case = min(self.edit_distance(word1, word2, a - 1, b, memory) if (x := memory[a - 1][b]) == -1 else x,
                        self.edit_distance(word1, word2, a, b - 1, memory) if (x := memory[a][b - 1]) == -1 else x,
                        self.edit_distance(word1, word2, a - 1, b - 1, memory)
                        if (x := memory[a - 1][b - 1]) == -1 else x)
        memory[a][b] = 1 + best_case

        return 1 + best_case

    def edit_distance_recursive(self, word1: str, word2: str,
                                a=-1, b=-1) -> int:
        if a == -1:
            a = len(word1)
        if b == -1:
            b = len(word2)

        if a == 0:
            return b

        if b == 0:
            return a

        if word1[a - 1] == word2[b - 1]:
            return self.edit_distance_recursive(word1, word2, a - 1, b - 1)

        best_case = min(self.edit_distance_recursive(word1, word2, a - 1, b),
                        self.edit_distance_recursive(word1, word2, a, b - 1),
                        self.edit_distance_recursive(word1, word2, a - 1, b - 1))

        return 1 + best_case

    def edit_distance_dp(self, word1, word2):
        a = len(word1)
        b = len(word2)

        dp = [[0 for _ in range(b + 1)] for _ in range(a + 1)]

        for i in range(a + 1):
            for j in range(b + 1):
                if i == 0 or j == 0:
                    dp[i][j] = max(i, j)
                    continue

                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[a][b]

    @staticmethod
    def find_top(dct: dict[str, int], n=10) -> List[tuple]:
        '''
        Takes a dictionary and returns n items with biggest values
        '''
        sorted_list = sorted(dct.items(), key=operator.itemgetter(1))
        return sorted_list[:n]

    def brute_force(self, word: str):
        distances = {}
        for w in self.dictionary.iterate_all():
            distances[w] = self.get_score(word, w)

        return distances

    def slice_n_check(self, word: str):
        length = len(word)
        slices = [[word[:i], word[i:]] for i in range(length)]

        insertions = {slice[0] + c + slice[1] for slice in slices for c in ascii_lowercase}
        deletions = {word[:i] + word[i + 1:] for i in range(length)}
        replaces = {word[:i] + c + word[i + 1:] for i in range(length) for c in ascii_lowercase}

        print(len(insertions.union(deletions).union(replaces)))
        distances = {}
        for w in insertions.union(deletions).union(replaces):
            if not self.dictionary.find_word(w):
                continue
            distances[w] = 1  # we know cause we made it 1

        return distances
