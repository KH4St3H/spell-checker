from spellchecker import SpellChecker
from dictionary import Dictionary
from utils import benchmark


dct = Dictionary()
dct.add_from_file('dictionaries/english.txt')

sc = SpellChecker('edit_distance_dp', dct)


@benchmark
def suggest(word):
    distances = sc.brute_force(word)
    top = sc.find_top(distances, 10)
    return top

if __name__ == '__main__':
    t, top = suggest('hallow')
    print(f'took {t:.2f}s')
    print(top)
