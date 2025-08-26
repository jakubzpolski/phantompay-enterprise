    run:
		uvicorn app.main:app --reload --port 8000

    db-upgrade:
		alembic upgrade head

    db-rev:
		alembic revision --autogenerate -m "$(m)"
