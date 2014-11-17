__author__ = 'loromichi'

import os
import pickle
import tools


# UTF-8の各バイトの文字集合
# bytes_dict = {1: set(), 2: set(), 3: set(), 4: set()}
if not os.path.exists(os.path.join("pickles", "utf8_charset.pickle")):
    tools.make_utf8_char_set()
with open(os.path.join("pickles", "utf8_charset.pickle"), "rb") as f:
    utf8_bytes_dict = pickle.load(f)

# ngram
if not os.path.exists(os.path.join("pickles", "ngram.pickle")):
    tools.n_gram()
with open(os.path.join("pickles", "ngram.pickle"), "rb") as f:
    ngram_dict = pickle.load(f)

