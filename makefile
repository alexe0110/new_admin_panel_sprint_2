VENV ?= .venv
LINE_LENGTH ?= 120
LINT_DIRS = movies_admin sqlite_to_postgres
EXCLUDE_DIRS = movies_admin/movies/migrations

install:
	python3.11 -m venv .venv
	$(VENV)/bin/pip config --site set global.index-url https://pypi.org/simple/
	$(VENV)/bin/pip config --site set global.extra-index-url https://pypi.org/simple/
	$(VENV)/bin/pip install -r requirements

migrate:
	psql -h 127.0.0.1 -U app -d movies_database -c 'CREATE SCHEMA IF NOT EXISTS content;'
	$(VENV)/bin/python manage.py migrate

gen-migrate:
	$(VENV)/bin/python movies_admin/manage.py makemigrations movies --settings=config.settings

run:
	$(VENV)/bin/python manage.py runserver

docker-run:
	docker-compose up -d --build
