def unoriented_Euler(V, E):
    """
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    
    Returns:
    W := set( u, Edge(u,v), v )
    """
    # 判断是否存在Euler闭迹
    dev = dict(zip(list(V), [0] * len(V)))
    for e in E:
        dev[e[0]] += 1
        dev[e[1]] += 1
    for v in dev.values():
        if v % 2 != 0:
            print('不存在Euler闭迹')
            return None
    vk = list(V)[0]
    v_end = vk
    v = vk
    Wk = [vk]
    Gk = E
    E_add = set([])
    while True:
        # 选取一条与v关联的边e
        for e in Gk:
            if v in list(e):
                v_new = list(set(e) - {v})[0]
                break
        Wk.append(e)
        Wk.append(v_new)
        Gk = Gk- {e}
        if e in E_add:
            E_add = E_add - {e}
        else:
            Gk = Gk - {e}

        if v_new == v_end:
            'Gk为空图'
            if len(Gk) == 0:
                break
            else:
                #Wk.append('开始下一个欧拉环游')
                #v =[e[0] for e in Gk][0]
                #v_end = v
                v = v_new
        else:
            v = v_new
    return Wk

def oriented_Euler(V, E):
    """
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    
    Returns:
    W := set( u, Edge(u,v), v )
    """
    # 判断是否存在Euler闭迹
    dev_in = dict(zip(list(V), [0] * len(V)))
    dev_out = dict(zip(list(V), [0] * len(V)))
    for e in E:
        dev_in[e[0]] += 1
        dev_out[e[1]] += 1
    for v in list(dev_in.values()) + list(dev_out.values()):
        if v % 2 != 0:
            print('不存在Euler闭迹')
            return None

    vk = list(V)[0]
    v_end = vk
    v = vk
    Wk = [vk]
    Gk = E
    E_add = set([])
    while True:
        # 选取一条与v关联的边e
        for e in Gk:
            if v == e[0]:
                v_new = e[1]
                break
        Wk.append(e)
        Wk.append(v_new)
        Gk = Gk- {e}
        if e in E_add:
            E_add = E_add - {e}
        else:
            Gk = Gk - {e}

        if v_new == v_end:
            'Gk为空图'
            if len(Gk) == 0:
                break
            else:
                Wk.append('开始下一个欧拉环游')
                v =[e[0] for e in Gk][0]
                v_end = v

        else:
            v = v_new
    return Wk
if __name__ == '__main__':
    V = {1, 2, 3, 4, 5, 6, 7, 8} 
    E = {(1, 2), (1, 3), (1, 4), (1, 6), 
        (2, 3), (2, 4), (2, 5), 
        (3, 5), (3, 8),
        (4, 6), (4, 7),
        (5, 7), (5, 8),
        (6, 7), (6, 8),
        (7, 8)}
    W = unoriented_Euler(V, E)
    print('-'.join(map(str, W)))

    V = {1, 2, 3, 4, 5, 6, 7, 8} 
    E = {(1, 2), (1, 3), (1, 4), (1, 6), 
        (2, 3), (2, 4), (2, 5), 
        (3, 5), (3, 8),
        (4, 6), (4, 7),
        (5, 7), (5, 8),
        (6, 7), (6, 8),
        (7, 8)}

    W = oriented_Euler(V, E)
    print('-'.join(map(str, W)))