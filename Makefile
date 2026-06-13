install:
	uv sync

dev:
	uv run task_manager/manage.py runserver

lint:
	uv run ruff check task_manager

migrate:
	uv run task_manager/manage.py makemigrations



	