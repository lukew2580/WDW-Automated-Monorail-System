# Contributing to WDW Automated Monorail System

We welcome contributions from the community! This document outlines the process for contributing to the WDW Automated Monorail System project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

- Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- Provide detailed steps to reproduce
- Include screenshots if applicable
- Specify the expected vs. actual behavior

### Suggesting Enhancements

- Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case and why it's valuable
- Provide mockups or examples if possible

### Pull Requests

1. Fork the repository and create your branch from `main`
2. Follow the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md)
3. Ensure your code passes all tests
4. Update documentation as needed
5. Submit your pull request for review

## Development Setup

### Prerequisites

- Python 3.12+
- Blender 3.4+
- Git
- Node.js (for web components)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/WDW-Automated-Monorail-System.git
cd WDW-Automated-Monorail-System

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install Blender addons (if needed)
# Follow specific instructions in the documentation
```

## Coding Standards

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Include docstrings for all public functions and classes
- Write unit tests for new functionality

### Blender Scripts

- Use clear variable names
- Add comments for complex operations
- Follow Blender Python API conventions
- Test scripts in Blender's scripting environment

### Documentation

- Use Markdown format
- Keep documentation up-to-date
- Include examples where helpful
- Use clear, concise language

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_sensor_framework.py

# Run with coverage
python -m pytest --cov=.
```

### Test Coverage

- Aim for 80%+ test coverage
- Test edge cases and error conditions
- Include both unit and integration tests

## Version Control

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

<body>

<footer>
```

Common types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

## Community

### Communication

- Join our [Discord server](https://discord.gg/invite/zocomputer) for discussions
- Use GitHub Issues for bug reports and feature requests
- Participate in community meetings (see calendar)

### Code Reviews

- Be respectful and constructive
- Focus on code quality and functionality
- Provide clear, actionable feedback
- Respond promptly to review comments

## License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Questions?

If you have any questions about contributing, please:
- Check our [FAQ](docs/FAQ.md)
- Ask in our [Discord community](https://discord.gg/invite/zocomputer)
- Open a GitHub Discussion

Thank you for contributing to the WDW Automated Monorail System! 🚝

