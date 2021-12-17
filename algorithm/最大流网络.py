#!/usr/bin/env python
# -*- coding:utf-8 -*-
def D_f(V, E, C, F):
    '''
    剩余网络
    
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

def AD_f(V, E_D, vs, vt):
    '''
    分层剩余网络
    V := set( Vertex(v) )
    E_D := set( Edge(u,v) )
    '''
    # 广探法标号
    h = dict()
    # 初始化
    h[vs] = 0

    # 开始进行分层
    floor_num = 0
    while (len(h) < len(V)) and (floor_num < 20):
        floor_num += 1
        for (vi, vj) in E_D:
            if vi in h.keys() and vj not in h.keys():
                h[vj] = h[vi]+1
            if vi in h.keys() and vj in h.keys() and h[vj] > h[vi]+1:
                h[vj] = h[vi]+1

    # 如果vt不能被标号，则不存在(vs, vt)路
    flag = True
    if vt not in h.keys():
        flag = False
        V_AD = set([vt])
        E_AD = set()
    else:
        V_AD = set([vt] + [v for v in V if h[v]<h[vt]])
        E_AD = set([e for e in E_D if h[e[1]] == h[e[0]] + 1 and h[e[1]] < h[vt]] + [e for e in E_D if h[e[0]] == h[vt] -1 and e[1] == vt])
    return flag, h, V_AD, E_AD

def ford_fulkerson(V, E, vs, vt, C, F=None):
    """
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    vs, vt: 发点，收点
    C := dict( Edge(u,v) : volume)
    F := dict( Edge(u,v) : flow)
    """

    # 是否自动生成零流
    if F == None:
        F = dict(zip(list(E), [0]*(len(E))))
    
    # 构建剩余网络
    V, E_D, C_D = D_f(V, E, C, F)
    # 构建分层剩余网络
    flag, h, V_AD, E_AD = AD_f(V, E_D, vs, vt)
    # 如果不存在(vs, vt) 路则跳出h函数
    if flag == False:
        return F
    
    # 寻找(vs, vt)路, 与delta
    road_vs_to_vt = set()
    v_visit = vt
    e_lable = dict()
    while v_visit != vs:
        for e in E_AD:
            # 反向弧
            if e[0] == v_visit and h[e[1]] == h[e[0]]-1 and F[e] > 0:
                road_vs_to_vt.add(e)
                v_visit = e[1]
                e_lable[e] = -1
                break

            # 正向弧
            if e[1] == v_visit and h[e[0]] == h[e[1]]-1 and F[e] < C[e]:
                road_vs_to_vt.add(e)
                v_visit = e[0]
                e_lable[e] = 1
                break   
    # 进行增广
    delta = min([C_D[e] for e in road_vs_to_vt if e_lable[e] == 1] + [F[e] for e in road_vs_to_vt if e_lable[e] == -1])
    print('调整值：{0}, 路：{1}, 当前可行流：{2}'.format(delta, road_vs_to_vt, F))
    for e in road_vs_to_vt:
        if e_lable[e] == 1:
            F[e] = F[e] + delta
        if e_lable[e] == -1:
            F[e] = F[e] - delta
    
    return ford_fulkerson(V, E, vs, vt, C, F)

if __name__ == '__main__':    
    V = set([1,2,3,4,5,6])
    E = set([(1,2), (1,4), (2,3), (2,4), (2,5), (5,3), (3,6), (4,5), (5,6)])
    vs = 1
    vt = 6
    C = dict({(1,2):4, (1,4):6, (2,3):2, (2,4):2, (2,5):1, (5,3):3, (3,6):4, (4,5):5, (5,6):7})
    F = ford_fulkerson(V, E, vs, vt, C)
    print(F, '\n')
    
    print(V, E, C, F, '\n')
    print(D_f(V, E, C, F))


