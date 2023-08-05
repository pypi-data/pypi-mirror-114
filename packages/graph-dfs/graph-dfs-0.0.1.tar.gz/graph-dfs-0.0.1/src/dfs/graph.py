from typing import List


class Graph:
    def __init__(self, n: int):
        self.n = n
        self._edges: List[List[int]] = [list() for _ in range(n)]

    def link(self, u: int, v: int):
        self._edges[u].append(v)

    @property
    def vertices(self):
        for u in range(self.n):
            yield u

    def neighbors(self, u: int):
        for v in self._edges[u]:
            yield v
