SHELL := /bin/bash
include .env

requirements:
	pip freeze > requirements.txt

run-local:
	docker-compose -f docker-compose.dev.yml up -d
	flask run --debug --port=${APP_PORT}

test:
	python -m unittest

first-migration:
	docker exec -it $(CONTAINER_ID) flask db init
	docker exec -it $(CONTAINER_ID) flask db migrate -m "Initial migration"
	docker exec -it $(CONTAINER_ID) flask db upgrade
