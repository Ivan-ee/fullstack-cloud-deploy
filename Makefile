SHELL := /bin/bash
include .env

requirements:
	pip freeze > requirements.txt

run-dev:
	docker-compose -f docker-compose.dev.yml up -d
	flask run --debug --port=${APP_PORT}

stop-dev:
	docker compose stop

run-local:
	docker-compose -f docker-compose.local.yml --env-file .env.local up --build web

stop-local:
	docker-compose stop

test:
	python -m unittest
