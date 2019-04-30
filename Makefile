default: test

test: env
	.env/bin/pytest tests
	.env/bin/pylint --rcfile .pylintrc flask_loopback tests setup.py

env: .env/.up-to-date

.env/.up-to-date: setup.py Makefile
	python -m virtualenv .env
	.env/bin/pip install -e ".[testing]"
	touch $@
