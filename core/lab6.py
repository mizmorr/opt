import random
from operator import itemgetter
from quadratic.optfuncs import *


class AIS:
    def __init__(self, objective_function, num_agents, num_clones, num_elite, num_elite_clones, x_range, y_range):
        self.objective_function = objective_function
        self.x_range = float(x_range)
        self.y_range = float(y_range)

        self.num_agents = num_agents
        self.agents = [[random.uniform(-self.x_range, self.x_range), random.uniform(-self.y_range, self.y_range), 0.0]
                       for _ in range(self.num_agents)]
        for agent in self.agents:
            agent[2] = self.objective_function(agent[0], agent[1])

        self.num_elite = num_elite
        self.num_elite_clones = num_elite_clones
        self.num_clones = num_clones

    def evolve(self, mutation_coefficient):
        elite_population = sorted(self.agents, key=itemgetter(2))[:self.num_elite]

        new_population = [clone for elite_agent in elite_population for clone in
                          [elite_agent.copy() for _ in range(self.num_clones)]]

        for new_agent in new_population:
            new_agent[0] += mutation_coefficient * random.uniform(-0.5, 0.5)
            new_agent[1] += mutation_coefficient * random.uniform(-0.5, 0.5)
            new_agent[2] = self.objective_function(new_agent[0], new_agent[1])

        new_population = sorted(new_population, key=itemgetter(2))[:self.num_elite_clones]

        self.agents += new_population
        self.agents = sorted(self.agents, key=itemgetter(2))[:self.num_agents]

    def get_best_agent(self):
        return self.agents[0]
