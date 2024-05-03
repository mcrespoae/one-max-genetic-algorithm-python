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
	pipenv run mypyc src/*.py

ifeq ($(OS),Windows_NT)
	@if not exist compiled mkdir compiled
	@move src\*.pyd compiled
else
	@if [ ! -d "compiled" ]; then mkdir -p compiled; fi
	@mv *.so compiled
endif

run: build
	@PYTHONPATH=./compiled $(VENV_ACTIVATE) $(PYTHON) -c "import main; main.main()"

run-numpy: build
	@PYTHONPATH=./compiled $(VENV_ACTIVATE) $(PYTHON) -c "import main; main.main(True)"

run-dev:
	$(VENV_ACTIVATE) $(PYTHON) ./src/main.py

run-dev-numpy:
	$(VENV_ACTIVATE) $(PYTHON) ./src/main.py --numpy

clean:
	$(RMDIR) .mypy_cache
	$(RM) *.so
	$(RMDIR) compiled

test:
	$(VENV_ACTIVATE) $(PYTHON) -m unittest discover -v -s ./tests -p "*test*.py"
