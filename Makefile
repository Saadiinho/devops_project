# Define directories for the project and tests
TEST_DIR = 'tests/'               # Directory containing test files
PROJECT_DIR = 'devops_project/.'   # Directory containing the main project code

# Format the code in the project directory using Black
black:
	black $(PROJECT_DIR)

# Format the code in the test directory using Black
black_test:
	black $(TEST_DIR)

# Check if the code in the project directory conforms to Black formatting (without modifying files)
black_check:
	black --check $(PROJECT_DIR)

# Lint the code in the project directory using Pylint
lint:
	pylint $(PROJECT_DIR)

# Lint the code in the test directory using Pylint
lint_test:
	pylint $(TEST_DIR)

# Perform security analysis on the project directory using Bandit
bandit:
	bandit $(PROJECT_DIR)

# Run unit tests using pytest
test:
	pytest $(TEST_DIR)

# Build a Dockerfile
docker-build:
	docker build -- devops_proj .

# Run a docker image
docker-compose:
	docker compose up --detach