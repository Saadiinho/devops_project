# ==================================================================================== #
# VARIABLES
# ==================================================================================== #
TEST_DIR := tests/
DEVOPS_PROJECT := devops_project/


# ==================================================================================== #
# HELPERS
# ==================================================================================== #
## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ":" | sed -e 's/^/ /'


# ==================================================================================== #
# BUILD
# ==================================================================================== #

## test: run pytest on the tests directory
test:
	pytest $(TEST_DIR)

## test: run coverage on the tests directory
cov:
	coverage run -m pytest --cov=. --cov-report xml $(TEST_DIR)/*

## black: run black on the current directory
black:
	black .

## black_check: Verify code formatting with black.
black_check:
	black --check .

## black_test: run black on the tests directory
black_test:
	black $(TEST_DIR)

## black_festo: run black on the project directory
black_devops:
	black $(DEVOPS_PROJECT)

## bandit: run bandit on the project directory
bandit:
	bandit -r $(DEVOPS_PROJECT)/*.py

## all: run all tests, linting, and formatting
all: test cov black black_check black_test black_devops bandit
