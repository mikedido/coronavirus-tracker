PYTHON = python3
TEST = app/tests/test_*

test:
	$(PYTHON) -m unittest $(TEST)

install:
	pip install -r requirements.txt

lint:
	flake8 app

run:
	$(PYTHON) run.py