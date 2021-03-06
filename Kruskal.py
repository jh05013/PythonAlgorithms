# Kruskal's algorithm for MST
# inf if disconnected
# n = number of vertices
# edges = list of edges of the form (cost, v, v)
# sort = if True, then [edges] is sorted before processing
# This can be either 0-indexed or 1-indexed

__import__('sys').setrecursionlimit(123123)
def MST(n, edges, sort=True):
    parent = list(range(n+1))
    def union(x, y): parent[find(x)] = find(y)
    def find(x):
        if parent[x] != x: parent[x] = find(parent[x])
        return parent[x]
    
    if sort: edges.sort()
    cost = 0; MST = []
    for e in edges:
        c, a, b = e
        if find(a) != find(b): cost+= c; union(a, b); MST.append(e)
    if len(MST) < n-1: return float('inf'), []
    return cost#, MST

from sys import stdin
input = stdin.readline
v, e = map(int,input().split())
edges = []
for i in range(e):
    a, b, c = map(int,input().split())
    edges.append((c,a,b))
