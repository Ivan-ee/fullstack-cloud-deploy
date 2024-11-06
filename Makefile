SHELL := /bin/bash
include .env

requirements:
	pip freeze > requirements.txt

run-local:
	docker-compose -f docker-compose.dev.yml up -d
	flask run --debug --port=${APP_PORT}

test:
	python -m unittest
