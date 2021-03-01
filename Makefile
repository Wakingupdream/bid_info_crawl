.PHONY: clean flake8 pylint lint dist upload

PIPRUN := $(shell command -v pipenv > /dev/null && echo pipenv run)
TARGET := uc_crawler

clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
	find . -name '__pycache__' -print0 | xargs -0 rm -rf
	find . -name '.pytest_cache' -print0 | xargs -0 rm -rf

flake8:
	${PIPRUN} flake8 \
		--statistics \
		--inline-quotes 'double' \
		${TARGET}

pylint:
	${PIPRUN} pylint ${TARGET}

lint: flake8 pylint

dist:
	${PIPRUN} python setup.py sdist bdist_wheel

upload:
	${PIPRUN} twine upload dist/*
