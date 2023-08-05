from dfs.dfs import DFS
from dfs.graph import Graph


def get_sample_graph() -> Graph:
    g = Graph(7)
    edges = [(0, 1), (0, 4), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (5, 6)]
    for u, v in edges:
        g.link(u, v)
    return g


def test_001():
    g = get_sample_graph()
    assert g.n == 7


def test_002():
    g = get_sample_graph()
    dfs = DFS(g)
    dfs.start()
    assert list(dfs.topological_sorting()) == [6, 5, 4, 3, 2, 1, 0]
