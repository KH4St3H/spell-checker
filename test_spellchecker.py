import unittest
from spellchecker import SpellChecker


class TestEditDistance(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.spellchecker = SpellChecker('edit_distance')

    def score_check(self, args, value):
        self.assertEqual(self.spellchecker.get_score(*args), value)

    def test_equal(self):
        a = 'hello'
        b = 'hello'
        self.score_check((a, b), 0)

    def test_append(self):
        a = 'pick'
        b = 'picky'
        self.score_check((a, b), 1)

        a = 'candid'
        b = 'candidate'
        self.score_check((a, b), 3)

    def test_remove(self):
        a = 'loser'
        b = 'lose'
        self.score_check((a, b), 1)

    def test_change(self):
        a = 'duck'
        b = 'luck'
        self.score_check((a, b), 1)

    def test_complex(self):
        a = 'loser'
        b = 'lost'
        # test change + add
        self.score_check((a, b), 2)

    def test_long(self):
        a = 'keratinkera'
        b = 'eratinkerat'
        self.score_check((a, b), 2)


class TestEditDistanceRecursive(TestEditDistance):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.spellchecker = SpellChecker('edit_distance_recursive')


if __name__ == '__main__':
    unittest.main()

