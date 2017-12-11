"""http://bit.ly/openwest-py-17
http://www.gutenberg.org/ebooks/74

python3 -m idlelib.idle

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



"""
import argparse
import random
import sys

# This is a comment

class CharIter:
    def __init__(self, lines):
        self.data = iter(lines)
        self.line = None
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        while 1:
            if self.line is None:
                self.line = next(self.data)
            try:
                char = self.line[self.pos]
            except IndexError:
                self.line = next(self.data)
                self.pos = 0
            else:
                self.pos += 1
                return char

class WordIter(CharIter):
    def __next__(self):
        while 1:
            if self.line is None:
                self.line = next(self.data)
            try:
                words = self.line.split()
                word = words[self.pos]
            except IndexError:
                self.line = next(self.data)
                self.pos = 0
            else:
                self.pos += 1
                return word

# this hurts memory b/c it returns everything in a big list
def char_gen_old(lines):
    res = []
    for line in lines:
        for char in line:
            res.append(char)
    return res

# list comprehension
def char_gen_lc(lines):
    res = [char for line in lines for char in line]
    return res

# generator expression - list comprehension for generators
def char_gen_exp(lines):
    res = (char for line in lines for char in line)
    return res

# generators are denoted by yield key word
# Generators do lazy loading like the iter examples above making them very performant
# this doesn't return a list, but a generator that doesn't run until called
# generators remember where they are so they become exhausted
# generators can be infinite (don't support slicing)
def char_gen(lines):
    for line in lines:
        for char in line:
            yield char

def word_gen(lines):
    for line in lines:
        for word in line.split():
            yield word

def window_gen(data, size):
    win = []
    for thing in data:
        win.append(thing)
        if len(win) == size:
            yield win
            win = win[1:]
    for i in range(len(win)):
        yield win[i:]

class Markov:
    """
    >>> m3 = Markov('Find a city, find yourself a city to live in', 3)
    >>> m3.predict('cit')
    'y'

    """
    def __init__(self, data, size=1):
        #self.table = get_table(data)
        self.tables = []
        for i in range(size):
            self.tables.append(get_table_old(data, i+1))

    def predict(self, data_in):
        table = self.tables[len(data_in)-1]
        options = table[data_in]
        possible = ''
        for key, count in options.items():
            possible += key * count
        return random.choice(possible)

class CharMarkov(Markov):
    """
    >>> lines = ['abc', 'def', 'hi']
    >>> cm = CharMarkov(lines, 2)
    >>> cm.predict('cd')
    'e'
    """
    def __init__(self, lines, size=1):
        self.tables = []
        data = list(char_gen(lines))
        for i in range(size):
            self.tables.append(get_table(data, i+1))

def just_name(klass):
    def name(self):
        return '{}'.format(self.__class__.__name__)
    klass.__str__ = name
    return klass

@just_name
class WordMarkov(Markov):
    """
    >>> lines = ['my name is', 'matt', 'bye']
    >>> wm = WordMarkov(lines, 2)
    >>> wm.predict('is')
    'matt'
    """
    def __init__(self, lines, size=1):
        self.tables = []
        data = list(word_gen(lines))
        for i in range(size):
            self.tables.append(get_table(data, i+1))

    def predict(self, data_in):
        table = self.tables[len(data_in.split())-1]
        options = table[data_in]
        possible = []
        for key, count in options.items():
            for i in range(count):
                    possible.append(key)
        return random.choice(possible)

def test_predict(m, start, numchars=1):
    res = [start]
    for i in range(20):
        let = m.predict(start)
        res.append(let)
        start = ''.join(let[-numchars:])
    return ''.join(res)

def get_table(data, size=1, join_char=''):
    results = {}
    for tokens in window_gen(data, size+1):
        item = join_char.join(tokens[:size])
        try:
            output = tokens[size]
        except IndexError:
            break
        inner_dict = results.get(item, {})
        inner_dict.setdefault(output, 0)
        inner_dict[output] += 1
        results[item] = inner_dict
    return results

def get_table_old(line, numchars=1):
    result = {}
    for i, _ in enumerate(line):
        chars = line[i:i+numchars]
        try:
            next_char = line[i+numchars]
        except IndexError:
            break
        char_dict = result.get(chars, {})
        char_dict.setdefault(next_char, 0)
        char_dict[next_char] += 1
        result[chars] = char_dict
    return result

def repl(m):
    while 1:
        try:
            txt = input(">")
        except KeyboardInterrupt:
            break
        res = m.predict(txt)
        print(res)

def add(x, y):
    "this adds x and y"
    return x+y
# args = (2,3)
# add(*args)
# kw = {'x':2, 'y':3}
# add(**kw)

def foo(*args, **kwargs):
    print(args, kwargs)

# can curry in Python - closures
def genadder(suffix):
    def adder(x):
        return x+ suffix
    return adder
# add5 = genadder(5)
# add5(10)
# addtxt = genadder('.txt')
# addtxt('data')
# 'data.txt'

#def iden(func):
#    return func
#add_new = iden(add)
#add_new(6, 7)
# Adding decorators - print functions inside
# may be very useful in a timer
def iden2(f):
    def inner(*args, **kwargs):
        print("Before", args, kwargs)
        res = f(*args, **kwargs)
        print("AFTER", res)
        return res
    return inner
#add_new2 = iden2(add)
#add_new2(6, 7)

#import time
#def slow(x):
#    time.sleep(x)
##    return x
##
##def timing(func):
##    time1 = time()
##    func()
##    time2 = time()
##    print('{} took {}'.format(func, time2-time1))
##
##@timing
##def greet(name):
##    print('hi {}'.format(name))

#name = 'matt'
#print(name)

def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--file', help='input file')
    p.add_argument('-s', '--size', help="Markov size",
                   default=1, type=int)
    p.add_argument('--encoding', help='File encoding',
                   default='utf8')
    p.add_argument('-t', '--test', action='store_true', help='Run tests')
    opt = p.parse_args(args)
    if opt.file:
        with open(opt.file, encoding=opt.encoding) as fin:
        #with open(opt.file) as fin:

            data = fin.read()
            m = Markov(data, size=opt.size)
            repl(m)
    elif opt.test:
        import doctest
        doctest.testmod()

if __name__ == '__main__':
    # When we are executing this file
    import doctest
    doctest.testmod()
    # main(sys.argv[1:])
else:
    print("not running")
