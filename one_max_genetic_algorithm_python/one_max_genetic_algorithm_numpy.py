from typing import Tuple
import numpy as np


# Create a single instance of default_rng
gen = np.random.default_rng(seed=None)


def set_seed() -> None:
    global gen
    gen = np.random.default_rng(seed=None)


def random_genome(length: int) -> np.ndarray:
    return gen.integers(0, 2, size=length, dtype=np.int8)


def init_population(population_size: int, genome_length: int) -> np.ndarray:
    return np.array([random_genome(genome_length) for _ in range(population_size)])


def get_genome_fitness(genome: np.ndarray) -> float:
    return np.sum(genome) / len(genome)


def calculate_population_fitnesses(population: np.ndarray) -> np.ndarray:
    return np.mean(population, axis=1)


def get_target_fitness() -> int:
    return 1


def get_best_fitness(fitness_values: np.ndarray) -> float:
    return np.max(fitness_values) if len(fitness_values) > 0 else 0.0


def get_generation_fitness(fitness_values: np.ndarray, population_size: int) -> float:
    return np.sum(fitness_values) / population_size if population_size != 0 else 0.0


def select_parent(population: np.ndarray, fitness_values: np.ndarray, mode: str = "tournament") -> np.ndarray:
    if mode.lower() == "tournament" or mode.lower() not in ["roulette", "tournament"]:
        tournament_size: int = gen.integers(int(len(population) * 0.6), int(len(population) * 0.8) + 1)
        tournament_size = tournament_size if tournament_size > 1 else 1
        return select_parent_tournament(population, fitness_values, tournament_size)
    else:
        return select_parent_roulette(population, fitness_values)


def select_parent_tournament(population: np.ndarray, fitness_values: np.ndarray, tournament_size: int) -> np.ndarray:
    # Tournament implementation
    random_idx = gen.choice(population.shape[0], size=tournament_size, replace=False)
    selected_idx = random_idx[np.argmax(fitness_values[random_idx])]
    return population[selected_idx]


def select_parent_roulette(population: np.ndarray, fitness_values: np.ndarray) -> np.ndarray:
    # Roulette wheel implementation
    total_fitness = np.sum(fitness_values)
    pick = gen.uniform(0, total_fitness)
    current = 0
    for individual, fitness_value in zip(population, fitness_values):
        current += fitness_value
        if current > pick:
            return individual
    return population[0]


def crossover(parent1: np.ndarray, parent2: np.ndarray, crossover_rate: float) -> Tuple[np.ndarray, np.ndarray]:

    if gen.random() < crossover_rate:
        crossover_point = gen.integers(1, len(parent1))
        return np.concatenate((parent1[:crossover_point], parent2[crossover_point:]), axis=0), np.concatenate((parent2[:crossover_point], parent1[crossover_point:]), axis=0)
    else:
        return parent1.copy(), parent2.copy()


def mutate(genome: np.ndarray, mutation_rate: float) -> np.ndarray:
    mask = gen.random(size=len(genome)) < mutation_rate
    genome[mask] = 1 - genome[mask]
    return genome


def print_best_values(fitness_values: np.ndarray, population: np.ndarray, generation_fitness: float) -> None:
    best_index = np.argmax(fitness_values)
    best_solution = population[best_index]
    print(f"Best Final Solution: {best_solution}")
    print(f"Best Final Fitness: {get_genome_fitness(best_solution)}")
    print(f"Generation perfect fitness percentage: {generation_fitness:.2f}")


def create_new_population(population_size: int, population: np.ndarray,
                          fitness_values: np.ndarray, select_parent_mode: str,
                          crossover_rate: float, mutation_rate: float) -> np.ndarray:

    new_population = np.empty_like(population)

    for i in range(0, population_size, 2):
        parent1 = select_parent(population, fitness_values, mode=select_parent_mode)
        parent2 = select_parent(population, fitness_values, mode=select_parent_mode)
        offspring1, offspring2 = crossover(parent1, parent2, crossover_rate)
        new_population[i] = mutate(offspring1, mutation_rate)
        new_population[i+1] = mutate(offspring2, mutation_rate)

    if population_size % 2 != 0:
        parent = select_parent(population, fitness_values, mode=select_parent_mode)
        new_population[-1] = mutate(parent, mutation_rate)

    return new_population


def genetic_algorithm(population_size: int = 100, genome_length: int = 50,
                      max_generations: int = 1000, mutation_rate: float = 0.02,
                      crossover_rate: float = 0.7, select_parent_mode: str = "tournament",
                      target_generation_fitness: float = 0.9, verbose: bool = False) -> Tuple[int, float, float]:

    set_seed()

    target_fitness = get_target_fitness()
    population = init_population(population_size, genome_length)
    best_population = population
    fitness_values = calculate_population_fitnesses(population)

    best_generation_fitness = 0

    for generation in range(max_generations):
        population = create_new_population(population_size, population, fitness_values, select_parent_mode, crossover_rate, mutation_rate)
        fitness_values = calculate_population_fitnesses(population)
        generation_fitness = get_generation_fitness(fitness_values, population_size)
        best_gen_fitness = get_best_fitness(fitness_values)

        if verbose:
            print(f"Generation {generation}: Best Fitness = {best_gen_fitness} Generation Fitness Percentage: {generation_fitness:.2f}")

        if generation_fitness >= best_generation_fitness:
            best_population = population
            best_generation = generation
            best_generation_fitness = generation_fitness
            best_fitness = best_gen_fitness

        if generation_fitness >= target_generation_fitness and best_gen_fitness == target_fitness:
            if verbose:
                print(f"Ideal solution found in generation {generation}.")
                print_best_values(fitness_values, population, generation_fitness)
            return generation, generation_fitness, best_gen_fitness  # Early return

    if verbose:
        best_fitness_values = calculate_population_fitnesses(best_population)
        print(f"Best solution found after {max_generations} generations was generation number {best_generation}.")
        print_best_values(best_fitness_values, best_population, best_generation_fitness)

    return max_generations, best_generation_fitness, best_fitness
