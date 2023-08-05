from typing import List

from dfs.graph import Graph


class DFS:
    def __init__(self, graph: Graph):
        self.graph = graph
        self._unseen: List[bool] = [True for _ in range(graph.n)]
        self._finalized: List[int] = list()

    def start(self):
        for u in self.graph.vertices:
            if self._unseen[u]:
                self.explore(u)

    def explore(self, u: int):
        self._unseen[u] = False
        for v in self.graph.neighbors(u):
            if self._unseen[v]:
                self.explore(v)
        self._finalized.append(u)

    def topological_sorting(self):
        for u in self._finalized:
            yield u
