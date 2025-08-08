.PHONY: help install test lint format clean

# Variables
PYTHON = python
PIP = pip
PYTEST = python -m pytest
FLAKE8 = flake8
BLACK = black
ISORT = isort
MYPY = mypy

# Default target when 'make' is run without arguments
help:
	@echo "\nSecure Image Encryption System - Development Commands"
	@echo "=============================================="
	@echo "\nAvailable commands:\n"
	@echo "  install           - Install all dependencies (backend + frontend)"
	@echo "  install-backend   - Install Python backend dependencies"
	@echo "  install-frontend  - Install Node.js frontend dependencies"
	@echo "  test             - Run all tests"
	@echo "  test-backend     - Run backend tests"
	@echo "  test-frontend    - Run frontend tests"
	@echo "  lint             - Run all linters"
	@echo "  lint-backend     - Lint Python code"
	@echo "  lint-frontend    - Lint JavaScript/TypeScript code"
	@echo "  format           - Format all code"
	@echo "  format-backend   - Format Python code"
	@echo "  format-frontend  - Format frontend code"
	@echo "  clean            - Remove all build artifacts and caches"
	@echo "  clean-backend    - Clean Python build artifacts"
	@echo "  clean-frontend   - Clean frontend build artifacts"
	@echo "  run-backend      - Start the backend server"
	@echo "  run-frontend     - Start the frontend development server"
	@echo "  docker-build     - Build Docker images"
	@echo "  docker-up        - Start all services with Docker Compose"
	@echo "  docker-down      - Stop all services and remove containers"
	@echo "  check-env        - Check environment setup"

# Install dependencies
install: install-backend install-frontend

install-backend:
	@echo "\nInstalling Python dependencies..."
	pip install --upgrade pip
	pip install -e ".[dev]"
	pre-commit install

install-frontend:
	@echo "\nInstalling Node.js dependencies..."
	cd frontend && npm install

# Testing
test: test-backend test-frontend

test-backend:
	@echo "\nRunning backend tests..."
	pytest tests/ --cov=secure_image_encryption --cov-report=term-missing --cov-report=xml

test-frontend:
	@echo "\nRunning frontend tests..."
	cd frontend && npm test

# Linting
lint: lint-backend lint-frontend

lint-backend:
	@echo "\nLinting Python code..."
	black --check secure_image_encryption/ tests/
	isort --check-only secure_image_encryption/ tests/
	flake8 secure_image_encryption/ tests/
	mypy secure_image_encryption/

lint-frontend:
	@echo "\nLinting frontend code..."
	cd frontend && npm run lint

# Formatting
format: format-backend format-frontend

format-backend:
	@echo "\nFormatting Python code..."
	black secure_image_encryption/ tests/
	isort secure_image_encryption/ tests/

format-frontend:
	@echo "\nFormatting frontend code..."
	cd frontend && npm run format

# Cleaning
clean: clean-backend clean-frontend

clean-backend:
	@echo "\nCleaning Python build artifacts..."
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ .coverage htmlcov/ .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

clean-frontend:
	@echo "\nCleaning frontend build artifacts..."
	cd frontend && npm run clean

# Running
run-backend:
	@echo "\nStarting backend server..."
	python -m uvicorn backend.main:app --reload

run-frontend:
	@echo "\nStarting frontend development server..."
	cd frontend && npm start

# Docker
docker-build:
	@echo "\nBuilding Docker images..."
	docker-compose build

docker-up:
	@echo "\nStarting services with Docker Compose..."
	docker-compose up -d

docker-down:
	@echo "\nStopping services and removing containers..."
	docker-compose down

# Environment setup
check-env:
	@echo "\nChecking environment setup..."
	@echo "Python: $$(python --version 2>/dev/null || echo 'Not installed')"
	@echo "Node.js: $$(node --version 2>/dev/null || echo 'Not installed')"
	@echo "npm: $$(npm --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker: $$(docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker Compose: $$(docker-compose --version 2>/dev/null || echo 'Not installed')"

# Run the application
run:
	python -m secure_image_encryption

# Run with hot reload for development
dev:
	python -m uvicorn secure_image_encryption.main:app --reload

# Build Docker image
docker-build:
	docker build -t secure-image-encryption .

# Run Docker container
docker-run:
	docker run -p 8000:8000 secure-image-encryption

# Run all checks
check: lint test

# Pre-commit hook
pre-commit: format lint test

# Set up pre-commit hooks
setup-hooks:
	pre-commit install

# Install pre-commit hooks
install-hooks: setup-hooks
	pre-commit install --hook-type pre-commit --hook-type pre-push
