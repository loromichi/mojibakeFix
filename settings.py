__author__ = 'loromichi'

import os
import pickle

# UTF-8の各バイトの文字集合
# bytes_dict = {1: set(), 2: set(), 3: set(), 4: set()}
with open(os.path.join("pickles", "utf8_charset.pickle"), "rb") as f:
    utf8_bytes_dict = pickle.load(f)

# ngram
with open(os.path.join("pickles", "ngram.pickle"), "rb") as f:
    ngram_dict = pickle.load(f)

