#!/usr/bin/env python
# -*- coding:utf-8 -*-

from numpy import minimum

def D_f(V, E, C, F, w):
    '''
    剩余网络
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    C := dict( Edge(u,v) : volume)
    F := dict( Edge(u,v) : flow)
    w := dict( Edge(u,v) : cost)
    '''
    E_D_plus = [e for e in E if F[e] < C[e]]
    E_D_minus = [(e[1], e[0]) for e in E if F[e] > 0]
    E_D = set(E_D_plus + E_D_minus)
    # 改变权重
    C_D = dict()
    w_D = dict()
    for e in E_D_plus:
        C_D[e] = C[e] - F[e]
        w_D[e] = w[e]
    for e in E_D_minus:
        C_D[e] = F[(e[1], e[0])]
        w_D[e] = w[(e[1], e[0])]

    return V, E_D, C_D, w_D

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
    
def min_cost_path(V, E, vs, vt, C, w, f_sum, w_sum, F=None):
    """
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    vs, vt: 发点，收点
    C := dict( Edge(u,v) : volume)
    w := dict( Edge(u,v) : cost)
    f_sum := 最大流量
    w_sum := 最大费用
    F := dict( Edge(u,v) : flow)
    """

    '''
    Step One: 生成初始流值, 并计算总费用和流量
    '''
    if F == None:
        F = dict(zip(list(E), [0]*len(E)))
    
    f_sum_now = sum([F[e] for e in E if e[0] == vs])
    w_sum_now = sum([F[e]*w[e] for e in E])
    if f_sum_now >= f_sum or w_sum_now >= w_sum:
        return F
    '''
    Step Two: 寻找最小费用路， 直到达到指定流量 or 达到设定费用

    '''
    while True:
        V, E_D, C_D, w_D = D_f(V, E, C, F, w) # 得到剩余网络
        U, R = floyd(V, E_D, w_D)# 得到最短费用路
        minimum_road = set()
        u = vs
        while R[(u, vt)] != vt:
            minimum_road.add((u, R[(u, vt)]))
            u = R[(u, vt)]
        minimum_road.add((u, vt))
        # 判断最短路是否存在
        if len(minimum_road) == 1 and list(minimum_road)[0] not in C_D.keys():
            break

        print('最小费用路：', minimum_road) 
        flow_delta = min([C_D[e] for e in minimum_road])
        w_delta = sum([w_D[e] for e in minimum_road])
        #print('流量{0}, 费用{1}'.format(C_D, w_D))
        print(f_sum_now, w_sum_now)
        # 加流
        if f_sum_now + flow_delta > f_sum:
            flow_delta = abs(f_sum-f_sum_now)
        if flow_delta > int((w_sum - w_sum_now)/w_delta):
            flow_delta = int((w_sum - w_sum_now)/w_delta)
        if flow_delta == 0:
            flow_delta = 1
        # 判断是否加满
        if f_sum_now + flow_delta > f_sum or w_sum_now + w_delta * flow_delta > w_sum:
            break
        else:
            f_sum_now = f_sum_now + flow_delta
            w_sum_now = w_sum_now + w_delta * flow_delta
            for e in minimum_road:
                F[e] = F[e] + flow_delta

    return F

if __name__ == '__main__':    
    V = set(['vs',1,2,3, 'vt'])
    E = {(1, 2), (3, 2), (1, 3), ('vs', 3), ('vs', 1), (2, 'vt'), (3, 'vt')}
    vs = 'vs'
    vt = 'vt'
    C = dict({('vs',1):3, ('vs',3):2,(1,2):3, (1,3):1, (3,2):2, (3,'vt'):3, (2,'vt'):3})
    w = dict({('vs',1):2, ('vs',3):3,(1,2):4, (1,3):1, (3,2):5, (3,'vt'):2, (2,'vt'):1})
    f_sum = 2 # 设定流量
    w_sum = 20 # 设定总费用
    F = min_cost_path(V, E, vs, vt, C, w, f_sum, w_sum)
    print('可行流',F, '\n流量', sum([F[i] for i in F.keys() if i[0] == vs]))
