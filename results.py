from typing import List


class Results:
    def __init__(self, max_generations: int, max_fitness: float = 1.0) -> None:
        self.max_generations: int = max_generations
        self.max_fitness: float = max_fitness

        self.generations: List[int] = []
        self.generation_fitnesses: List[float] = []
        self.best_fitnesses: List[float] = []
        self.score: float = 0.0
        self.total_generations: int = 0
        self.avg_generation: float = 0.0
        self.avg_generation_fitness: float = 0.0
        self.avg_best_fitness: float = 0.0
        self.best_fitness: float = 0.0
        self.set_overall_values()

    def add_result(self, generation: int, generation_fitness: float, best_fitness: float) -> None:
        self.generations.append(generation)
        self.generation_fitnesses.append(generation_fitness)
        self.best_fitnesses.append(best_fitness)
        self.set_overall_values()

    def set_overall_values(self) -> None:
        self.total_generations = len(self.generations)
        self.avg_generation = sum(self.generations) / self.total_generations if self.total_generations > 0 else self.max_generations
        self.avg_generation_fitness = sum(self.generation_fitnesses) / self.total_generations if self.total_generations > 0 else 0
        self.avg_best_fitness = sum(self.best_fitnesses) / self.total_generations if self.total_generations > 0 else 0
        self.best_fitness = max(self.best_fitnesses) if len(self.best_fitnesses) > 0 else 0
        self.calculate_ponderate_score()

    def calculate_ponderate_score(self) -> None:
        if len(self.generations) == 0:
            self.score = 0

        # Define weights for each metric
        weight_best_fitness: float = 0.4
        weight_avg_generation_fitness: float = 0.3
        weight_avg_best_fitness: float = 0.2
        weight_avg_generation: float = 0.1

        # Adjusting the scores based on criteria
        score_best_fitness: float = self.best_fitness / self.max_fitness
        score_avg_generation: float = 1 - (self.avg_generation - 1) / self.max_generations  # Inverting the avg_generation score and scaling it to 0-1 range
        score_avg_generation_fitness: float = self.avg_generation_fitness  # avg_generation_fitness already in desired range
        score_avg_best_fitness: float = self.avg_best_fitness / self.max_fitness  # Scaling avg_best_fitness to 0-1 range

        # Calculate the ponderate score
        self.score = (
            weight_best_fitness * score_best_fitness +
            weight_avg_generation * score_avg_generation +
            weight_avg_generation_fitness * score_avg_generation_fitness +
            weight_avg_best_fitness * score_avg_best_fitness)

    def get_score(self) -> float:
        return self.score

    def __repr__(self) -> str:
        return f"Overall score: {self.score:.3f} \nBest fitness: {self.best_fitness} \nAverage Generation Fitness: {self.avg_generation_fitness:.3f} \nAverage Best Fitness: {self.avg_best_fitness:.3f} \nAverage Generations Runned: {self.avg_generation:.3f} of {self.max_generations} max generations."