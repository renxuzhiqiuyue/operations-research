#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
def dict_to_numpy(data_dict, V):
    data_np = np.zeros((len(V), len(V)))
    for i in data_dict.keys():
        data_np[i[0]-1, i[1]-1] = data_dict[i]
    print(data_np)

def floyd(V, E, w, INF = float("inf")):
    """
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    w := dict( Edge(u,v) : cost)
    
    Returns:
    U := dict( (vi, vj) ： cost)
    R := dict( (vi, vj): next)

    else:
    print('存在负回路')
    negative_road : = set( Egde(u,v))
    """
    
    """
    Step 1 : Initialization
    """
    U, R = dict(), dict()
    
    for u in V:
        for v in V:
            if (u, v) in E:
                U[(u, v)] = w[(u, v)]
            elif u == v:
                U[(u, v)] = 0
            else:
                U[(u, v)] = INF
                
            R[(u, v)] = v
    print('-----loop 0-----')
    dict_to_numpy(U, V), dict_to_numpy(R, V) 
    """
    Step 2 : 迭代
    """
    iteration = 0
    for k in V:
        iteration += 1
        for u in V:
            for v in V:
                if U[(u, v)] > U[(u, k)] + U[(k, v)]:
                    U[(u, v)] = U[(u, k)] + U[(k, v)]
                    R[(u, v)] = R[(u, k)]
        print('-----loop {0}-----迭代顶点：{1}'.format(iteration, k))
        dict_to_numpy(U, V), dict_to_numpy(R, V) 
    '''
    Step 3：判断回路
    '''
    for v in V:
        if U[(v, v)] <0:
            print('存在负回路')
            negative_road = set()
            vs, vt = v, v
            while R[(vs, vt)] != vt:
                negative_road.add((vs, R[(vs, vt)]))
                vs = R[(vs, vt)]
            negative_road.add((vs, R[(vs, vt)]))
            return negative_road
    
    return U, R
if __name__ == '__main__':
    V = {1, 2, 3, 4, 5} 
    E = {(1, 2), (5, 4), (2, 3), (4, 3), (5, 1), (2, 5), (4, 1), (3, 5)}
    w = {(1, 2): 1, (4, 1): 3, (5, 1): 4, (2, 3): 5, (2, 5): -3, (3, 5): 2, (4, 3): 6, (5, 4): -2}
    negative_road = floyd(V, E, w)
    print('\n', negative_road) 