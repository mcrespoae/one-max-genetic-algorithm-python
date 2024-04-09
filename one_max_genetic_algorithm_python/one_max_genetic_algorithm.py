import random
from typing import List, Tuple

def random_genome(length: int) -> List[int]:
    return [random.randint(0, 1) for _ in range(length)]


def init_population(population_size: int, genome_length: int) -> List[List[int]]:
    return [random_genome(genome_length) for _ in range(population_size)]


def get_genome_fitness(genome: List[int]) -> float:
    return sum(genome) / len(genome)


def calculate_population_fitnesses(population: List[List[int]]) -> List[float]:
    return [get_genome_fitness(genome) for genome in population]


def get_target_fitness() -> int:
    return 1


def get_best_fitness(fitness_values: List[float]) -> float:
    return max(fitness_values) if fitness_values else 0.0

def get_generation_fitness(fitness_values: List[float], population_size: int) -> float:
    return sum(fitness_values) / (population_size) if population_size != 0 else 0


def select_parent(population: List[List[int]], fitness_values: List[float], mode: str = "roulette") -> List[int]:
    if mode.lower() == "roulette" or mode.lower() not in ["roulette", "tournament"]:
        return select_parent_roulette(population, fitness_values)
    else:
        tournament_size: int = random.randint(int(len(population) * 0.6), int(len(population) * 0.8))
        return select_parent_tournament(population, fitness_values, tournament_size)


def select_parent_tournament(population: List[List[int]], fitness_values: List[float], tournament_size: int) -> List[int]:
    # Tournament implementation
    selected_candidates = random.sample(list(zip(population, fitness_values)), tournament_size)
    winner = max(selected_candidates, key=lambda x: x[1])  # Select the candidate with the highest fitness
    return winner[0]  # Return the selected individual from the winning tournament


def select_parent_roulette(population: List[List[int]], fitness_values: List[float]) -> List[int]:
    # Roulette wheel implementation
    total_fitness = sum(fitness_values)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness_value in zip(population, fitness_values):
        current += fitness_value
        if current > pick:
            return individual
    return population[0]


def crossover(parent1: List[int], parent2: List[int], crossover_rate: float) -> Tuple[List[int], List[int]]:
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:], parent2[:crossover_point] + parent1[crossover_point:]
    else:
        return parent1, parent2


def mutate(genome: List[int], mutation_rate: float) -> List[int]:
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            genome[i] = abs(genome[i] - 1)
    return genome


def print_best_values(fitness_values: List[float], population: List[List[int]], generation_fitness: float) -> None:
    best_index = fitness_values.index(get_best_fitness(fitness_values))
    best_solution = population[best_index]
    print(f"Best Final Solution: {best_solution}")
    print(f"Best Final Fitness: {get_genome_fitness(best_solution)}")
    print(f"Generation perfect fitness percentage: {generation_fitness:.2f}")


def genetic_algorithm(population_size: int = 100, genome_length: int = 50,
                      max_generations: int = 1000, mutation_rate: float = 0.02,
                      crossover_rate: float = 0.7, select_parent_mode: str = "tournament",
                      target_generation_fitness: float = 0.9, verbose: bool = False) -> Tuple[int, float, float]:

    target_fitness = get_target_fitness()
    population = init_population(population_size, genome_length)
    fitness_values = calculate_population_fitnesses(population)

    for generation in range(max_generations):
        new_population = []

        for _ in range(population_size // 2):
            # Tournament mode converges way faster than roulette
            parent1 = select_parent(population, fitness_values, mode=select_parent_mode)
            parent2 = select_parent(population, fitness_values, mode=select_parent_mode)
            offspring1, offspring2 = crossover(parent1, parent2, crossover_rate)
            new_population.extend([mutate(offspring1, mutation_rate), mutate(offspring2, mutation_rate)])

        population = new_population
        prev_generation_fitness = get_generation_fitness(fitness_values, population_size)
        fitness_values = calculate_population_fitnesses(population)
        generation_fitness = get_generation_fitness(fitness_values, population_size)
        best_gen_fitness = get_best_fitness(fitness_values)

        if verbose:
            print(f"Generation {generation}: Best Fitness = {best_gen_fitness} Generation Fitness Percentage: {generation_fitness:.2f}")

        if generation_fitness >= prev_generation_fitness:
            best_population = population
            best_generation = generation
            best_generation_fitness = generation_fitness
            best_fitness = best_gen_fitness

        if best_gen_fitness == target_fitness and generation_fitness >= target_generation_fitness:
            if verbose:
                print(f"Ideal solution found in generation {generation}.")
                print_best_values(fitness_values, population, generation_fitness)
            return generation, generation_fitness, best_fitness  # Early return

    best_fitness_values = calculate_population_fitnesses(best_population)
    if verbose:
        print(f"Best solution found after {max_generations} generations was generation number {best_generation}.")
        print_best_values(best_fitness_values, best_population, best_generation_fitness)
    return max_generations, best_generation_fitness, best_fitness
