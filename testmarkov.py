import unittest

from markov import CharIter, WordIter, char_gen, word_gen, window_gen
import markov as mar

class TestMarkov(unittest.TestCase):
    def test_table(self):
        lines = ['abc', 'def', 'hi']
        t = mar.get_table(char_gen(lines))
        # print(t)
        self.assertEqual(t, {'a': {'b': 1}, 'b': {'c': 1}, 'c': {'d': 1}, 'd': {'e': 1}, 'e': {'f': 1}, 'f': {'h': 1}, 'h': {'i': 1}})

    def test_table2(self):
        lines = ['abc', 'def', 'hi']
        t = mar.get_table(char_gen(lines), 2)
        # print(t)
        self.assertEqual(t, {'ab': {'c': 1}, 'bc': {'d': 1}, 'cd': {'e': 1}, 'de': {'f': 1}, 'ef': {'h': 1}, 'fh': {'i': 1}})


class TestCharIter(unittest.TestCase):
    def test_basic(self):
        ci = CharIter(['a', 'b'])
        it = iter(ci)
        item = next(it)
        self.assertEqual(item, 'a')
        item = next(it)
        self.assertEqual(item, 'b')

    def test_basic2(self):
        ci = CharIter(['a', 'b'])
        res = list(ci)
        self.assertEqual(res, ['a', 'b'])

    def test_gen(self):
        ci = char_gen(['a', 'b'])
        res = list(ci)
        self.assertEqual(res, ['a', 'b'])

class TestWordIter(unittest.TestCase):
    def test_basic(self):
        wi = WordIter(['A beautiful day', 'in the neighborhood'])
        res = list(wi)
        self.assertEqual(res, ['A', 'beautiful', 'day', 'in', 'the', 'neighborhood']) 

    def test_gen(self):
        wi = word_gen(['A beautiful day', 'in the neighborhood'])
        res = list(wi)
        self.assertEqual(res, ['A', 'beautiful', 'day', 'in', 'the', 'neighborhood']) 

class TestWindow(unittest.TestCase):
    def test_win(self):
        lines = ['hi there', 'name is matt']
        res = list(window_gen(word_gen(lines), 3))
        self.assertEqual(res, [['hi', 'there', 'name'],
                               ['there', 'name', 'is'],
                               ['name', 'is', 'matt'],
                               ['is', 'matt'],
                               ['matt']
                               ])

unittest.main()
