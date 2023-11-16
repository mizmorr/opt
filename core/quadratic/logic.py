from scipy.optimize import minimize
import numpy as np

def sqMethod(x, y):
    #   global points
    points = []

    def fun(x_i):  # Функция
        x1 = x_i[0]
        x2 = x_i[1]
        return 2 * x1 * x1 + 3 * x2 * x2 + 4 * x1 * x2 - 6 * x1 - 3 * x2

    def callback(x_w):
        g_list = np.ndarray.tolist(x_w)
        g_list.append(fun(x_w))
        points.append(g_list)

    b = (0, float("inf"))
    bounds = (b, b)
    x0 = (x, y)  # начальная точка
    con = {'type': 'eq', 'fun': fun}

    # вот тут основной движ
    res = minimize(fun, x0, method="SLSQP", bounds=bounds,
                   constraints=con, callback=callback)

    glist = np.ndarray.tolist(res.x)
    glist.append(res.fun)
    points.append(glist)

    for iteration, point in enumerate(points):
        yield iteration, point