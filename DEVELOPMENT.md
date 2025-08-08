# Development Guide

This document provides detailed instructions for setting up the development environment, running tests, and contributing to the Secure Image Encryption System.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
  - [Python Environment](#python-environment)
  - [Node.js Backend](#nodejs-backend)
  - [Database Setup](#database-setup)
  - [Redis Setup](#redis-setup)
- [Running the Application](#running-the-application)
  - [Running with Docker](#running-with-docker)
  - [Running Locally](#running-locally)
- [Testing](#testing)
  - [Python Tests](#python-tests)
  - [API Tests](#api-tests)
- [Code Quality](#code-quality)
  - [Linting](#linting)
  - [Type Checking](#type-checking)
  - [Formatting](#formatting)
- [Debugging](#debugging)
- [Documentation](#documentation)
- [CI/CD](#cicd)

## Prerequisites

- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- Git
- PostgreSQL 13+
- Redis 6+

## Development Setup

### Python Environment

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```

### Node.js Backend

1. Install Node.js dependencies:
   ```bash
   cd backend
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Database Setup

1. Start PostgreSQL and Redis using Docker:
   ```bash
   docker-compose up -d db redis
   ```

2. Run database migrations:
   ```bash
   cd backend
   npx sequelize-cli db:migrate
   ```

### Redis Setup

Redis is used for caching and message brokering. It's automatically configured when using the Docker Compose setup.

## Running the Application

### Running with Docker (Recommended)

```bash
docker-compose up --build
```

### Running Locally

1. Start the backend server:
   ```bash
   cd backend
   npm run dev
   ```

2. In a separate terminal, run the Python application:
   ```bash
   python -m secure_image_encryption --help
   ```

## Testing

### Python Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=secure_image_encryption --cov-report=term-missing
```

### API Tests

Run API tests:
```bash
cd backend
npm test
```

## Code Quality

### Linting

Python:
```bash
flake8 secure_image_encryption tests
```

JavaScript/TypeScript:
```bash
cd backend
npm run lint
```

### Type Checking

Python:
```bash
mypy secure_image_encryption
```

### Formatting

Python:
```bash
black secure_image_encryption tests
isort secure_image_encryption tests
```

JavaScript/TypeScript:
```bash
cd backend
npm run format
```

## Debugging

### Python Debugging

Use the built-in `pdb` debugger:
```python
import pdb; pdb.set_trace()
```

Or use VS Code's debugger with the following launch configuration:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

### API Debugging

Use Postman or curl to test API endpoints:
```bash
# Example: Health check
curl http://localhost:8000/health
```

## Documentation

### API Documentation

Access the interactive API documentation at:
```
http://localhost:8000/api-docs
```

### Generating Documentation

Generate Python API documentation:
```bash
cd docs
make html
```

The documentation will be available in `docs/_build/html`.

## CI/CD

The project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml` and runs on every push and pull request.

### Manual Deployment

Deploy to production:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Monitoring

Access monitoring tools:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Check the connection string in `.env`
   - Run database migrations

2. **Redis Connection Issues**
   - Ensure Redis is running
   - Check the Redis URL in `.env`

3. **Docker Issues**
   - Ensure Docker is running
   - Try rebuilding the containers: `docker-compose build --no-cache`

## Getting Help

If you encounter any issues, please:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search the [issue tracker](https://github.com/yourusername/secure-image-encryption/issues)
3. Open a new issue if your problem isn't documented

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
