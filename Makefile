sync:
	uv lock
	uv sync --inexact --all-extras

update-precommit:
	uv run pre-commit autoupdate --freeze
