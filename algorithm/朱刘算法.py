# 第一次在git中发表文件， 这个文件复制了别人的代码，但是找不到是哪一个了，以后补充作者相关信息
# this is the first time I published code in Git. This file copied someone else's code, but I can't find which one. The author related information will be added later

#!/usr/bin/env python
# -*- coding:utf-8 -*-

def msa(V, E, r, w):
    """
    Recursive Edmond's algorithm as per Wikipedia's explanation
    Returns a set of all the edges of the minimum spanning arborescence.
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    r := Root(v)
    w := dict( Edge(u,v) : cost)
    """

    """
    Step 1 : Removing all edges that lead back to the root
    """
    for (u,v) in E.copy():
        if v == r:
            E.remove((u,v))
            w.pop((u,v))

    """
    Step 2 : Finding the minimum incoming edge for every vertex. O(n**2) but okay since it is
    a small sized list
    """
    pi = dict()
    for v in V:
        edges = [edge[0] for edge in E if edge[1] == v]
        if not len(edges):
            continue
        costs = [w[(u,v)] for u in edges]
        pi[v] = edges[costs.index(min(costs))]
    
    """
    Step 3 : Finding cycles in the graph
    """
    cycle_vertex = None
    for v in V:
        if cycle_vertex is not None:
            break
        visited = set()
        next_v = pi.get(v)
        while next_v:
            if next_v in visited:
                cycle_vertex = next_v
                break
            visited.add(next_v)
            next_v = pi.get(next_v)
    
    """
    Step 4 : If there is no cycle, return all the minimum edges pi(v)
    """
    if cycle_vertex is None:
        return set([(pi[v],v) for v in pi.keys()])
    
    """
    Step 5 : Otherwise, all the vertices in the cycle must be identified
    """
    C = set()
    C.add(cycle_vertex)
    next_v = pi.get(cycle_vertex)
    while next_v != cycle_vertex:
        C.add(next_v)
        next_v = pi.get(next_v)
    
    """
    Step 6 : Contracting the cycle C into a new node v_c
    v_c is negative and squared to avoid having the same number
    """
    v_c = -cycle_vertex**2
    V_prime = set([v for v in V if v not in C] + [v_c])
    E_prime = set()
    w_prime = dict()
    correspondance = dict()
    for (u,v) in E:
        if u not in C and v in C:
            e = (u,v_c)
            if e in E_prime:
                if w_prime[e] < w[(u,v)] - w[(pi[v],v)]:
                    continue
            w_prime[e] = w[(u,v)] - w[(pi[v],v)]
            correspondance[e] = (u,v)
            E_prime.add(e)
        elif u in C and v not in C:
            e = (v_c,v)
            if e in E_prime:
                old_u = correspondance[e][0]
                if w[(old_u,v)] < w[(u,v)]:
                    continue
            E_prime.add(e)
            w_prime[e] = w[(u,v)]
            correspondance[e] = (u,v)
        elif u not in C and v not in C:
            e = (u,v)
            E_prime.add(e)
            w_prime[e] = w[(u,v)]
            correspondance[e] = (u,v)
    
    """
    Step 7 : Recursively calling the algorithm again until no cycles are found
    """
    tree = msa(V_prime, E_prime, r, w_prime)
    
    """
    Step 8 : 
    """
    cycle_edge = None
    for (u,v) in tree:
        if v == v_c:
            old_v = correspondance[(u,v_c)][1]
            cycle_edge = (pi[old_v],old_v)
            break
    
    ret = set([correspondance[(u,v)] for (u,v) in tree])
    for v in C:
        u = pi[v]
        ret.add((u,v))
        
    ret.remove(cycle_edge)
    
    return ret

if __name__ == '__main__':
    V = set([1, 2, 3, 4, 5, 6])
    E = set([(1, 2), (2, 6), (5, 6), (6, 1), (6, 3), (2, 3), (4, 3), (3, 5)])
    r = 4
    w = dict({(1, 2): 3, (2, 6): 3, (5, 6): 5, (6, 1): 3, (6, 3): 2, (2, 3): 1, (4, 3): 6, (3, 5): 5})
    minimal_tree = msa(V, E, r, w)
    for i in minimal_tree:
        print(i)

    V = set([1,2,3,4])
    E = set([(1,2), (2,3), (3,4), (4,2)])
    r = 1
    w = dict({(1,2):4, (2,3):3, (3,4):2, (4,2):1})
    minimal_tree = msa(V, E, r, w)
    for i in minimal_tree:
        print(i)