install:
	uv sync

dev:
	uv run task_manager/manage.py runserver

lint:
	uv run ruff check task_manager

migrate:
	uv run task_manager/manage.py makemigrations

collectstatic:
	uv run task_manager/manage.py collectstatic

migrate app:
	uv run task_manager/manage.py makemigrations task_manager

apply migrations:
	uv run task_manager/manage.py migrate task_manager

compilemessages:
	uv run task_manager/manage.py compilemessages

messages:
	uv run task_manager/manage.py  makemessages -l ru

test:
	uv run pytest task_manager/

	