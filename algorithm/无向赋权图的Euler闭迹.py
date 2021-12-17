def floyd(V, E, w, oriented = True, INF = float("inf")):
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
    if not oriented:
        E_unchange = E.copy()
        for e in E_unchange:
            E.add((e[1], e[0]))
            w[(e[1], e[0])] = w[e]
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
        # 判断最短路是否存在, 修改？
        if len(minimum_road) == 1:
            break

        #print('最小费用路：', minimum_road) 
        flow_delta = min([C_D[e] for e in minimum_road])
        w_delta = sum([w_D[e] for e in minimum_road])
        #print('流量{0}, 费用{1}'.format(C_D, w_D))
        #print(f_sum_now, w_sum_now)
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

def unoriented_weight_Euler(V, E, W):
    """
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    w := dict( Edge(u,v) : cost)
    
    Returns:
    W := set( u, Edge(u,v), v )
    """
    E_origin = E.copy()
    #print(id(E_origin), id(E))
    # 判断是否存在Euler闭迹
    dev = dict(zip(list(V), [0] * len(V)))
    for e in E:
        dev[e[0]] += 1
        dev[e[1]] += 1

    v_odd = set([])# 奇点集合
    for v in V:
        if dev[v] % 2 != 0:
            v_odd.add(v)
            
    if len(v_odd) != 0:
        print('不存在Euler闭迹, 需要添加边')
        '求出最短路，构造完全图F'
        U, R = floyd(V, E, W, oriented = False)

        F = dict()
        for u in v_odd:
            for v in v_odd:
                if u != v:
                    F[(u,v)] = U[(u, v)]
        #print(F) # 输出最短路
        '求出最大匹配M'
        import itertools
        M_F = sum(F.values())
        M_ouput = F
        for X in itertools.permutations(list(v_odd), int(len(v_odd)/2)):
            X = set(X)
            Y = v_odd - X
            vs, vt = 'vs', 'vt'
            # 增加收点和发点
            F_change = dict()
            C_change = dict()
            for v in X:
                F_change[(vs, v)] = 0
                C_change[(vs, v)] = 1
            for v in Y:
                F_change[(v, vt)] = 0
                C_change[(v, vt)] = 1
            for (u, v) in F.keys():
                if u in X and v in Y:
                    C_change[(u, v)] = 1
                    F_change[(u, v)] = F[(u,v)]
            v_odd_copy = v_odd.copy()
            v_odd_copy.update({'vs', 'vt'})
            M = min_cost_path(V = v_odd_copy, E = set(F_change.keys()), vs = vs, vt = vt, C = C_change, w = F_change, f_sum = int(1e+04), w_sum = int(1e+10))
            M_F_now = sum([F_change[m] for m in M if M[m] > 0])

            if M_F_now < M_F and sum(M.values()) == len(X) * 3:
                M_ouput = M
                M_F = M_F_now

        M = M_ouput
        print(M) # 输出添加的边
        print('原始的边：', E_origin)
        # 出现了重弧，将E转化为字典
        E_dict = dict()
        for e in E_origin:
            E_dict[e] = 1
        print('添加边并且转化为字典：', E_dict)

        for (u, v) in M:
            if M[(u, v)] > 0 and len(set([vs, vt]) - set([u, v])) == 2:
                while True:
                    if (u, R[(u, v)]) in E_origin:
                        E_dict[(u, R[(u, v)])] += 1
                    else:
                        E_dict[(R[(u, v)], u)] += 1
                
                    if R[(u, v)] == v:
                        break
                    u = R[(u, v)]
    print('添加边并且转化为字典：', E_dict)
    vk = list(V)[0]
    vk = 1
    v_end = vk
    v = vk
    Wk = [vk]
    Gk = E_dict

    while True:
        # 选取一条与v关联的边e
        for e in Gk.keys():
            if Gk[e] > 0 and v in list(e):
                v_new = list(set(e) - {v})[0]
                break
        Wk.append(e)
        Wk.append(v_new)
        Gk[e] += -1

        if v_new == v_end:
            'Gk为空图'
            if sum(Gk.values()) == 0:
                break
            else:
                if len([e for e in Gk if Gk[e] > 0 and v_new in list(e)]) == 0:
                    Wk.append('开始下一个欧拉环游')
                    v =[e[0] for e in Gk if Gk[e] > 0][0]
                    v_end = v
                    Wk.append(v)
                else:
                    v = v_new
        else:
            v = v_new
    return Wk

if __name__ == '__main__':
    V = {1, 2, 3, 4, 5, 6, 7, 8} 
    E = {(1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6), (5, 7), (6, 8), (7, 8)}
    W = {(1, 2):1, (1, 3):2, 
        (2, 4): 1, 
        (3, 4):10, (3, 5):5,
        (4, 6):5,
        (5, 6):10, (5, 7):1,
        (6, 8):2,
        (7, 8):2}
    
    Wk = unoriented_weight_Euler(V, E, W)           
    #print(Wk)
    #print('花费：', weight_loss)
    print('-'.join(map(str, Wk)))