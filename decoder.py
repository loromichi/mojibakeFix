__author__ = 'loromichi'

import sys
import math
from Graph import Graph, viterbi
from settings import utf8_bytes_dict, ngram_dict


class UTF_8():
    """
    文字化けしたUTF-8のバイト列をもとに解釈可能な文字列のグラフを作成する
    """

    def num_of_byte(self, b):
        """
        UTF-8の一文字の先頭バイト -> バイト数, 中間バイト-> 0, 不当なバイト -> -1 を返す
        """
        assert(isinstance(b, int))

        for first, end, n in [(0x80, 0xBF, 0), (0x0, 0x7F, 1), (0xC2, 0xDF, 2), (0xE0, 0xEF, 3), (0xF0, 0xF7, 4)]:
            if first <= b <= end:
                return n
        return -1

    def split_utf8(self, utf8_sequence, replace_char):
        """
        UTF-8の1文字になりうる箇所で切った配列を作成
        ex. b"\x41\xe3\x81\x82\x61" -> [b"\x41", b"\xe3\x81\x82", b"\x61"]
        """

        utf8_sequence = utf8_sequence.replace(replace_char, b"\x00\x00")
        utf8_sequence = [-1 if i == 0x00 else i for i in utf8_sequence]
        char_list = []
        i = 0
        while i < len(utf8_sequence):
            num_of_byte = self.num_of_byte(utf8_sequence[i])

            # ある文字の先頭バイトから始まる
            # INFO: else以下の処理で統一すると,[3, 0, 0, -1, -1, 2, 0]みたいなのきたとき0と-1の間で切れなくなる
            if num_of_byte > 0:
                char_list.append(utf8_sequence[i:i + num_of_byte])
                i += num_of_byte

            # 代替文字(-1)から始まる
            else:
                # 次の文字先頭バイトが来るまで進み，見つかったらそれ以前のバイト列を格納
                for offset, b in enumerate(utf8_sequence[i:]):
                    if self.num_of_byte(b) > 0:
                        char_list.append(utf8_sequence[i:i + offset])
                        i += offset
                        break
                # 最後まで先頭バイトが見つからなかった
                else:
                    char_list.append(utf8_sequence[i:])
                    break

        # 代替文字を-1に変換したときに，最後に余計な[-1]がついていたら削除
        # UTF-8の1byte文字をShift_JISは内包しているので[-1]が単独で現れることはない
        if char_list[-1] == [-1]:
            char_list.pop()

        return char_list

    def generate_charcter(self, utf8_char):
        """
        brokenなUTF-8の1文字がきたとき，そこから解釈可能なUnicode文字の集合を生成する
        """
        if -1 not in utf8_char:
            return set(bytes(utf8_char).decode("utf-8"))

        # すべてが-1なら予め用意したnバイト文字の集合を返す
        if utf8_char == [-1] * len(utf8_char):
            return utf8_bytes_dict[len(utf8_char)]

        char_set = set()
        stack = [utf8_char]

        while stack:
            char = stack.pop()

            # -1があるなら，最初の-1の箇所にすべてのバイトを入れる
            if -1 in char:
                idx = char.index(-1)
                stack += [char[:idx] + [i] + char[idx+1:] for i in range(0x80, 0xF8)]
                continue

            # -1がないならUTF-8で解釈してみる
            try:
                char_set.add(bytes(char).decode("UTF-8"))
            except UnicodeDecodeError:
                pass

        return char_set

    def make_graph(self, chars_list):
        """
        グラフを作成する
        chars_list: [["あ"], [”い”, "う", "え", "お"],...]
        """
        uni_gram = ngram_dict[1]
        bi_gram = ngram_dict[2]

        uni_sam = sum(uni_gram.values())    # uni-gramの合計数

        graph = Graph()
        now_ids = [0]  # <S>を入れる
        for chars in chars_list + [["</S>"]]:
            prev_ids = now_ids[:]  # 前回のノードid
            now_ids = []
            for now_char in chars:
                uni_num = uni_gram.get((now_char, ), 0)

                # TODO: 未知文字はSKIP
                if uni_num == 0:
                    continue

                node_weight = uni_num / uni_sam     # P(now_char)

                now_id = graph.add_node(now_char, -1 * math.log(node_weight))
                now_ids.append(now_id)

                # 前回の文字から現在の文字へのパスを張る
                for prev_id in prev_ids:
                    prev_char = graph.id_node[prev_id].name
                    bi_num = bi_gram.get((prev_char, now_char), 1)
                    edge_weight = bi_num / uni_gram.get((prev_char, ))      # P(now_char|prev_char)

                    graph.add_edge(prev_id, now_id, -1 * math.log(edge_weight))

        return graph

    def fix_mojibake(self, lines, replace_char):
        # 候補集合の作成
        chars_list = []
        for char in self.split_utf8(lines, replace_char):
            chars_list.append(list(self.generate_charcter(char)))

        # グラフの構築
        g = self.make_graph(chars_list)

        # 最短経路の計算
        route = viterbi(g)

        return "".join(str(g.id_node[i]) for i in route[1:-1])