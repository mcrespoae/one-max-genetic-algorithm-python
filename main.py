# One max problem solved with a genetic algorithm

import random
from tqdm import tqdm
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from timeit_functions import timeit
from results import Results
from helper import generate_equally_spaced_values

RUN_TIMES: int = 70
GENERATIONS: int = 1000
POPULATION_SIZE: int = 100
GENOME_LENGTH: int = 50
SELECT_PARENT_MODE: str = "tournament"  # tournament or roulette
TARGET_GENERATION_FITNESS: float = 0.9
MUTATION_RATE_MIN: float = 0.01
MUTATION_RATE_MAX: float = 0.1
CROSSOVER_RATE_MIN: float = 0.5
CROSSOVER_RATE_MAX: float = 0.8


def random_genome(length: int) -> List[int]:
    return [random.randint(0, 1) for _ in range(length)]


def init_population(population_size: int, genome_length: int) -> List[List[int]]:
    return [random_genome(genome_length) for _ in range(population_size)]


def calculate_population_fitnesses(population: List[List[int]]) -> List[float]:
    return [get_genome_fitness(genome) for genome in population]


def get_target_fitness() -> int:
    return 1


def get_genome_fitness(genome: List[int]) -> float:
    return sum(genome) / GENOME_LENGTH


def get_best_fitness(fitness_values: List[float]) -> float:
    return max(fitness_values)


def get_generation_fitness(fitness_values: List[float]) -> float:
    return sum(fitness_values) / (POPULATION_SIZE)


def select_parent(population: List[List[int]], fitness_values: List[float], mode: str = "roulette") -> List[int]:
    if mode.lower() == "roulette" or mode.lower() not in ["roulette", "tournament"]:
        return select_parent_roulette(population, fitness_values)
    else:
        tournament_size: int = random.randint(int(POPULATION_SIZE * 0.6), int(POPULATION_SIZE * 0.8))
        return select_parent_tournament(population, fitness_values, tournament_size)


def select_parent_tournament(population: List[List[int]], fitness_values: List[float], tournament_size: int) -> List[int]:
    # Tournament implementation
    selected_candidates = random.sample(list(zip(population, fitness_values)), tournament_size)
    winner = max(selected_candidates, key=lambda x: x[1])  # Select the candidate with the highest fitness
    return winner[0]  # Return the selected individual from the winning tournament


def select_parent_roulette(population: List[List[int]], fitness_values: List[float]) -> List[int]:
    # Roulette wheel implementation
    total_fitness = sum(fitness_values)
    pick = random.uniform(0, total_fitness)  # TO DO, select better parents
    current = 0
    for individual, fitness_value in zip(population, fitness_values):
        current += fitness_value
        if current > pick:
            return individual


def crossover(parent1: List[int], parent2: List[int], crossover_rate: float) -> Tuple[List[int], List[int]]:
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:], parent2[:crossover_point] + parent1[crossover_point:]
    else:
        return parent1, parent2


def mutate(genome: List[int], mutation_rate: float) -> List[int]:
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            genome[i] = abs(genome[1] - 1)
    return genome


def print_best_values(fitness_values: List[float], population: List[List[int]], generation_fitness: float) -> None:
    best_index = fitness_values.index(get_best_fitness(fitness_values))
    best_solution = population[best_index]
    print(f"Best Final Solution: {best_solution}")
    print(f"Best Final Fitness: {get_genome_fitness(best_solution)}")
    print(f"Generation perfect fitness percentage: {generation_fitness:.2f}")


