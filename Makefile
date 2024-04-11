# Makefile
# Check if the OS is Windows
ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE = .venv\Scripts\activate &
	PYTHON = python

else
	VENV_ACTIVATE = . .venv/bin/activate &&
	PYTHON = python3

endif


install:
	mkdir -p .venv
	pipenv install
	pipenv shell

run:
	$(VENV_ACTIVATE) $(PYTHON) ./one_max_genetic_algorithm_python/main.py


run_tests:
	$(VENV_ACTIVATE) $(PYTHON) -m unittest discover -v -s ./tests -p "*test*.py"
