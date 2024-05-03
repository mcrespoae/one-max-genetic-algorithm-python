import unittest

from src.one_max_genetic_algorithm_vanilla import (
    calculate_population_fitnesses,
    create_new_population,
    crossover,
    genetic_algorithm,
    get_best_fitness,
    get_generation_fitness,
    get_genome_fitness,
    get_target_fitness,
    init_population,
    mutate,
    random_genome,
    select_parent,
    select_parent_roulette,
    select_parent_tournament,
)


class TestUnitGeneticAlgorithm(unittest.TestCase):

    def test_random_genome_length(self):
        length = 10
        actual_genome = random_genome(length)
        self.assertEqual(len(actual_genome), length)

    def test_random_genome_range(self):
        length = 10
        genome = random_genome(length)
        for gen in genome:
            self.assertTrue(gen == 0 or gen == 1)

    def test_random_genome_zero_length(self):
        length = 0
        genome = random_genome(length)
        self.assertEqual(len(genome), 0)

    def test_init_population_length(self):
        population_size = 10
        genome_length = 5
        population = init_population(population_size, genome_length)
        self.assertEqual(len(population), population_size)

    def test_init_population_genome_length(self):
        population_size = 10
        genome_length = 5
        population = init_population(population_size, genome_length)
        for genome in population:
            self.assertEqual(len(genome), genome_length)

    def test_genome_fitness_all_zeros(self):
        genome = [0] * 10
        expected_fitness = 0.0
        actual_fitness = get_genome_fitness(genome)
        self.assertEqual(actual_fitness, expected_fitness)

    def test_genome_fitness_all_ones(self):
        genome = [1] * 10
        expected_fitness = 1.0
        actual_fitness = get_genome_fitness(genome)
        self.assertEqual(actual_fitness, expected_fitness)

    def test_genome_fitness_mixed(self):
        genome = [0, 1, 0, 1, 0, 1, 1, 0]
        expected_fitness = 0.5
        actual_fitness = get_genome_fitness(genome)
        self.assertEqual(actual_fitness, expected_fitness)

    def test_calculate_population_fitnesses_empty_population(self):
        population = []
        expected_fitness = []
        actual_fitness = calculate_population_fitnesses(population)
        print(actual_fitness)
        self.assertEqual(actual_fitness, expected_fitness)

    def test_calculate_population_fitnesses_single_genome(self):
        population = [[0, 1, 0, 1, 0, 1]]
        expected_fitness = [0.5]
        actual_fitness = calculate_population_fitnesses(population)
        self.assertEqual(actual_fitness, expected_fitness)

    def test_calculate_population_fitnesses_multiple_genomes(self):
        population = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        ]
        expected_fitness = [0.0, 0.6, 0.4]
        actual_fitness = calculate_population_fitnesses(population)
        self.assertEqual(actual_fitness, expected_fitness)

    def test_get_target_fitness(self):
        expected_target_fitness = 1
        actual_target_fitness = get_target_fitness()
        self.assertEqual(actual_target_fitness, expected_target_fitness)

    def test_get_best_fitness_empty_vector(self):
        fitness_values = []
        expected_best_fitness = 0
        actual_best_fitness = get_best_fitness(fitness_values)
        self.assertEqual(actual_best_fitness, expected_best_fitness)

    def test_get_best_fitness_single_value(self):
        fitness_values = [0.5]
        expected_best_fitness = 0.5
        actual_best_fitness = get_best_fitness(fitness_values)
        self.assertEqual(actual_best_fitness, expected_best_fitness)

    def test_get_best_fitness_multiple_values(self):
        fitness_values = [0.2, 0.9, 0.4, 0.6, 0.3]
        expected_best_fitness = 0.9
        actual_best_fitness = get_best_fitness(fitness_values)
        self.assertEqual(actual_best_fitness, expected_best_fitness)

    def test_get_generation_fitness_empty_population(self):
        fitness_values = []
        expected_generation_fitness = 0.0
        actual_generation_fitness = get_generation_fitness(fitness_values, 0)
        self.assertEqual(actual_generation_fitness, expected_generation_fitness)

    def test_get_generation_fitness_single_value_population(self):
        fitness_values = [0.8]
        expected_generation_fitness = 0.8
        actual_generation_fitness = get_generation_fitness(fitness_values, 1)
        self.assertEqual(actual_generation_fitness, expected_generation_fitness)

    def test_get_generation_fitness_multiple_values_population(self):
        fitness_values = [0.5, 0.7, 0.9]
        expected_generation_fitness = 0.7
        actual_generation_fitness = get_generation_fitness(fitness_values, 3)
        epsilon = 0.0001
        self.assertLess(abs(actual_generation_fitness - expected_generation_fitness), epsilon)

    def test_select_parent(self):
        # Test scenario with a small population
        population = [
            [1, 1, 1, 1],  # Individual 1
            [1, 0, 1, 0],  # Individual 2
            [0, 0, 1, 1],  # Individual 3
            [0, 0, 0, 0],  # Individual 4
        ]
        fitness_values = calculate_population_fitnesses(population)

        mode = "gibberish"  # Ensure default mode if the mode doesn't exist
        selected_individual = select_parent(population, fitness_values, mode)
        self.assertIn(selected_individual, population)  # Ensure the selected individual is from the population

    def test_select_parent_tournament(self):
        # Test scenario with a small population
        population = [
            [1, 1, 1, 1],  # Individual 1
            [1, 0, 1, 0],  # Individual 2
            [0, 0, 1, 1],  # Individual 3
            [0, 0, 0, 0],  # Individual 4
        ]
        fitness_values = calculate_population_fitnesses(population)
        tournament_size = 2

        selected_individual = select_parent_tournament(population, fitness_values, tournament_size)
        self.assertIn(selected_individual, population)  # Ensure the selected individual is from the population

    def test_select_parent_roulette(self):
        # Test scenario with a small population
        population = [
            [1, 1, 1, 1],  # Individual 1
            [1, 0, 1, 0],  # Individual 2
            [0, 0, 1, 1],  # Individual 3
            [0, 0, 0, 0],  # Individual 4
        ]
        fitness_values = calculate_population_fitnesses(population)

        selected_individual = select_parent_roulette(population, fitness_values)
        self.assertIn(selected_individual, population)  # Ensure the selected individual is from the population

    def test_crossover_no_crossover(self):
        # Given
        parent1 = [1, 2, 3, 4, 5]
        parent2 = [6, 7, 8, 9, 10]
        crossover_rate = 0.0  # No crossover

        child1, child2 = crossover(parent1, parent2, crossover_rate)

        self.assertEqual(child1, parent1)
        self.assertEqual(child2, parent2)

    def test_crossover_with_crossover(self):
        # Given
        parent1 = [1, 2, 3, 4, 5]
        parent2 = [6, 7, 8, 9, 10]
        crossover_rate = 1.0  # Always crossover

        child1, child2 = crossover(parent1, parent2, crossover_rate)

        # Check that the lengths of the children are the same as the parents
        self.assertEqual(len(child1), len(parent1))
        self.assertEqual(len(child2), len(parent2))

        # Check that the new elements are different
        self.assertNotEqual(child1, parent1)
        self.assertNotEqual(child2, parent2)
        self.assertNotEqual(child1, child2)

    def test_mutate_zeros_with_rate_1(self):
        self.assertEqual(mutate([0, 0, 0, 0], 1.0), [1, 1, 1, 1])

    def test_mutate_ones_with_rate_1(self):
        self.assertEqual(mutate([1, 1, 1, 1], 1.0), [0, 0, 0, 0])

    def test_mutate_mixed_with_rate_0(self):
        self.assertEqual(mutate([0, 1, 0, 1], 0.0), [0, 1, 0, 1])

    def test_mutate_mixed_with_rate_0_5(self):
        mutated_genome = mutate([0, 1, 0, 1], 0.5)
        self.assertEqual(len(mutated_genome), 4)

    def test_mutate_population_fitness_all_ones(self):
        num_times = 100_000
        mutation_rate = 0.5
        genome_length = 50
        mutated_gen_fitness = []
        for _ in range(0, num_times):
            genome = [1] * genome_length
            mutated_genome = mutate(genome, mutation_rate)
            mutated_gen_fitness.append(get_genome_fitness(mutated_genome))

        avg_mutation_gen_fitness = sum(mutated_gen_fitness) / len(mutated_gen_fitness)
        self.assertTrue(0.49 <= avg_mutation_gen_fitness <= 0.51)

    def test_mutate_population_fitness_all_zeroes(self):
        num_times = 100_000
        mutation_rate = 0.5
        genome_length = 50

        mutated_gen_fitness = []
        for _ in range(0, num_times):
            genome = [0] * genome_length
            mutated_genome = mutate(genome, mutation_rate)
            mutated_gen_fitness.append(get_genome_fitness(mutated_genome))

        avg_mutation_gen_fitness = sum(mutated_gen_fitness) / len(mutated_gen_fitness)
        self.assertTrue(0.49 <= avg_mutation_gen_fitness <= 0.51)

    def test_population_size_odd(self):
        population_size = 101
        population = [[0, 1, 0, 1]] * population_size
        fitness_values = [0.5] * population_size
        select_parent_mode = "tournament"
        crossover_rate = 0.8
        mutation_rate = 0.03
        population_fitness = calculate_population_fitnesses(population)
        population_fitness_avg = get_generation_fitness(population_fitness, population_size)

        new_population = create_new_population(
            population_size, population, fitness_values, select_parent_mode, crossover_rate, mutation_rate
        )
        new_population_fitness = calculate_population_fitnesses(new_population)
        new_population_fitness_avg = get_generation_fitness(new_population_fitness, population_size)

        self.assertEqual(len(new_population), population_size)
        self.assertLessEqual(population_fitness_avg * 0.8, new_population_fitness_avg)

    def test_genetic_algorithm_default_parameters(self):
        # Test with default parameters
        generation, generation_fitness, best_fitness = genetic_algorithm()
        self.assertIsInstance(generation, int)
        self.assertIsInstance(generation_fitness, float)
        self.assertIsInstance(best_fitness, float)

        # Check if generation is less than or equal to max_generations
        self.assertLessEqual(generation, 1000)

        # Check if generation_fitness and best_fitness are within the range [0, 1]
        self.assertGreaterEqual(generation_fitness, 0)
        self.assertLessEqual(generation_fitness, 1)
        self.assertGreaterEqual(best_fitness, 0)
        self.assertLessEqual(best_fitness, 1)

    def test_genetic_algorithm_custom_parameters(self):
        # Test with custom parameters
        population_size = 20
        genome_length = 10
        max_generations = 50
        mutation_rate = 0.01
        crossover_rate = 0.8
        select_parent_mode = "roulette"
        target_generation_fitness = 0.95
        verbose = True

        generation, generation_fitness, best_fitness = genetic_algorithm(
            population_size=population_size,
            genome_length=genome_length,
            max_generations=max_generations,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            select_parent_mode=select_parent_mode,
            target_generation_fitness=target_generation_fitness,
            verbose=verbose,
        )

        self.assertIsInstance(generation, int)
        self.assertIsInstance(generation_fitness, float)
        self.assertIsInstance(best_fitness, float)

        # Check if generation is less than or equal to max_generations
        self.assertLessEqual(generation, max_generations)

        # Check if generation_fitness and best_fitness are within the range [0, 1]
        self.assertGreaterEqual(generation_fitness, 0)
        self.assertLessEqual(generation_fitness, 1)
        self.assertGreaterEqual(best_fitness, 0)
        self.assertLessEqual(best_fitness, 1)


