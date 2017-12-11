"""http://bit.ly/openwest-py-17
https://www.gutenberg.org/ebooks/74

REPL - Read, evaluate, print, loop
PEP 8 - Conventions for Python coding

This module helps create Markov Chains

>>> m = Markov('ab')
>>> m.predict('a')
'b'
>>> m.predict('c')
Traceback (most recent call last):
...
KeyError: 'c'

>>> get_table('ab')
{'a': {'b': 1}}

>>> random.seed(42)
>>> m2 = Markov('Find a city, find yourself a city to live in')
>>> m2.predict('c')
'i'
>>> m2.predict('i')
'n'
>>> m2.predict('t')
'o'

>>> test_predict(m2, 'c')
'cind a ty, citourse f'


>>> m3 = Markov('Find a city, find yourself a city to live in', 3)
>>> m3.predict('cit')
'y'

"""
import argparse
import random
import sys
# import urllib.request as req
# fin = req.urlopen('https://www.gutenberg.org/files/74/74-0.txt')
# data = fin.read()
# type(data)
# data[:100]
# with open('/tmp/ts.txt', 'wb') as fout:
#   fout.write(data)
# ts = open('/tmp/ts.txt')
# print(ts[0:100])
# >>> import locale
# >>> locale.getpreferredencoding(False)
# with open('/tmp/ts.txt', encoding='windows_1252') as fin:
#	ts2 = fin.read()
# with open('/tmp/ts.txt', encoding='utf8') as fin:
#	ts2 = fin.read()
# m4 = Markov(ts, 4)

# This is a comment

# CamelCase classes in Python for PEP 8
# dunder init == __init__ => dunder (double under)
#   This is the constructor of the class
#   This is the magic under Python
class Markov:
    def __init__(self, data, size=1):
        # self.table = get_table(data)
        self.tables = []
        for i in range(size):
            self.tables.append(get_table(data, i+1))


    def predict(self, data_in):
        table = self.tables[len(data_in)-1]
        options = table[data_in]
        possible = ''
        for key, count in options.items():
            possible += key*count
        return random.choice(possible)

def test_predict(m2, start, numchars=1):
    res = [start]
    for i in range(20):
        let = m2.predict(start)
        res.append(let)
        start = ''.join(let[-numchars:])
    return ''.join(res)

def get_table(line, numchars=1):
    """
    >>> get_table('mambma')
    {'m': {'a': 2, 'b': 1}, 'a': {'m': 1}, 'b': {'m': 1}}
    """
    result = {}
    for i, _ in enumerate(line):
        chars = line[i: i+numchars]
        try:
            next_char = line[i+numchars]
        except IndexError:
            break
        char_dict = result.get(chars, {})
        char_dict.setdefault(next_char,0)
        char_dict[next_char] += 1
        # print(char)
        result[chars] = char_dict
    return result
    # return {'a': {'b': 1}}

def repl(m):
    while 1:
        try:
            txt = input(">")
        except KeyboardInterrupt:
                break
        res = m.predict(txt)
        print(res)


# name = 'matt'
# print(name)
# print(name[::-1])

def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--file', help='Input file')
    p.add_argument('-s', '--size', help='Markov size', default=1, type=int)
    p.add_argument('--encoding', help='File encoding', defualt='utf8')
    p.add_argument('-t', '--test')
    opt = p.parse_args(args)
    if opt.file:
        with open(opt.file, encoding=opt.encoding) as fin:
            data = fin.read()
            m = Markov(data, size=opt.size)
            repl(m)
    elif opt.test:
        import doctest
        doctest.testmod()
        #>>> help(doctest.testmod)
        # looks like this is using the comments at the top to test the script


if __name__ == '__main__':
    # When we are executing this file
    main(sys.argv[1:])
else:
    print('not running')
