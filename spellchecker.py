from typing import List


class SpellChecker:
    def __init__(self, algorithm='edit_distance') -> None:

        if algorithm == 'edit_distance':
            self.get_score = self.edit_distance

        elif algorithm == 'edit_distance_recursive':
            self.get_score = self.edit_distance_recursive


    def edit_distance(self, word1: str, word2: str,
                      a=-1, b=-1, memory: List[List[int]]=[]) -> int:
        if a == -1:
            a = len(word1)
        if b == -1:
            b = len(word2)

        if a == 0:
            return b

        if b == 0:
            return a

        if not memory:
            memory = [[-1 for _ in range(b+1)] for _ in range(a+1)]

        if word1[a-1] == word2[b-1]:
            if memory[a][b] != -1:
                memory[a][b] = memory[a-1][b-1]
                return memory[a][b]

            else:
                memory[a][b] = self.edit_distance(word1, word2, a-1, b-1, memory)
                return memory[a][b]
       
        if memory[a][b] != -1:
            return memory[a][b]

        best_case = min(self.edit_distance(word1, word2, a-1, b, memory) if (x:=memory[a-1][b])==-1 else x,
                        self.edit_distance(word1, word2, a, b-1, memory) if (x:=memory[a][b-1])==-1 else x,
                        self.edit_distance(word1, word2, a-1, b-1, memory) if (x:=memory[a-1][b-1])==-1 else x)
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

        if word1[a-1] == word2[b-1]:
            return self.edit_distance_recursive(word1, word2, a-1, b-1)

        best_case = min(self.edit_distance_recursive(word1, word2, a-1, b),
                        self.edit_distance_recursive(word1, word2, a, b-1),
                        self.edit_distance_recursive(word1, word2, a-1, b-1))

        return 1 + best_case

    
