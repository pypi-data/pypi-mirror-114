# Anagram Solver

[![Build Status](https://travis-ci.com/Ruben9922/anagram-solver.svg?branch=master)](https://travis-ci.com/Ruben9922/anagram-solver)
[![PyPI](https://img.shields.io/pypi/v/ruben-anagram-solver)](https://pypi.org/project/ruben-anagram-solver/)
[![GitHub](https://img.shields.io/github/license/Ruben9922/anagram-solver)](https://github.com/Ruben9922/anagram-solver/blob/master/LICENSE)

Simple anagram solver.

Currently only English is supported, but it could be extended to support other languages. The main difficulty would be finding a systematic way to obtain lists of valid words for multiple languages.

## Installation
Install as usual:

```bash
pip install ruben-anagram-solver
```

You may wish to [create a virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) beforehand.

## Usage
Run the program using the following command:
```bash
ruben-anagram-solver
```

Using the program is extremely simple:
```
Enter string: cchikne
['check-in', 'chicken']
```

## How It Works
Since an anagram of some word is just some rearrangement of the word's letters, two words are anagrams of each other if they are same when the order (and possibly case) of the letters is ignored. To check this, the idea was to convert each of the two words to some "order-insensitive" representation and compare this. Such a representation could be simply the letters sorted (e.g. `['c', 'c', 'e', 'h', 'i', 'k', 'n']` for "chicken") or a count of each letter in the word (e.g. `{('n', 1), ('h', 1), ('c', 2), ('e', 1), ('i', 1), ('k', 1)}`). I also decided to ignore case (by first converting the word to lower case) and ignore non-alphanumeric characters (by removing them from the word).

The exact steps are as follows:
1.  Read a list of English words.
    *   IIRC the words list is from: https://github.com/dwyl/english-words.
2.  Convert each word to its order-insensitive representation (as described above).
3.  Create a dictionary where each key is an order-insensitive representation (e.g. `{"a": 1, "b": 1, "t": 1}`) and each value is the set of words that correspond to that order-insensitive representation (e.g. `{"bat", "tab"}`).
    *   This is to make lookups more efficient, should the program be extended to allow multiple lookups.
4.  Input an anagram from the user.
5.  Convert the anagram to its order-insensitive representation.
6.  Look this up in the dictionary to obtain the set of words corresponding to the anagram's order-insensitive representation.
7.  Output this set of words.
