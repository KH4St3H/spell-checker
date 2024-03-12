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

    def addsub(self, word, level=1) -> None:
        if level == len(word): 
            self.word = word
            return

        letter = word[level]
        if letter not in self.subs:
            self.subs[letter] = Node(letter)

        self.subs[letter].addsub(word, level+1)

    def find_word(self, word, level=1):
        if level == len(word):
            return word == self.word

        letter = word[level]
        if letter in self.subs:
            return self.subs[letter].find_word(word, level+1)
        
        return False


    def __str__(self) -> str:
        return self.word if self.word else self.letter

    def __repr__(self) -> str:
        return str(self)


class Dictionary:
    def __init__(self) -> None:
        self.starting_nodes = {}
        pass

    def add_word(self, new_word):
        letter = new_word[0] 
        if letter in self.starting_nodes:
            self.starting_nodes[letter].addsub(new_word)
        else:
            self.starting_nodes[letter] = Node(letter)

    def find_word(self, word):
        return self.starting_nodes[word[0]].find_word(word)

    def add_from_file(self, path):
        logging.info(f'Reading words from "{path}"')
        with open(path, 'r') as file:
            for d, word in enumerate(file.readlines()):
                self.add_word(word[:-1])
                if d % 1000 == 0:
                    logging.info(f"Read {d} lines from file")


if __name__ == '__main__':
    dct = Dictionary()
    dct.add_from_file('dictionaries/english.txt')

    print(dct.find_word('hello'))

