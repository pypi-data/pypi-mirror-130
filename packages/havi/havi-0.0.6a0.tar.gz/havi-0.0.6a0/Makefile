.PHONY: lint # if I want to setup linting for the code

NAME=heimdall

install:
	pip install -r requirements.txt && pip install -e .

lint: # for linting python files
	pip install isort && isort . --atomic && pip install black && black **/*.py

release:
	python setup.py sdist && pip install twine && twine upload dist/*