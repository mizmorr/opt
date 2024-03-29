import numpy as np
import numdifftools as nd

def partial_function(f___, input, pos, value):
    tmp = input[pos]
    input[pos] = value
    ret = f___(*input)
    input[pos] = tmp
    return ret

def dist(x1,y1,x0,y0):
    return np.sqrt((x1-x0)**2+(y1-y0)**2)

def gradient(function, input):

    ret = np.empty(len(input))
    for i in range(len(input)):
        fg = lambda x: partial_function(function, input, i, x)
        ret[i] = nd.Derivative(fg)(input[i])
    return ret

def next_point(x, y, gx, gy, step) -> tuple:
    return x - step * gx, y - step * gy

def grad_desc(function, x0, y0, tk, M):
    yield x0, y0, 0, function(x0, y0)

    e1=0.000001
    e2=0.000001

    k=0
    while True:
        (gx, gy) = gradient(function, [x0,y0])
        if np.linalg.norm((gx,gy))<e1:
            break

        if k>=M:
            break
        x1, y1 = next_point(x0, y0, gx, gy, tk)
        f1 = function(x1, y1)
        f0 = function(x0, y0)
        while not f1 < f0:  # 8 условие
            tk = tk / 2
            x1, y1 = next_point(x0, y0, gx, gy, tk)
            f1 = function(x1, y1)
            f0 = function(x0, y0)

        if dist(x1, y1, x0, y0)<e2 and abs(f1-f0)<e2:
            x0, y0 = x1, y1
            break
        else:
            k+=1
            x0, y0 = x1, y1
            yield x0, y0, k, f1


