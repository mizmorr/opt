from operator import itemgetter

from core.gradient.optfuncs import rosenbrock_2
from core.lab4 import PSO
from core.lab6 import AIS


class HybridAlgorithm:
    def __init__(self, func, population, position_x, position_y, fi_p, fi_g, target_fitness, pso_to_ais_ratio,
                 num_agents, num_clones, num_elite, num_elite_clones, x_range, y_range, mutation_coefficient=0.1,
                 callback_func=None):
        self.pso = PSO(func, population, position_x, position_y, fi_p, fi_g)
        self.ais = AIS(func, num_agents, num_clones, num_elite, num_elite_clones, x_range, y_range)
        self.mutation_coefficient = mutation_coefficient
        self.target_fitness = target_fitness
        self.pso_to_ais_ratio = pso_to_ais_ratio
        self.callback_func = callback_func

    def run(self, num_iterations):
        epoch = 0
        for _ in range(num_iterations):
            iter_data = []
            self.pso.next_iteration()

            # Получение лучшего решения от PSO
            pso_best_solution = min(self.pso.particles, key=itemgetter(2))

            # Обновление AIS с использованием лучшего решения от PSO
            for agent in self.ais.agents:
                if agent[2] > pso_best_solution[2]:
                    agent[0] += self.mutation_coefficient * (pso_best_solution[0] - agent[0])
                    agent[1] += self.mutation_coefficient * (pso_best_solution[1] - agent[1])
                    agent[2] = self.ais.objective_function(agent[0], agent[1])

            # Запуск AIS
            self.ais.evolve(mutation_coefficient=self.mutation_coefficient)

            # Обновление частиц в PSO на основе лучших решений из AIS
            num_particles_to_update = int(self.pso_to_ais_ratio * len(self.pso.particles))
            ais_top_solutions = sorted(self.ais.agents, key=itemgetter(2))[:num_particles_to_update]

            for i in range(num_particles_to_update):
                self.pso.particles[i] = (ais_top_solutions[i][0], ais_top_solutions[i][1],
                                         self.pso.func(ais_top_solutions[i][0], ais_top_solutions[i][1]))
            if ais_top_solutions[0][2] <= self.target_fitness:
                break
            self.mutation_coefficient = max(0.1, 0.1 - 0.09 * (ais_top_solutions[0][2] / self.target_fitness))
            iter_data.append(self.ais.agents)

            if self.callback_func is not None:
                self.callback_func(epoch, iter_data)
            epoch += 1

        ais_best_solution = min(self.ais.agents, key=itemgetter(2))
        return ais_best_solution


def callback_func(epoch, iter_data):
    print(f"Iteration {epoch + 1}:")
    for iteration_data in iter_data:
        for x, y, z in iteration_data:
            print(f"x: {x}, y: {y}, z: {z}")
    print()


# Пример использования гибридного алгоритма
hybrid_algo = HybridAlgorithm(
    func=rosenbrock_2,
    population=20,
    position_x=5,
    position_y=5,
    fi_p=3.0,
    fi_g=2.0,
    target_fitness=0.000001,
    pso_to_ais_ratio=0.3,
    num_agents=10,
    num_clones=5,
    num_elite=2,
    num_elite_clones=3,
    x_range=5,
    y_range=5,
    mutation_coefficient=0.1,
    callback_func=callback_func
)


result = hybrid_algo.run(num_iterations=1000)
print("Optimal solution:", result)
