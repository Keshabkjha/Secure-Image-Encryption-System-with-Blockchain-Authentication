# Contributing to Secure Image Encryption System

First off, thank you for considering contributing to our project! We appreciate your time and effort in making this project better.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#-getting-started)
- [How to Contribute](#-how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Environment](#-development-environment)
- [Coding Standards](#-coding-standards)
- [Commit Message Guidelines](#-commit-message-guidelines)
- [License](#-license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report any unacceptable behavior to [keshabkumarjha876@gmail.com](mailto:keshabkumarjha876@gmail.com).

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Docker (optional)
- Hedera Testnet Account (for blockchain features)

### Setting Up the Development Environment

1. **Fork the Repository**
   
   Click the "Fork" button on the top right of the [GitHub repository](https://github.com/Keshabkjha/Secure-Image-Encryption-System-with-Blockchain-Authentication).

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/Secure-Image-Encryption-System-with-Blockchain-Authentication.git
   cd Secure-Image-Encryption-System-with-Blockchain-Authentication
   ```

3. **Set Up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

4. **Set Up Node.js Dependencies**
   ```bash
   cd web
   npm install
   ```

## 🤝 How to Contribute

### Reporting Bugs

1. **Check Existing Issues**
   - Before creating a new issue, please check if a similar issue already exists.

2. **Create a New Issue**
   - Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template
   - Provide detailed steps to reproduce the issue
   - Include error messages and screenshots if applicable
   - Specify your environment (OS, Python version, etc.)

### Suggesting Enhancements

1. **Check Existing Proposals**
   - Search for similar feature requests

2. **Create a New Feature Request**
   - Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template
   - Clearly describe the problem you're trying to solve
   - Explain why this enhancement would be valuable
   - Suggest a proposed solution if you have one

### Your First Code Contribution

1. **Find an Issue**
   - Look for issues labeled "good first issue" or "help wanted"
   - Comment on the issue to let others know you're working on it

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Follow the coding standards
   - Write tests for your changes
   - Update documentation as needed

4. **Run Tests**
   ```bash
   pytest
   cd web && npm test
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

### Pull Requests

1. **Create a Pull Request**
   - Open a pull request against the `main` branch
   - Use the PR template to provide necessary details
   - Reference any related issues

2. **Code Review**
   - Address any review comments
   - Update your PR as needed
   - Ensure all tests pass

3. **Merge**
   - A maintainer will review and merge your PR
   - Thank you for your contribution! 🎉

## 🛠 Development Environment

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_encryption.py

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Linting and Formatting

```bash
# Python formatting with Black
black src/

# Python linting with flake8
flake8 src/
# Type checking with mypy
mypy src/
```

### Docker Development

```bash
# Build the development container
docker-compose -f docker-compose.dev.yml build

# Start the development environment
docker-compose -f docker-compose.dev.yml up
```

## 📝 Coding Standards

### Python
- Follow PEP 8 style guide
- Use type hints for all functions and methods
- Write docstrings for all public functions/classes/modules
- Keep functions small and focused
- Use meaningful variable and function names

### JavaScript/TypeScript
- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Use TypeScript for type safety
- Write JSDoc comments for public APIs

## ✨ Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

### Examples:
```
feat(encryption): add support for AES-256 encryption
fix(ui): resolve layout issue on mobile devices
docs: update API documentation
```

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).uting to SecureCircle

We're excited you're interested in contributing to SecureCircle! Before you begin, please take a moment to read these guidelines.

## 🛠 Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/Keshabkjha/Encryption-Yolo-Circle-passoord.git
   cd Encryption-Yolo-Circle-passoord
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Node.js environment**
   ```bash
   cd Backend
   npm install
   ```

## 🚀 Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test thoroughly

3. Ensure all tests pass:
   ```bash
   # Add test commands here when available
   ```

4. Commit your changes with a clear message:
   ```bash
   git commit -m "feat: add new encryption feature"
   ```

5. Push to your fork and open a Pull Request

## 📝 Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Update the documentation if needed
- Include tests for new features
- Follow the existing code style
- Reference any related issues

## 🧪 Testing

Please ensure all tests pass before submitting a PR:

```bash
# Add test commands here when available
```

## 📜 Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## 🙋 Need Help?

If you have questions, feel free to open an issue or reach out to the maintainers.
