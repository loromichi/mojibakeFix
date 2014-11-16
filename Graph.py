__author__ = 'hiromichi_s'

import sys
from collections import defaultdict


class Node:
    def __init__(self, id_, name, weight):
        self.id = id_
        self.name = name
        self.weight = weight

    def __str__(self):
        return self.name


class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight

    def __str__(self):
        return str(self.start_node.name) + "-" + str(self.end_node.name) + "(" + str(self.weight) + ")"


class Graph:
    def __init__(self):
        self.id_node = {}                       # ノードidとノードオブジェクトの辞書
        self.id_next_edges = defaultdict(list)  # {ノードid: ノードidのノードから接続先ノードへのedgeオブジェクトのリスト}
        self.id_prev_edges = defaultdict(list)  # {ノードid: 接続元ノードからノードidのノードへのedgeオブジェクトのリスト}
        self.last_id = -1                       # 最後に追加されたノードのid

        self.add_node("<S>", 0)

    def get_next_edges(self, node_id):
        return self.id_next_edges[node_id]

    def get_prev_edges(self, node_id):
        return self.id_prev_edges[node_id]

    def add_node(self, name, weight):
        self.last_id += 1
        self.id_node[self.last_id] = Node(self.last_id, name, weight)
        return self.last_id

    def add_edge(self, start_id, end_id, weight):
        edge = Edge(self.id_node[start_id], self.id_node[end_id], weight)
        self.id_next_edges[start_id].append(edge)   # next_edge
        self.id_prev_edges[end_id].append(edge)     # prev_edge


def viterbi(graph):
    """
    graphの最短経路のパスを計算
    startからendまでのidのリストを返す
    """

    id_sumCost = {0: 0}  # {ノードid: そこに至るまでの最短のコスト}
    id_prevId = {}       # {ノードid: その後ろのid}

    for node_id, node in sorted(graph.id_node.items()):
        if node_id == 0:
            continue
        node_cost = node.weight  # node自身のコスト
        shortest_prev_node = None
        min_cost = sys.maxsize

        # nodeに到達するまでの最小コストをもとめ，id_sumCodeとid_prevIdに保存
        for prev_edge in graph.get_prev_edges(node_id):

            # startからprev_nodeまでのコスト + prev_nodeからnodeまでのエッジのコスト + node自身のコスト
            prev_id = prev_edge.start_node.id
            cost = id_sumCost[prev_id] + prev_edge.weight + node_cost

            if cost < min_cost:
                min_cost = cost
                shortest_prev_node = prev_id

        id_sumCost[node.id] = min_cost
        id_prevId[node.id] = shortest_prev_node

    # 最短経路
    # BOSになるまでprev_nodeを追加していく
    shortest_path = [graph.last_id]
    while shortest_path[-1] != 0:
        shortest_path.append(id_prevId[shortest_path[-1]])

    return list(reversed(shortest_path))


if __name__ == '__main__':
    g = Graph()
    a_node_id = g.add_node("a", 1)
    b_node_id = g.add_node("b", 2)
    c_node_id = g.add_node("c", 3)
    d_node_id = g.add_node("d", 4)
    e_node_id = g.add_node("e", 5)
    f_node_id = g.add_node("</S>", 0)

    g.add_edge(0, a_node_id, 0)
    g.add_edge(a_node_id, b_node_id, 5)
    g.add_edge(a_node_id, c_node_id, 4)
    g.add_edge(b_node_id, d_node_id, 3)
    g.add_edge(c_node_id, d_node_id, 2)
    g.add_edge(d_node_id, e_node_id, 1)
    g.add_edge(e_node_id, f_node_id, 0)

    print("-".join(str(g.id_node[i]) for i in viterbi(g)))

