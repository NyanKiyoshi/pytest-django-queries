sync:
	uv lock
	uv sync --inexact --all-extras --all-groups

run-server: sync
	./manage.py migrate
	./manage.py runserver
