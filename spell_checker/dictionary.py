from multiprocessing.dummy import Pool as ThreadPool

import logging


class Node:
    def __init__(self, letter) -> None:
        self.letter = letter
        self.word = None
        self.subs = {}

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, str):
            return __value == self.letter

        return False

    def addsub(self, word, level=0) -> None:
        if level == len(word):
            self.word = word
            return

        letter = word[level]
        if letter not in self.subs:
            self.subs[letter] = Node(letter)

        self.subs[letter].addsub(word, level + 1)

    def find_word(self, word, level=0):
        if level == len(word):
            return word == self.word

        letter = word[level]
        if letter in self.subs:
            return self.subs[letter].find_word(word, level + 1)

        return False

    def __str__(self) -> str:
        return self.word if self.word else self.letter

    def __repr__(self) -> str:
        return str(self)


class Dictionary:
    def __init__(self, thread_count=10) -> None:
        self.starting_node = Node('')
        self.threads = thread_count

    def add_word(self, new_word):
        self.starting_node.addsub(new_word)

    def find_word(self, word):
        return self.starting_node.find_word(word)

    def check_words(self, words: list[str]) -> list[bool]:
        pool = ThreadPool(self.threads)
        results = pool.map(self.find_word, words)
        pool.close()
        pool.join()
        return results

    def add_from_file(self, path):
        logging.info(f'Reading words from "{path}"')
        with open(path, 'r') as file:
            for d, word in enumerate(file.readlines()):
                self.add_word(word[:-1])
                if d % 1000 == 0:
                    logging.info(f"Read {d} lines from file")

    def iterate_all(self):
        stack = [self.starting_node]
        while stack:
            current_node = stack.pop()
            if current_node.word:
                yield current_node.word
            for node in current_node.subs.values():
                if node.subs:
                    stack.append(node)
                elif node.word:
                    yield node.word


if __name__ == '__main__':
    dct = Dictionary()
    dct.add_from_file('dictionaries/english.txt')

    print(dct.find_word('hello'))
    print(dct.find_word('hell'))
    print(dct.find_word('hero'))
    print(dct.find_word('helo'))
    print(dct.find_word('simpsonss'))
