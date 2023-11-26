import numpy as np


class Bee:
    def __init__(self, position, fitness_func):
        self.position = position
        self.fitness_func = fitness_func
        self.fitness = self.evaluate_fitness()

    def evaluate_fitness(self):
        return self.fitness_func(*self.position)


class BeeAlgorithm:
    def __init__(self, n_bees, n_dim, max_epochs, target_fitness, elite_sites, patch_size, search_space, fitness_func,
                 callback_func=None):
        self.n_bees = n_bees
        self.n_dim = n_dim
        self.max_epochs = max_epochs
        self.target_fitness = target_fitness
        self.elite_sites = elite_sites
        self.patch_size = patch_size
        self.search_space = search_space
        self.fitness_func = fitness_func
        self.callback_func = callback_func

        # Инициализация пчёл
        self.bees = [Bee(position=np.random.uniform(search_space[0], search_space[1], n_dim), fitness_func=fitness_func)
                     for _ in range(n_bees)]

    def employed_bees_phase(self, epoch):
        iteration_data = []
        for i, bee in enumerate(self.bees):
            new_position = bee.position + np.random.uniform(low=-1, high=1, size=self.n_dim) * self.patch_size
            new_position = np.clip(new_position, self.search_space[0], self.search_space[1])

            new_fitness = self.evaluate_fitness(new_position)

            if bee.fitness is None or new_fitness < bee.fitness:
                bee.position = new_position
                bee.fitness = new_fitness

            iteration_data.append((bee.position[0], bee.position[1], bee.fitness))

        # if self.callback_func is not None:
        #     self.callback_func(epoch, iteration_data)

    def evaluate_fitness(self, position):
        return self.fitness_func(*position)

    def onlooker_bees_phase(self, epoch):
        iteration_data = []
        probabilities = np.exp(-np.array([bee.fitness for bee in self.bees]))
        probabilities /= probabilities.sum()

        selected_bees = np.random.choice(self.bees, size=self.n_bees, p=probabilities)

        for i, bee in enumerate(selected_bees):
            new_position = bee.position + np.random.uniform(low=-1, high=1, size=self.n_dim) * self.patch_size
            new_position = np.clip(new_position, self.search_space[0], self.search_space[1])

            new_fitness = self.evaluate_fitness(new_position)

            if bee.fitness is None or new_fitness < bee.fitness:
                bee.position = new_position
                bee.fitness = new_fitness

            iteration_data.append((bee.position[0], bee.position[1], bee.fitness))

        if self.callback_func is not None:
            self.callback_func(epoch, iteration_data)

    def scout_bees_phase(self, epoch):
        iteration_data = []
        for i, bee in enumerate(self.bees):
            if np.random.rand() < 0.01:
                bee.position = np.random.uniform(self.search_space[0], self.search_space[1], self.n_dim)
                bee.fitness = None

        # if self.callback_func is not None:
        #     self.callback_func(epoch, iteration_data)

    def run(self):
        epoch = 0
        while epoch < self.max_epochs:
            self.employed_bees_phase(epoch)
            self.onlooker_bees_phase(epoch)
            self.scout_bees_phase(epoch)

            best_fitness = min([bee.fitness for bee in self.bees if bee.fitness is not None])

            if best_fitness < self.target_fitness:
                print("Target fitness reached. Stopping optimization.")
                break

            epoch += 1
