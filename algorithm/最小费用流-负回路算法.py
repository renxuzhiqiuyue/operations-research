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

def ford_fulkerson(V, E, vs, vt, C, f, F=None):
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
    if sum([F[i] for i in F.keys() if i[0] == vs]) == f:
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
    if delta > 0:
        delta = 1

    print('调整值：{0}, 路：{1}, 当前可行流：{2}'.format(delta, road_vs_to_vt, F))
    for e in road_vs_to_vt:
        if e_lable[e] == 1:
            F[e] = F[e] + delta
        if e_lable[e] == -1:
            F[e] = F[e] - delta
    
    return ford_fulkerson(V, E, vs, vt, C, f, F)

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
    #print('-----loop 0-----')
    #dict_to_numpy(U, V), dict_to_numpy(R, V) 
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
        #print('-----loop {0}-----迭代顶点：{1}'.format(iteration, k))
        #dict_to_numpy(U, V), dict_to_numpy(R, V) 
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
    
def negative_cost_circuit(V, E, vs, vt, C, w, f, F=None):
    """
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    vs, vt: 发点，收点
    C := dict( Edge(u,v) : volume)
    w := dict( Edge(u,v) : cost)
    f := 定流
    F := dict( Edge(u,v) : flow)
    """

    '''
    Step One: 生成给定的流值
    '''
    F = ford_fulkerson(V, E, vs, vt, C, f)
    if sum([F[i] for i in F.keys() if i[0] == vs]) < f:
        print('最大流小于给定的流值')
    
    '''
    Step Two: 构造剩余网络，并寻找负回路
    '''
    flag = True
    while flag:
        V, E_D, C_D = D_f(V, E, C, F)
        try:
            negative_road = floyd(V, E_D, w)

            # 进行增广
            delta = min([C_D[e] for e in negative_road])
            #print('调整值：{0}, 路：{1}, 当前可行流：{2}'.format(delta, road_vs_to_vt, F))
            for e in negative_road:
                try:
                    F[e] = F[e] + delta
                except:
                    F[e] = delta
        except:
            flag = False

    return F

if __name__ == '__main__':    
    V = set(['vs',1,2,3, 'vt'])
    E = {(1, 2), (3, 2), (1, 3), ('vs', 3), ('vs', 1), (2, 'vt'), (3, 'vt')}
    vs = 'vs'
    vt = 'vt'
    C = dict({('vs',1):3, ('vs',3):2,(1,2):3, (1,3):1, (3,2):2, (3,'vt'):3, (2,'vt'):3})
    w = dict({('vs',1):2, ('vs',3):3,(1,2):4, (1,3):1, (3,2):5, (3,'vt'):2, (2,'vt'):1})
    f = 1000
    F = negative_cost_circuit(V, E, vs, vt, C, w, f, F=None)
    print('可行流',F, '\n流量', sum([F[i] for i in F.keys() if i[0] == vs]))