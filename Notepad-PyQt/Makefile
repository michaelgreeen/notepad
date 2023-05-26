.PHONY: venv run clean

# Variables
PYTHON = py
PIP = pip
MAIN_FILE = Notepad.py

# Create a virtual environment and install dependencies
venv:
	python -m venv env
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run the Python project
run:
	$(PYTHON) $(MAIN_FILE)

# Remove the virtual environment
clean:
	@IF EXIST env ( \
		RMDIR /Q /S env \
	)
