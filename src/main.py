# One max problem solved with a genetic algorithm
import argparse
from concurrent.futures import ProcessPoolExecutor
from os import cpu_count
from typing import List

from tqdm import tqdm

from results import Results
from timeit_functions import timeit
from utils import generate_equally_spaced_values

RUN_TIMES: int = 8
GENERATIONS: int = 400
POPULATION_SIZE: int = 50
GENOME_LENGTH: int = 35
SELECT_PARENT_MODE: str = (
    "tournament"  # tournament or roulette. Tournament usually converges faster and yields better results.
)
TARGET_GENERATION_FITNESS: float = (
    0.998  # When a generation is considered fit enough to skip the next iterations. Values close to 1.0 will yield better results.
)
TARGET_PROBLEM_FITNESS: float = (
    0.999  # When the problem is marked as solved. Values very close to 1.0 will not stop the execution.
)
MUTATION_RATE_MIN: float = 0.001
MUTATION_RATE_MAX: float = 0.01
CROSSOVER_RATE_MIN: float = 0.1
CROSSOVER_RATE_MAX: float = 0.6


def process_genetic_algorithm(
    mutation_rate_values: List[float], crossover_rate_values: List[float], use_numpy: bool = False
):
    if use_numpy:
        print("Running numpy version.")
        from one_max_genetic_algorithm_numpy import genetic_algorithm
    else:
        print("Running vanilla version.")
        from one_max_genetic_algorithm_vanilla import genetic_algorithm

        # TODO: Use JAX for GPU

    workers = max(2, cpu_count() - 2) if cpu_count() is not None else 2  # type: ignore
    total_iterations = len(mutation_rate_values) * len(crossover_rate_values)
    progress_bar = tqdm(total=total_iterations, desc="Processing")
    best_mutation_rate = 0.0
    best_crossover_rate = 0.0
    prev_best_score = 0.0

    for mutation_rate in mutation_rate_values:

        prev_local_score = 0.0

        for i, crossover_rate in enumerate(crossover_rate_values):
            results = Results(max_generations=GENERATIONS, max_fitness=1.0)
            progress_bar.set_description(f"Score:{prev_best_score:.3f}")

            with ProcessPoolExecutor(max_workers=workers) as executor:
                future_tasks = [
                    executor.submit(
                        genetic_algorithm,
                        POPULATION_SIZE,
                        GENOME_LENGTH,
                        GENERATIONS,
                        mutation_rate,
                        crossover_rate,
                        SELECT_PARENT_MODE,
                        TARGET_GENERATION_FITNESS,
                    )
                    for _ in range(RUN_TIMES)
                ]
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

            if prev_local_score < (score * 0.9) and i != 0:  # Skip this loop since the score is not improving
                progress_bar.update(len(crossover_rate_values) - i)
                break

            prev_local_score = score
            progress_bar.update(1)

        if prev_best_score >= TARGET_PROBLEM_FITNESS:  # Check if perfect score to close the algorithm execution
            progress_bar.update(total_iterations - progress_bar.n)
            break

    progress_bar.set_description(f"Score: {best_result.score:.3f}")
    progress_bar.close()
    print("-" * 50)
    print("\tBest results")
    print("-" * 50)
    print(f"Best Mutation Rate: {best_mutation_rate}\nBest Crossover Rate: {best_crossover_rate}")
    print(f"{best_result}")


@timeit
def main(use_numpy: bool = False) -> None:
    mutation_rate_values = generate_equally_spaced_values(
        min_val=MUTATION_RATE_MIN, max_val=MUTATION_RATE_MAX, length=8, invert=True
    )
    crossover_rate_values = generate_equally_spaced_values(
        min_val=CROSSOVER_RATE_MIN, max_val=CROSSOVER_RATE_MAX, length=5
    )

    print(
        f"""Running {RUN_TIMES} times the one max problem with genetic algorithms for:
        Generations:{GENERATIONS:>16}
        Population Size:{POPULATION_SIZE:>12}
        Genome Length:{GENOME_LENGTH:>14}
        Parent selection mode: {SELECT_PARENT_MODE}
        Mutation Rate:  {mutation_rate_values[0]:>9} to {mutation_rate_values[-1]} with {len(mutation_rate_values)} steps
        Crossover Rate: {crossover_rate_values[0]:>9} to {crossover_rate_values[-1]} with {len(crossover_rate_values)} steps
        {"-" * 50}"""
    )

    process_genetic_algorithm(mutation_rate_values, crossover_rate_values, use_numpy)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--numpy", action="store_true", help="Specify to include numpy")
    args = parser.parse_args()
    main(use_numpy=args.numpy)
