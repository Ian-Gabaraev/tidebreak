.PHONY: up up-d down build logs shell migrate admin seed psql db-backup reset test collectstatic

COMPOSE = docker compose -f docker-compose.yml
WEB     = $(COMPOSE) exec django-api

## Build the tidebreak wheel into dist/ then rebuild Docker images
build:
	rm -rf dist/ build/
	pip wheel . --no-deps -w dist/
	$(COMPOSE) build

## Start all services (foreground)
up:
	$(COMPOSE) up

## Start all services (detached)
up-d:
	$(COMPOSE) up -d

## Stop all services
down:
	$(COMPOSE) down

## Tail all service logs
logs:
	$(COMPOSE) logs -f

## Django shell inside the web container
shell:
	$(WEB) python manage.py shell

## Run Django migrations
migrations:
	$(WEB) python manage.py makemigrations

## Run Django migrations
migrate:
	$(WEB) python manage.py migrate

## Create a Django superuser for Admin access
admin:
	$(WEB) python manage.py createsuperuser

## Seed country source mappings
seed:
	$(WEB) python manage.py seed_sources

## Open a psql shell to the database
psql:
	$(COMPOSE) exec postgres psql -U tidebreak tidebreak

## Dump the database to a local file (creates backups/ dir if needed)
db-backup:
	mkdir -p backups
	$(COMPOSE) exec -T postgres pg_dump -U tidebreak tidebreak > backups/db-$$(date +%Y%m%d).sql

## Reset the database and Redis cache (destructive — local dev only)
reset:
	$(COMPOSE) down -v
	$(COMPOSE) up -d

## Run Django tests
test:
	$(WEB) python manage.py test api

## Collect static files into staticfiles/
collectstatic:
	$(WEB) python manage.py collectstatic --noinput
