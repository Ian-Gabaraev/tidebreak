.PHONY: up down build wheel logs shell

## Build cbfx wheel into dist/
wheel:
	rm -rf dist/ build/
	pip wheel . --no-deps -w dist/

## Start all services
up:
	docker compose up

## Start in detached mode
up-d:
	docker compose up -d

## Stop all services
down:
	docker compose down

## Rebuild images (rebuilds cbfx wheel first, then Docker images)
build: wheel
	docker compose build

## Tail all service logs
logs:
	docker compose logs -f

## Reset the database and Redis cache (destructive — local dev only)
reset:
	docker compose down -v
	docker compose up -d