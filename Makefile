PYTHON = python3
TEST = app/tests/test_*

test:
	$(PYTHON) -m unittest $(TEST)
	$(PYTHON) -m unittest app/tests/services/test*

install:
	pip install -r requirements.txt

lint:
	flake8 app --ignore=E501,E703,F401,E402

run:
	$(PYTHON) run.py