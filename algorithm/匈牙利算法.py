#!/usr/bin/env python
# -*- coding:utf-8 -*-

def hungarian_methold(X, Y, E, M = None):
    """
    X := set( Vertex(v) )
    Y := set( Vertex(v) )
    E := set( Edge(x,y) )
    M := set( Edge(x,y) )
    return M := set( Edge(x,y) )
    """
    if M == None:
        M = set(list(E)[0])

    # 判断是否存在非饱和点
    if len(set([m[0] for m in M])) == len(X):
        return M

    while True:
        # 查看饱和的M_X 和M_Y
        M_X = set([m[0] for m in M])
        M_Y = set([m[1] for m in M])
        
        unsaturate_dot = X - M_X
        if len(unsaturate_dot) ==0:
            break
        unvisited_dot = dict(zip(list(unsaturate_dot), [True] * len(unsaturate_dot))) 
        label_dot = dict(zip(list(unsaturate_dot), [-1] * len(unsaturate_dot)))

        
        # 检查每一个不饱和点
        while True:
            # 任取一个点
            for x in label_dot.keys():
                if unvisited_dot[x]:
                    break

            for e in E:
                # 将所有和x 
                if e[0] == x and e[1] not in label_dot.keys():
                    label_dot[e[1]] = e[0]

            # 检查是否存在不饱和y点
            if len([y for y in label_dot if y in Y and y not in M_Y]) > 0:
                for y in label_dot:
                    if y in Y and y not in M_Y:
                        break
                P = set()
                while label_dot[y] != -1:
                    P.add((label_dot[y], y))
                    y = label_dot[y]
                P.add((label_dot[y], y))
                break

            unvisited_dot[x] = False
            if len([x for x in unvisited_dot.keys() if unvisited_dot[x]]) == 0:
                P = set() # 没有增广链
                break
        
        M_unchange = M
        M = (M - set([e for e in P if e[0] in Y])) | set([e for e in P if e[0] in X])
        if M == M_unchange:
            break
    return M

if __name__ == '__main__':    
    X = {'x1','x2','x3','x4','x5'}
    Y = {'y1', 'y2', 'y3', 'y4', 'y5'}
    E = {('x1', 'y2'), ('x1', 'y3'), ('x2', 'y1'), ('x2', 'y2'), ('x2', 'y4'), ('x2', 'y5'), 
        ('x3', 'y2'), ('x3', 'y3'), ('x4', 'y2'), ('x4', 'y3'), ('x5', 'y4'), ('x5', 'y5')}

    M = hungarian_methold(X, Y, E, M = {('x1', 'y2')})
    print(M)