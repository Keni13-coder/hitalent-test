
.PHONY: build dependencies prod test stop-dependencies

build:
	docker compose build

dependencies:
	docker compose up -d db redis

prod:
	docker compose up -d app

test: dependencies
	docker compose run --rm test-app

stop-dependencies:
	docker compose stop db redis