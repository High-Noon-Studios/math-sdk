PYTHON := python3
VENV_DIR := env
VENV_PY := $(VENV_DIR)/bin/python

ifeq ($(OS),Windows_NT)
	VENV_PY := $(VENV_DIR)\Scripts\python.exe
	ACTIVATE := $(VENV_DIR)\Scripts\activate.bat
else
	ACTIVATE := source $(VENV_DIR)/bin/activate
endif

makeVirtual:
	$(PYTHON) -m venv $(VENV_DIR)

pipInstall: makeVirtual
	$(VENV_PY) -m pip install --upgrade pip

pipPackages: pipInstall
	$(VENV_PY) -m pip install -r requirements.txt

packInstall: pipPackages
	$(VENV_PY) -m pip install -e .

setup: packInstall
	@echo "Virtual environment ready."
	@echo "To activate it, run:"
	@echo "$(ACTIVATE)"

run GAME:
	$(VENV_PY) games/$(GAME)/run.py

runDev GAME:
	$(VENV_PY) games/$(GAME)/run_dev.py

visualize GAME:
	$(VENV_PY) games/$(GAME)/visualize_stats.py --json games/$(GAME)/library/stats_summary.json --excel games/$(GAME)/library/$(GAME)_full_statistics.xlsx --out games/$(GAME)/stats_figs --show 1

test:
	cd $(CURDIR)
	pytest tests/

clean:
	rm -rf env __pycache__ *.pyc