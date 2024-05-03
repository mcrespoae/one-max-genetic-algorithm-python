
# Genetic Algorithm: Solving the One Max Problem in Python

This project implements a genetic algorithm to solve the One Max Problem, which involves finding a binary string of maximum length where all bits are set to 1. It showcases the use of Python, multithreading, NumPy, mypyc, and Make. The codebase has been tested on macOS and Windows 11 platforms.

## Requirements

- [Pipenv](https://pipenv.pypa.io/).
- [Python 3.12](https://www.python.org/downloads/release/python-3123/).
- [Make](https://www.gnu.org/software/make/). For Windows users, consider installing Make via [Chocolatey](https://chocolatey.org/install) using  ` choco install make `

## Installation

To set up this project, begin by cloning the repository and navigating to the project directory. Install the dependencies by running:

```bash
make install
```

This command will establish a virtual environment and install all dependencies specified in the Pipfile.

## Project tree

- `Makefile`: Contains useful project-related commands.
- `src`
  - `main.py`: Contains the main entry point for running the algorithm.
  - `one_max_genetic_algorithm_numpy.py`: Implementation of the genetic algorithm using the NumPy library.
  - `one_max_genetic_algorithm_vannilla.py`: Implementation of the genetic algorithm using vanilla Python.
  - `timeit_functions.py`: Contains a decorator function for measuring the execution time.
  - `results.py`: Contains a class for storing and computing the results of the genetic algorithm.
  - `utils.py`: Contains helper functions.
- `tests`
  - `__init__.py`
  - `test_one_max_genetic_algorithm_vanilla.py`: Unit and integration tests for the genetic algorithm for the vanilla Python implementation.
  - `test_one_max_genetic_algorithm_numpy.py`: Unit and integration tests for the genetic algorithm for the NumPy implementation.
  - `test_results.py`: Unittests for the Results class.
  - `test_utils.py`: Unittests for the utils file.

## External Dependencies

- `tqdm`: Used for displaying progress bars during execution.
- `types-tqdm`: Provides support for tqdm types.
- `typing`: Provides type hints for the codebase.
- `numpy`: Provides support for numerical computing in Python.
- `setuptools`: Provides support for some errors when installing the virtual environment.
- `mypy`: Provides support for using mypyc (compiled Python to C extensions).

## Usage

### Running Interpreted Versions

To run the vanilla genetic algorithm, execute `main.py` by using:

```bash
make run-dev
```

Alternatively, you can execute the NumPy version of the algorithm with:

```bash
make run-dev-numpy
```

The NumPy version may have a slightly slower performance compared to the vanilla implementation. This NumPy implementation serves only to showcase my working knowledge in NumPy.

### Building and Running Compiled Versions

You can compile the code using mypyc with the command:

```bash
make build
```

Then, you can run the vanilla mypyc version with:

```bash
make run
```

Or run the compiled NumPy version with:

```bash
make run-numpy
```

Running the algorithm using the mypyc compiled version is slightly faster (≈7.15%) and it has been developed to showcase my working knowledge with mypyc.

### Cleaning

To clean the mypyc compiled code and subproducts, use:

```bash
make clean
```

### Algorithm customization

You can adjust various parameters in `main.py` to customize the genetic algorithm's behavior. These parameters are:

- `RUN_TIMES`: Number of times to run the genetic algorithm.
- `GENERATIONS`: Number of generations in the genetic algorithm.
- `POPULATION_SIZE`: Size of the population in each generation.
- `GENOME_LENGTH`: Length of the binary string.
- `SELECT_PARENT_MODE`: Type of parent selection. tournament or roulette. Tournament usually converges faster and yields better results.
- `TARGET_GENERATION_FITNESS`: Target fitness for a generation to be considered successful and skip the next iterations. From 0 to 1. Values close to 1.0 will yield better results.
- `TARGET_PROBLEM_FITNESS`: Target fitness for the whole problem to be marked as solved. From 0 to 1. Values very close to 1.0 will not stop the execution.
- `MUTATION_RATE_MIN`: Minimum mutation rate.
- `MUTATION_RATE_MAX`: Maximum mutation rate.
- `CROSSOVER_RATE_MIN`: Minimum crossover rate.
- `CROSSOVER_RATE_MAX`: Maximum crossover rate.

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

The genetic algorithm employs concurrent processing techniques for parallel execution, enhancing runtime performance. Additionally, it can be run using a compiled version by mypyc. Numba (njit and jit decorators) and cache optimizations were not used due to incompatibilities with the code.

## Testing

The code is equipped with comprehensive unit and integration tests to ensure reliability. They can be executed by using the Make command:

```bash
make test
```

## Rust implementation

I've also developed this repository in [Rust](https://github.com/mcrespoae/one-max-genetic-algorithm-rust), achieving an average execution time that could be up to 10 times faster compared to vanilla non-compiled Python.

## Contributors

- [Mario Crespo](https://github.com/mcrespoae)