class TestInteGeneticAlgorithm(unittest.TestCase):

    def test_inte_new_population_random(self):
        # Test with custom parameters
        population_size = 50
        genome_length = 20
        num_times = 200

        random_fitness = []
        for _ in range(0, num_times):
            population = init_population(population_size, genome_length)
            fitness_values = calculate_population_fitnesses(population)
            generation_fitness = get_generation_fitness(fitness_values, population_size)
            random_fitness.append(generation_fitness)

        fitness_avg = sum(random_fitness) / len(random_fitness)
        self.assertTrue(0.49 <= fitness_avg <= 0.51)

    def test_inte_new_population_zeroes(self):
        # Test with custom parameters
        population_size = 1_000
        genome_length = 50
        crossover_rate = 0.2
        mutation_rate = 0.03

        genome = [0] * genome_length
        population = [genome[:] for _ in range(population_size)]
        fitness_values = calculate_population_fitnesses(population)
        new_population = []

        for _ in range(population_size // 2):
            parent1 = select_parent(population, fitness_values, mode="roulette")
            parent2 = select_parent(population, fitness_values, mode="roulette")
            offspring1, offspring2 = crossover(parent1, parent2, crossover_rate)
            new_population.extend([mutate(offspring1, mutation_rate), mutate(offspring2, mutation_rate)])
        if population_size % 2 != 0:
            parent = select_parent(population, fitness_values, mode="roulette")
            new_population.append(mutate(parent, mutation_rate))

        fitness_values = calculate_population_fitnesses(new_population)
        generation_fitness = get_generation_fitness(fitness_values, population_size)

        self.assertTrue(0.02 <= generation_fitness <= 0.04)

    def test_inte_get_avg(self):
        # Test with custom parameters
        population_size = 1_000
        genome_length = 20
        crossover_rate = 0.6
        mutation_rate = 0.07
        num_times = 10

        genome = [0] * genome_length
        population = [genome[:] for _ in range(population_size)]
        fitness_values = calculate_population_fitnesses(population)

        generation_fitness = []
        best_genome_fitness = []
        for _ in range(0, num_times):
            new_population = create_new_population(
                population_size, population, fitness_values, "roulette", crossover_rate, mutation_rate
            )
            fitness_values = calculate_population_fitnesses(new_population)
            generation_fitness.append(get_generation_fitness(fitness_values, population_size))
            best_genome_fitness.append(get_best_fitness(fitness_values))

        avg_best_fitness = sum(generation_fitness) / len(generation_fitness)
        avg_best_genome_fitness = sum(best_genome_fitness) / len(best_genome_fitness)

        self.assertTrue(0.06 <= avg_best_fitness <= 0.073)
        self.assertTrue(0.25 <= avg_best_genome_fitness <= 0.45)


if __name__ == "__main__":
    unittest.main()
