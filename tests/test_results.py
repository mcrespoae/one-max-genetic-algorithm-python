import unittest

from src.results import Results


class TestResults(unittest.TestCase):
    def setUp(self):
        # Initialize a Results object with max_generations of 100 and max_fitness of 1.0
        self.results = Results(max_generations=100, max_fitness=1.0)

    def test_add_result(self):
        # Add a result to the Results object
        self.results.add_result(generation=60, generation_fitness=0.8, best_fitness=0.9)

        # Check if the result is added correctly
        self.assertEqual(len(self.results.generations), 1)
        self.assertEqual(len(self.results.generation_fitnesses), 1)
        self.assertEqual(len(self.results.best_fitnesses), 1)

    def test_set_overall_values(self):
        self.results.add_result(generation=1, generation_fitness=0.8, best_fitness=0.9)
        self.results.add_result(generation=2, generation_fitness=0.85, best_fitness=0.92)

        # Check if overall values are set correctly
        self.assertEqual(self.results.total_generations, 2)
        self.assertAlmostEqual(self.results.avg_generation, 1.5)
        self.assertAlmostEqual(self.results.avg_generation_fitness, 0.825)
        self.assertAlmostEqual(self.results.avg_best_fitness, 0.91)
        self.assertAlmostEqual(self.results.best_fitness, 0.92)

    def test_calculate_ponderate_score(self):
        self.results.add_result(generation=1, generation_fitness=0.8, best_fitness=0.9)
        self.results.add_result(generation=2, generation_fitness=0.85, best_fitness=0.92)

        # Check if the score is calculated correctly
        expected_score = 0.4 * (0.92 / 1.0) + 0.1 * (1 - (1.5 - 1) / 100) + 0.3 * 0.825 + 0.2 * (0.91 / 1.0)
        self.assertAlmostEqual(self.results.get_score(), expected_score)


if __name__ == "__main__":
    unittest.main()
