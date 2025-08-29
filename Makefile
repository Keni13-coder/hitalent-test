
.PHONY: build deps prod test stop-dependencies upgrade revision restart down rm

build:
	docker compose build

deps:
	docker compose up -d db redis

prod:
	docker compose up -d app

test:
	docker compose run --rm test-app

stop-dependencies:
	docker compose stop db redis

upgrade:
	docker compose exec -it app alembic upgrade head

revision:
	docker compose exec -it app alembic revision --autogenerate

restart:
	docker compose app restart

down:
	docker compose down

rm:
	docker compose down -v