all: run
	@echo 'Listening on http://localhost:8000'

down:
	docker compose down

run: build
	docker compose up -d && docker compose logs -f

build:
	docker compose build --parallel

logs:
	docker compose logs -f

watch:
	docker compose watch

deploy:
	git push sendit-projects-api 
	git push sendit-core