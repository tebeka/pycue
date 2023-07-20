default:
	$(error please pick a target)

test:
	python -m flake8 .
	python -m mypy cue.py
	python -m pytest -v tests

upload:
	rm -rf dist
	python setup.py sdist
	python -m twine upload dist/pycue-*.tar.gz
