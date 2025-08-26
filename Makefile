up:
	docker compose up --build

down:
	docker compose down

migrate:
	docker compose run backend alembic upgrade head

revision:
	docker compose run backend alembic revision --autogenerate -m "$(msg)"

logs:
	docker compose logs -f backend

format:
	docker compose run backend black .


test:
	docker compose run backend pytest backend/tests
