sync:
	uv lock
	uv sync --inexact --all-extras --all-groups

update-precommit:
	uv run pre-commit autoupdate --freeze
