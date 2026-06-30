install:
	uv sync

dev:
	uv run manage.py runserver

lint:
	uv run ruff check task_manager
	uv run ruff check apps

migrate:
	uv run manage.py makemigrations

collectstatic:
	uv run manage.py collectstatic

apply migrations:
	uv run manage.py migrate 

compilemessages:
	uv run manage.py compilemessages

messages:
	uv run manage.py  makemessages -l ru

test:
	uv run pytest .

	