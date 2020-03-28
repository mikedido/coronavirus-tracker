PYTHON = python3
TEST = app/tests/test_*

test:
	$(PYTHON) -m unittest $(TEST)

install:
	pip install -r requirements.txt

run:
	$(PYTHON) run.py