from spell_checker.spellchecker import SpellChecker
from spell_checker.dictionary import Dictionary
from spell_checker.utils import benchmark


dct = Dictionary()
dct.add_from_file('dictionaries/english.txt')

sc = SpellChecker('edit_distance_dp', dct)


@benchmark
def suggest(word):
    distances = sc.brute_force(word)
    top = sc.find_top(distances, 10)
    return top


@benchmark
def fast(word):
    distances = sc.slice_n_check(word)
    return list(distances.items())[:10]


if __name__ == '__main__':
    t, top = suggest('hallow')
    print(f'took {t:.2f}ms')
    print(top)
    t, top = fast('hallow')
    print(f'took {t:.2f}ms')
    print(top)
