import random
import numpy as np

def rosenbrock_2(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2

class GeneticAlg:
    def __init__(self, func, generations=42, min_value=True, mut_prob=0.71, survive_rate=0.77, population_size=123):
        self.funky = func
        self.population = dict()
        self.mut_prob = mut_prob
        self.survive_rate = survive_rate
        self.generations = generations
        self.population_size = population_size
        self.minimal = min_value

    def initialize_population(self, a, b):
        for i in range(self.population_size):
            x_gene = random.uniform(-a, a)
            y_gene = random.uniform(-b, b)
            self.population[i] = [x_gene, y_gene, self.funky(x_gene, y_gene)]

    def data_summary(self):
        return [max(self.population.items(), key=lambda item: item[1][2]),
                min(self.population.items(), key=lambda item: item[1][2])]

    def choose_candidates(self):
        sorted_folks = dict(
            sorted(self.population.items(), key=lambda item: item[1][2], reverse=self.minimal))

        threshold = int(self.population_size * (1 - self.survive_rate))
        parents_group1 = list(sorted_folks.items())[threshold: threshold * 2]
        parents_group2 = list(sorted_folks.items())[self.population_size - threshold: self.population_size]

        i = 0
        for person in sorted_folks.values():
            if random.random() > 0.5:
                person[0] = parents_group1[i][1][0]
                person[1] = parents_group2[i][1][1]
                person[2] = self.funky(parents_group1[i][1][0], parents_group2[i][1][1])
            else:
                person[0] = parents_group2[i][1][0]
                person[1] = parents_group1[i][1][1]
                person[2] = self.funky(parents_group2[i][1][0], parents_group1[i][1][1])
            i += 1
            if i >= threshold:
                break

        self.population = sorted_folks

    def make_mutations(self, current_generation):
        for person in self.population.values():
            if random.random() < self.mut_prob:
                person[0] += (random.random() - 0.5) * ((self.generations - current_generation) / self.generations)
            if random.random() < self.mut_prob:
                person[1] += (random.random() - 0.5) * ((self.generations - current_generation) / self.generations)
            person[2] = self.funky(person[0], person[1])

