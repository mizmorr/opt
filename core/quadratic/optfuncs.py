import numpy as np
def himmelblau(x):
    return np.sum(2 * x[:-1] ** 2 + 3 * x[1:] ** 2 + 4 * x[:-1] * x[1:] - 6 * x[:-1] - 3 * x[1:], axis=0)
def himmelblau_2(x, y):
    return 2 * x * x + 3 * y * y + 4 * x * y - 6 * x - 3 * y
def rosenbrock(x):
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0, axis=0)
def rosenbrock_2(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2
def rastrigin(x):
    return np.sum(x[1:] ** 2 - 10 * np.cos(2 * np.pi * x[1:]) + x[:-1] ** 2 - 10 * np.cos(2 * np.pi * x[:-1]), axis=0)
def rastrigin_2(x, y):
    return x ** 2 - 10 * np.cos(2 * np.pi * x) + y ** 2 - 10 * np.cos(2 * np.pi * y)
def hypersphere_2(x, y):
    return x ** 2 + y ** 2