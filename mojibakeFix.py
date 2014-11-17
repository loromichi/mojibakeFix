__author__ = 'loromichi'

import os
import argparse
import tools
from decoder import UTF_8


def main():
    # 引数の処理
    parser = argparse.ArgumentParser(description='fix mojibake')
    parser.add_argument('-f', type=str, help='text file')

    args = parser.parse_args()
    input_file = args.f

    if not os.path.exists(input_file):
        print(input_file, "is not found")
        return

    # データの作成(ないときだけ)
    if not os.path.exists(os.path.join("pickles", "utf8_charset.pickle")):
        tools.make_utf8_char_set()
    if not os.path.exists(os.path.join("pickles", "ngram.pickle")):
        tools.n_gram()

    # 文字化けの復元
    with open(input_file, "rb") as f:
        lines = f.read()

    u = UTF_8()
    fixed_string = u.fix_mojibake(lines, b"\x81\x45")
    print(fixed_string)


if __name__ == '__main__':
    main()