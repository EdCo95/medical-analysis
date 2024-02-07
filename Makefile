.PHONY: install-deploy install-dev lint format test clean analyse docker-build

VENV_DIR := .venv

install-deploy: venv
	ls -a .venv/bin
	$(VENV_DIR)/bin/pip install .

install-dev: venv
	$(VENV_DIR)/bin/pip install -e .
	$(VENV_DIR)/bin/pre-commit install
	$(VENV_DIR)/bin/pre-commit autoupdate

lint: venv
	$(VENV_DIR)/bin/flake8 src

format: venv
	$(VENV_DIR)/bin/black src
	$(VENV_DIR)/bin/isort src

test: venv
	$(VENV_DIR)/bin/pytest tests

clean:
	rm -rf $(VENV_DIR)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

docker-build:
	docker build -t medical-assessment .

analyse:
	docker run -e OPENAI_API_KEY=$$OPENAI_API_KEY -v $(PWD):/app medical-assessment --record-path /app/$(RECORD_PATH) --write-loc /app/$(WRITE_LOC)

venv: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: pyproject.toml
	python -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -U pip
	$(VENV_DIR)/bin/pip install -U setuptools wheel
	$(VENV_DIR)/bin/pip install -e .
