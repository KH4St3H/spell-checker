import unittest
from spell_checker.spellchecker import SpellChecker


class BaseTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.spellchecker = SpellChecker('edit_distance_dp')

    def score_check(self, args, value):
        self.assertEqual(self.spellchecker.get_score(*args), value)


class TestEditDistance(BaseTestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super(TestEditDistance, self).__init__(methodName)
        self.spellchecker = SpellChecker('edit_distance_recursive')

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

        a = 'asset'
        b = 'ascent'
        self.score_check((a, b), 2)

    def test_long(self):
        a = 'keratinkera'
        b = 'eratinkerat'
        self.score_check((a, b), 2)


class TestEditDistanceRecursive(TestEditDistance):
    def __init__(self, methodName: str = "runTest") -> None:
        super(TestEditDistance, self).__init__(methodName)
        self.spellchecker = SpellChecker('edit_distance_recursive')


class TestEditDistanceDP(TestEditDistance):
    def __init__(self, methodName: str = "runTest") -> None:
        super(TestEditDistance, self).__init__(methodName)
        self.spellchecker = SpellChecker('edit_distance_dp')


class TestEditDistanceSplit(BaseTestCase):
    def test_edit_distance_1(self):
        original_word = 'excase'
        for word, edit_distance in self.spellchecker.slice_n_check(original_word).items():
            self.assertEqual(edit_distance, 1)  # making sure edit distance is 1
            self.score_check((original_word, word), 1)

        original_word = 'pleaxe'
        for word, edit_distance in self.spellchecker.slice_n_check(original_word).items():
            self.assertEqual(edit_distance, 1)
            self.score_check((original_word, word), 1)

    def test_edit_distance_2(self):
        """
        find words with edit_distance <= 2
        """
        original_word = 'prooress'
        for word, edit_distance in self.spellchecker.slice_n_check(original_word, 2).items():
            self.score_check((original_word, word), edit_distance)

        original_word = 'assent'
        for word, edit_distance in self.spellchecker.slice_n_check(original_word, 2).items():
            self.score_check((original_word, word), edit_distance)


if __name__ == '__main__':
    unittest.main()
