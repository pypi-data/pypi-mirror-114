# Graph-DFS

This package allows for the creation of graphs. It also provides the depth first search algorithm. 

## How to use it?

To create a 
graph, do:

```python
g = Graph(n)
```

where `n` is the number of vertices. To create an arc from
vertex `a` to vertex `b`, do:

```python
g.link(a, b)
```

where `a` and `b` are indices in the range `[0, n - 1]`. You can perform a depth first search on the graph
with:

```python
dfs = DFS(g)
dfs.start()
```

## Installation

```shell
pip install graph-dfs
```



If you desire to obtain a topological sorting of the graph, then do so after a DFS with:

```python
dfs.opological_sorting()
```
