__author__ = 'loromichi'


import os
import math
import pickle
from itertools import product


def make_utf8_char_set():
    """
    UTF-8の1/2/3/4バイトの文字の集合を作成
    """
    bytes_dict = {1: set(), 2: set(), 3: set(), 4: set()}
    two = range(0x80, 0xBF + 1)

    for i in range(0x00, 0x7F + 1):
        bytes_dict[1].add(bytes([i]).decode("utf-8"))

    for i, j in product(range(0xC2, 0xDF + 1), two):
            bytes_dict[2].add(bytes([i, j]).decode("utf-8"))

    for i, j, k in product(range(0xE0, 0xEF + 1), two, two):
        try:
            bytes_dict[3].add(bytes([i, j, k]).decode("utf-8"))
        except UnicodeDecodeError:
            pass

    for i, j, k, l in product(range(0xF0, 0xF7 + 1), two, two, two):
        try:
            bytes_dict[4].add(bytes([i, j, k, l]).decode("utf-8"))
        except UnicodeDecodeError:
            pass

    with open("utf8_charset.pickle", "wb") as f:
        pickle.dump(bytes_dict, f)


def n_gram():
    def make_ngram_dict(file_path, n):
        d = {}
        with open(file_path, "r", encoding="UTF-8") as f:
            for line in f:
                chars, num = line.rstrip().rsplit("\t", 1)
                d[tuple(chars.rsplit(" ", n))] = int(num)
        return d

    ngram = dict()
    ngram[1] = make_ngram_dict(os.path.join("ngram", "1gm-0000"), 1)
    ngram[2] = make_ngram_dict(os.path.join("ngram", "2gm-0000"), 2)

    with open("ngram.pickle", "wb") as f:
        pickle.dump(ngram, f)


if __name__ == '__main__':
    #make_utf8_char_set()
    n_gram()