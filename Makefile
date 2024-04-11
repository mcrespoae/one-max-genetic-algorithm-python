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
ifeq ($(OS),Windows_NT)
	if not exist .venv mkdir .venv
else
	if [ ! -d ".venv" ]; then mkdir -p .venv; fi
endif
	pipenv install

run:
	$(VENV_ACTIVATE) $(PYTHON) ./one_max_genetic_algorithm_python/main.py


test:
	$(VENV_ACTIVATE) $(PYTHON) -m unittest discover -v -s ./tests -p "*test*.py"
