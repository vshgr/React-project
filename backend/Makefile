include .env
export


# Linter
## Format all
fmt: format
format: isort black


## Check code quality
chk: check
lint: check
check: flake black_check isort_check


## Sort imports
isort:
	isort app

isort_check:
	isort --check-only app


## Format code
black:
	black --config pyproject.toml app

black_check:
	black --config pyproject.toml --diff --check app


## Check pep8
flake:
	flake8 --config .flake8 app
