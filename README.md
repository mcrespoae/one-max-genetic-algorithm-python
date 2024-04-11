
# Genetic Algorithm: Solving the One Max Problem in Python

This project implements a genetic algorithm to solve the One Max Problem, which involves finding a binary string of maximum length where all bits are set to 1.

## Installation

You can install this project using [Pipenv](https://pipenv.pypa.io/). First, clone the repository and navigate to the project directory. If you want the dependencies to be installed in the same directory, create an empty directory called `.venv`. Then, run the following command:
```bash
pipenv install
```

This will create a virtual environment and install all dependencies specified in the Pipfile.

## Project tree

- `__init__.py`
- `one_max_genetic_algorithm_python`
    - `__init__.py`
    - `main.py`: Contains the main entry point for running the algorithm.
    - `one_max_genetic_algorithm.py`: Implementation of the genetic algorithm.
    - `timeit_functions.py`: Contains a decorator function for measuring the execution time.
    - `results.py`: Contains a class for storing and computing the results of the genetic algorithm.
    - `utils.py`: Contains helper functions.
- `tests`
    - `__init__.py`
    - `test_one_max_genetic_algorithm.py`: Unittests for the genetic algorithm.


## Dependencies

- `tqdm`: Used for displaying progress bars during execution.
- `concurrent.futures`: Used for parallel execution of genetic algorithm runs.
- `typing`: Provides type hints for the codebase.

## Usage

To run the genetic algorithm, execute `main.py`. You can adjust various parameters in `main.py` to customize the genetic algorithm's behavior. These parameters include:

- `RUN_TIMES`: Number of times to run the genetic algorithm.
- `GENERATIONS`: Number of generations in the genetic algorithm.
- `POPULATION_SIZE`: Size of the population in each generation.
- `GENOME_LENGTH`: Length of the binary string.
- `TARGET_GENERATION_FITNESS`: Target fitness for a generation to be considered successful and skip the next iterations. From 0 to 1. Values close to 1.0 will yield better results.
- `TARGET_PROBLEM_FITNESS`: Target fitness for the whole problem to be marked as solved. From 0 to 1. Values very close to 1.0 will not stop the execution.
- `MUTATION_RATE_MIN`: Minimum mutation rate.
- `MUTATION_RATE_MAX`: Maximum mutation rate.
- `CROSSOVER_RATE_MIN`: Minimum crossover rate.
- `CROSSOVER_RATE_MAX`: Maximum crossover rate.
```bash
python main.py
```
## Algorithm Overview

The genetic algorithm proceeds as follows:

1. **Initialization**: Initialize a population of binary strings randomly.
2. **Evaluation**: Evaluate the fitness of each individual in the population.
3. **Selection**: Select individuals for reproduction based on their fitness using either roulette or tournament selection.
4. **Crossover**: Produce offspring by combining genetic material from selected individuals.
5. **Mutation**: Introduce random changes to the offspring's genetic material.
6. **Replacement**: Replace the old generation with the new generation.
7. **Termination**: Repeat steps 2-6 until a termination condition is met, such as reaching a maximum number of generations or achieving a target fitness level.

## Results

The project includes functionality to process the genetic algorithm with different mutation rates and crossover rates to determine the optimal combination for solving the One Max Problem efficiently. The results are displayed, showing the best mutation rate and crossover rate found during the processing.

## Optimization

The genetic algorithm employs concurrent processing techniques for parallel execution, enhancing runtime performance.

## Contributors

- [Mario Crespo](https://github.com/mcrespoae)

