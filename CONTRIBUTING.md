# Contributing to Ambrosio

Thank you for your interest in contributing to Ambrosio! Here's how you can help:

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ambrosio.git
   cd ambrosio
   ```
3. Set up virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Testing Strategy

### Unit Tests
- Tests for individual components
- Located in `tests/unit/`
- Run with:
  ```bash
  pytest tests/unit/
  ```

### Integration Tests
- Tests for component interactions
- Located in `tests/integration/`
- Run with:
  ```bash
  pytest tests/integration/
  ```

### End-to-End Tests
- Full system tests
- Located in `tests/e2e/`
- Run with:
  ```bash
  pytest tests/e2e/
  ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Keep functions small and focused
- Write docstrings for all public methods

## Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Write tests for new functionality
4. Run all tests:
   ```bash
   pytest
   ```
5. Update documentation if needed
6. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Open a pull request

## Reporting Issues

When reporting issues, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

## Code of Conduct

Please note we have a code of conduct. Please follow it in all your interactions with the project.

## Maintenance Guidelines

- Regularly update dependencies
- Monitor system performance
- Review and update documentation
- Address security vulnerabilities promptly
