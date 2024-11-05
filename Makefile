SHELL := /bin/bash
include .env

requirements:
	pip freeze > requirements.txt

run-local:
	docker-compose -f docker-compose.dev.yml up -d
	flask run --host=0.0.0.0 --port=${APP_PORT}
