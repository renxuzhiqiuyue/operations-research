#!/usr/bin/env python
# -*- coding:utf-8 -*-
def D_f(V, E, C, F):
    '''
    剩余网络
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    C := dict( Edge(u,v) : volume)
    F := dict( Edge(u,v) : flow)
    '''
    E_D_plus = [e for e in E if F[e] < C[e]]
    E_D_minus = [(e[1], e[0]) for e in E if F[e] > 0]
    E_D = set(E_D_plus + E_D_minus)
    # 改变权重
    C_D = dict()
    for e in E_D_plus:
        C_D[e] = C[e] - F[e]
    for e in E_D_minus:
        C_D[e] = F[(e[1], e[0])]
    return V, E_D, C_D

if __name__ == '__main__':    
    V = set([1,2,3,4,5,6])
    E = set([(1,2), (1,4), (2,3), (2,4), (2,5), (5,3), (3,6), (4,5), (5,6)])
    C = dict({(1,2):4, (1,4):6, (2,3):2, (2,4):2, (2,5):1, (5,3):3, (3,6):4, (4,5):5, (5,6):7})
    F = dict({(1, 2): 3, (4, 5): 5, (5, 6): 6, (1, 4): 5, (2, 3): 2, (3, 6): 2, (2, 5): 1, (2, 4): 0, (5, 3): 0})
    
    print(D_f(V, E, C, F))