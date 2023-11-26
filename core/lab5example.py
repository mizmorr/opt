from core.lab5 import BeeAlgorithm

n_bees = 50
n_dim = 2
max_epochs = 1000
target_fitness = 1e-5
elite_sites = 2
patch_size = 0.1
search_space = (-5.0, 5.0)

def rosenbrock_2(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2

def callback_func(epoch, iteration_data):
    print(f"Iteration {epoch + 1}:")
    for x, y, z in iteration_data:
        print(f"x: {x}, y: {y}, z: {z}")
    print()


bee_algorithm = BeeAlgorithm(n_bees, n_dim, max_epochs, target_fitness, elite_sites, patch_size, search_space, fitness_func=rosenbrock_2, callback_func=callback_func)
bee_algorithm.run()