def genetic_algorithm(mutation_rate: float = 0.02, crossover_rate: float = 0.7, verbose: bool = False) -> Tuple[int, float, float]:
    target_fitness = get_target_fitness()
    population = init_population(POPULATION_SIZE, GENOME_LENGTH)
    fitness_values = calculate_population_fitnesses(population)

    for generation in range(GENERATIONS):
        new_population = []

        for _ in range(POPULATION_SIZE // 2):
            # Tournament mode converges way faster than roulette
            parent1 = select_parent(population, fitness_values, mode=SELECT_PARENT_MODE)
            parent2 = select_parent(population, fitness_values, mode=SELECT_PARENT_MODE)
            offspring1, offspring2 = crossover(parent1, parent2, crossover_rate)
            new_population.extend([mutate(offspring1, mutation_rate), mutate(offspring2, mutation_rate)])

        population = new_population
        prev_generation_fitness = get_generation_fitness(fitness_values)
        fitness_values = calculate_population_fitnesses(population)
        generation_fitness = get_generation_fitness(fitness_values)
        best_gen_fitness = get_best_fitness(fitness_values)

        if verbose:
            print(f"Generation {generation}: Best Fitness = {best_gen_fitness} Generation Fitness Percentage: {generation_fitness:.2f}")

        if generation_fitness >= prev_generation_fitness:
            best_population = population
            best_generation = generation
            best_generation_fitness = generation_fitness
            best_fitness = best_gen_fitness

        if best_gen_fitness == target_fitness and generation_fitness >= TARGET_GENERATION_FITNESS:
            if verbose:
                print(f"Ideal solution found in generation {generation}.")
                print_best_values(fitness_values, population, generation_fitness)
            return generation, generation_fitness, best_fitness  # Early return

    best_fitness_values = calculate_population_fitnesses(best_population)
    if verbose:
        print(f"Best solution found after {GENERATIONS} generations was generation number {best_generation}.")
        print_best_values(best_fitness_values, best_population, best_generation_fitness)
    return GENERATIONS, best_generation_fitness, best_fitness


def process_genetic_algorithm(mutation_rate_values: List[float], crossover_rate_values: List[float]):
    total_iterations = len(mutation_rate_values) * len(crossover_rate_values)
    progress_bar = tqdm(total=total_iterations, desc="Processing")
    best_mutation_rate = 0
    best_crossover_rate = 0
    prev_best_score = 0

    for mutation_rate in mutation_rate_values:

        prev_local_score = 0
        results = Results(max_generations=GENERATIONS)

        for i, crossover_rate in enumerate(crossover_rate_values):
            progress_bar.set_description(f"Score:{prev_best_score:.2f}")

            with ThreadPoolExecutor(max_workers=None) as executor:
                future_tasks = [executor.submit(genetic_algorithm, mutation_rate, crossover_rate) for _ in range(RUN_TIMES)]
                for future in future_tasks:
                    generation, generation_fitness, best_fitness = future.result()
                    results.add_result(generation, generation_fitness, best_fitness)

            score = results.get_score()
            # General score check
            if score >= prev_best_score:
                best_mutation_rate = mutation_rate
                best_crossover_rate = crossover_rate
                best_result = results
                prev_best_score = score

            if prev_local_score < score and i != 0:  # Skip this loop since
                progress_bar.update(len(crossover_rate_values) - i)
                break

            prev_local_score = score
            results = Results(max_generations=GENERATIONS)
            progress_bar.update(1)

        if results.score >= 0.99:  # Check if perfect score to close the algorithm execution
            progress_bar.update(len(crossover_rate_values))
            break

    progress_bar.set_description(f"Score: {best_result.score:.2f}")
    progress_bar.close()
    print("-" * 50)
    print("\tBest results")
    print("-" * 50)
    print(f"Best Mutation Rate: {best_mutation_rate}\nBest Crossover Rate: {best_crossover_rate}")
    print(f"{best_result}")


# @timeit
def main() -> None:

    mutation_rate_values = generate_equally_spaced_values(min_val=MUTATION_RATE_MIN, max_val=MUTATION_RATE_MAX, length=10)
    crossover_rate_values = generate_equally_spaced_values(min_val=CROSSOVER_RATE_MIN, max_val=CROSSOVER_RATE_MAX, length=10)

    print(f"""Running {RUN_TIMES} times the one max problem with genetic algorithms for:
        Generations:{GENERATIONS:>16}
        Population Size:{POPULATION_SIZE:>12}
        Genome Length:{GENOME_LENGTH:>14}
        Parent selection mode: {SELECT_PARENT_MODE}
        Mutation Rate:  {mutation_rate_values[0]:>9} to {mutation_rate_values[-1]}
        Crossover Rate: {crossover_rate_values[0]:>9} to {crossover_rate_values[-1]}
        {"-" * 50}""")

    process_genetic_algorithm(mutation_rate_values, crossover_rate_values)


if __name__ == "__main__":
    main()
