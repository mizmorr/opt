from lab6 import AIS
from quadratic.optfuncs import *
# Пример использования:
# objective_function - функция
# num_agents, num_clones - количество агентов и клонов
# num_elite, num_elite_clones - количество лучших агентов и клонов, которые сохраняются на каждом шаге
# x_range, y_range - диапазон начальных значений x и y
# mutation_coefficient - коэффициент для изменения координат клонов на каждом шаге

ais = AIS(rosenbrock_2, num_agents=50, num_clones=5, num_elite=20, num_elite_clones=10,
          x_range=-5, y_range=-5)

iter_number = 10000

for i in range(iter_number):
    ais.evolve(1/(i+1))

    for ag in ais.agents:
        print(ag[0], ag[1], ag[2])

    b = ais.get_best_agent()
    print("Best:"+str(b))