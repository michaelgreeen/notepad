.PHONY: venv run clean

# Variables
PYTHON = python3
PIP = pip
MAIN_FILE = Notepad.py
RM = rm -rf

# Determine the operating system
UNAME_S := $(shell uname -s)

# Create a virtual environment and install dependencies
venv:
ifeq ($(UNAME_S),Darwin)
	python3 -m venv env
	. env/bin/activate && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt
else ifeq ($(UNAME_S),Linux)
	python3 -m venv env
	. env/bin/activate && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt
else ifeq ($(UNAME_S),Windows_NT)
	python -m venv env
	.\env\Scripts\activate && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt
endif

# Run the Python project
run:
	$(PYTHON) $(MAIN_FILE)

# Remove the virtual environment
clean:
ifeq ($(UNAME_S),Darwin)
	@if [ -d env ]; then \
		$(RM) env; \
	fi
else ifeq ($(UNAME_S),Linux)
	@if [ -d env ]; then \
		$(RM) env; \
	fi
else ifeq ($(UNAME_S),Windows_NT)
	@IF EXIST env ( \
		RMDIR /Q /S env \
	)
endif