default: test

test: env
	.env/bin/py.test tests

env: .env/.up-to-date

.env/.up-to-date: setup.py Makefile
	python -m virtualenv .env
	.env/bin/pip install -e .
	.env/bin/pip install pytest
	touch $@

