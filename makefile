VENV ?= .venv
LINE_LENGTH ?= 120
LINT_DIRS = movies config

install:
	python3.11 -m venv .venv
	$(VENV)/bin/pip config --site set global.index-url https://pypi.org/simple/
	$(VENV)/bin/pip config --site set global.extra-index-url https://pypi.org/simple/
	$(VENV)/bin/pip install -r requirements


plint:
	$(VENV)/bin/ruff format $(LINT_DIRS)
	$(VENV)/bin/ruff check $(LINT_DIRS) --fix --show-fixes
	$(VENV)/bin/mypy --install-types --non-interactive --namespace-packages \
	    --explicit-package-bases $(LINT_DIRS) --disable-error-code import-untyped --exclude movies/migrations


migrate:
	psql -h 127.0.0.1 -U app -d movies_database -c 'CREATE SCHEMA IF NOT EXISTS content;'
	$(VENV)/bin/python manage.py migrate

gen-migrate:
	$(VENV)/bin/python movies_admin/manage.py makemigrations movies --settings=config.settings

run:
	$(VENV)/bin/python manage.py runserver

docker-run:
	docker-compose up -d --build
