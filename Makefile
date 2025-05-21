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
# TEST
# ==================================================================================== #

## test: run pytest on the tests directory
.PHONY: test
test:
	pytest $(TEST_DIR)

## test: run coverage on the tests directory
cov:
	coverage run -m pytest --cov=. --cov-report xml $(TEST_DIR)/*

# ==================================================================================== #
# FORMAT
# ==================================================================================== #

## black: run black on the current directory
.PHONY: black
black:
	black .

## black_check: Verify code formatting with black.
.PHONY: black_check
black_check:
	black --check .

## black_test: run black on the tests directory
.PHONY: black_test
black_test:
	black $(TEST_DIR)

## black_festo: run black on the project directory
.PHONY: black_devops
black_devops:
	black $(DEVOPS_PROJECT)

## bandit: run bandit on the project directory
.PHONY: bandit
bandit:
	bandit -r $(DEVOPS_PROJECT)/*.py

# ==================================================================================== #
# BUILD
# ==================================================================================== #

## docker-build: Build image of the project
.PHONY: docker-build
docker-build:
	docker build -t devops_project .

# ==================================================================================== #
# STOP
# ==================================================================================== #

## docker-build: Build image of the project
.PHONY: stop
stop:
	docker compose down

# ==================================================================================== #
# RUN
# ==================================================================================== #

## docker-build: Build image of the project
.PHONY: run
run:stop docker-build 
	docker compose up -d
