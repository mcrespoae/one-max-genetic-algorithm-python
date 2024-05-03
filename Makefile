# Makefile
# Check if the OS is Windows
ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE = .venv\Scripts\activate &
	PYTHON = python
	RM = del /Q
	RMDIR = rmdir /S /Q

else
	VENV_ACTIVATE = . .venv/bin/activate &&
	PYTHON = python3
	RM = rm -f
	RMDIR = rm -rf

endif


.PHONY: install build run run-numpy run-dev run-dev-numpy clean test

install:
ifeq ($(OS),Windows_NT)
	if not exist .venv mkdir .venv
else
	if [ ! -d ".venv" ]; then mkdir -p .venv; fi;
endif
	pipenv install

build:
ifeq ($(OS),Windows_NT)
	@for %%i in (src\*.py) do pipenv run mypyc %%i
	@if not exist compiled mkdir compiled
	@move *.pyd compiled
else
	@pipenv run mypyc src/*.py
	@if [ ! -d "compiled" ]; then mkdir -p compiled; fi
	@mv *.so compiled
endif

run:
ifeq ($(OS),Windows_NT)
	$(VENV_ACTIVATE) cd compiled & $(PYTHON) -c "import main; main.main()"
else
	PYTHONPATH=./compiled $(VENV_ACTIVATE) $(PYTHON) -c "import main; main.main()"
endif

run-numpy:
ifeq ($(OS),Windows_NT)
	$(VENV_ACTIVATE) cd compiled & $(PYTHON) -c "import main; main.main(True)"
else
	PYTHONPATH=./compiled $(VENV_ACTIVATE) $(PYTHON) -c "import main; main.main(True)"
endif

run-dev:
	$(VENV_ACTIVATE) $(PYTHON) ./src/main.py

run-dev-numpy:
	$(VENV_ACTIVATE) $(PYTHON) ./src/main.py --numpy

clean:
	$(RMDIR) .mypy_cache
	$(RM) *.so
	$(RM) *.pyd
	$(RMDIR) compiled
	$(RMDIR) build

test:
	$(VENV_ACTIVATE) $(PYTHON) -m unittest discover -v -s ./tests -p "*test*.py"
