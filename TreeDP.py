# When you need bfs order of tree
# adj = list of adjacent nodes (with edge costs)
# root = root

# unweighted tree
from collections import deque
def set_root(adj, root):
    Q = deque([root]); bfsord = []
    tadj = [[] for i in range(len(adj))]
    visit = [0]*len(adj); visit[root] = True
    while Q:
        p = Q.popleft(); bfsord.append(p)
        for q in adj[p]:
            if visit[q]: continue
            visit[q] = True; Q.append(q)
            tadj[p].append(q)
    return tadj, bfsord

# weighted tree
from collections import deque
def set_root(adj, root):
    Q = deque([root]); bfsord = []
    tadj = [[] for i in range(len(adj))]
    visit = [0]*len(adj); visit[root] = True
    while Q:
        p = Q.popleft(); bfsord.append(p)
        for q, c in adj[p]:
            if visit[q]: continue
            visit[q] = True; Q.append(q)
            tadj[p].append((q,c))
    return tadj, bfsord