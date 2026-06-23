# Contributing to JARVIS AI Assistant

We love your input! We want to make contributing to JARVIS AI Assistant as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/yourusername/jarvis-ai-assistant/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/jarvis-ai-assistant/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

### Prerequisites

- Python 3.7+
- Git
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run tests**
   ```bash
   pytest
   ```

## Code Style

We use several tools to maintain code quality:

### Python Code Style

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:
```bash
# Format code
black .
isort .

# Check linting
flake8 .

# Type checking
mypy .
```

### Code Standards

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Include type hints where appropriate
- Keep functions small and focused
- Write self-documenting code

### Example Code Style

```python
"""
Module docstring explaining the purpose.
"""

from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ExampleClass:
    """
    Class docstring explaining the purpose and usage.
    
    Attributes:
        attribute_name: Description of the attribute
    """
    
    def __init__(self, parameter: str) -> None:
        """
        Initialize the class.
        
        Args:
            parameter: Description of the parameter
        """
        self.attribute_name = parameter
    
    def example_method(self, input_data: Dict[str, Any]) -> Optional[str]:
        """
        Method docstring explaining what it does.
        
        Args:
            input_data: Description of input parameter
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When input is invalid
        """
        try:
            # Implementation here
            result = self._process_data(input_data)
            return result
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            raise ValueError(f"Invalid input data: {e}")
    
    def _process_data(self, data: Dict[str, Any]) -> str:
        """Private method for internal processing."""
        # Implementation
        return "processed"
```

## Testing

### Test Structure

- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- End-to-end tests in `tests/e2e/`

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from src.example_module import ExampleClass


class TestExampleClass:
    """Test cases for ExampleClass."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.example = ExampleClass("test_parameter")
    
    def test_example_method_success(self):
        """Test successful execution of example_method."""
        # Arrange
        input_data = {"key": "value"}
        expected_result = "processed"
        
        # Act
        result = self.example.example_method(input_data)
        
        # Assert
        assert result == expected_result
    
    def test_example_method_invalid_input(self):
        """Test example_method with invalid input."""
        # Arrange
        invalid_data = {}
        
        # Act & Assert
        with pytest.raises(ValueError):
            self.example.example_method(invalid_data)
    
    @patch('src.example_module.external_dependency')
    def test_with_mock(self, mock_dependency):
        """Test with mocked external dependency."""
        # Arrange
        mock_dependency.return_value = "mocked_result"
        
        # Act
        result = self.example.example_method({"key": "value"})
        
        # Assert
        assert result == "mocked_result"
        mock_dependency.assert_called_once()
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_example.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_example"
```

## Documentation

### Docstring Style

We use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2 with default value
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Example:
        >>> result = example_function("hello", 42)
        >>> print(result)
        True
    """
    pass
```

### Documentation Updates

- Update README.md for user-facing changes
- Update API documentation for new features
- Add examples for new functionality
- Update architecture diagrams if needed

## Feature Development

### Feature Request Process

1. **Check existing issues** to avoid duplicates
2. **Create detailed issue** with:
   - Clear description of the feature
   - Use cases and benefits
   - Proposed implementation approach
   - Potential challenges or considerations

### Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement feature**
   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation

3. **Test thoroughly**
   - Unit tests for individual components
   - Integration tests for feature workflow
   - Manual testing of user scenarios

4. **Submit pull request**
   - Clear title and description
   - Link to related issues
   - Include screenshots/demos if applicable

### Feature Categories

#### Core Features
- Voice processing improvements
- AI integration enhancements
- Authentication system updates
- System control capabilities

#### Integrations
- New AI providers
- Additional phone features
- Third-party service connections
- Hardware integrations

#### User Interface
- Web interface improvements
- New settings and controls
- Accessibility enhancements
- Mobile responsiveness

#### Performance
- Speed optimizations
- Memory usage improvements
- Battery life considerations
- Scalability enhancements

## Bug Fixes

### Bug Report Requirements

Include the following information:

1. **Environment Details**
   - Operating system and version
   - Python version
   - JARVIS version
   - Hardware specifications

2. **Steps to Reproduce**
   - Exact steps that trigger the bug
   - Input data or commands used
   - Expected vs actual behavior

3. **Error Information**
   - Full error messages
   - Log files (if available)
   - Screenshots or recordings

4. **Additional Context**
   - When the bug started occurring
   - Any recent changes to system
   - Workarounds discovered

### Bug Fix Process

1. **Reproduce the bug** in development environment
2. **Write failing test** that demonstrates the issue
3. **Implement fix** with minimal changes
4. **Verify fix** passes new and existing tests
5. **Update documentation** if behavior changes

## Security

### Reporting Security Issues

**DO NOT** create public GitHub issues for security vulnerabilities.

Instead, email security concerns to: security@jarvis-ai.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Guidelines

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Validate all user inputs
- Follow secure coding practices
- Keep dependencies updated

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Discord**: Real-time chat (link in README)
- **Email**: Direct contact for sensitive issues

### Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](CODE_OF_CONDUCT.md).

### Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special recognition for major features

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Changelog updated
- [ ] Release notes prepared
- [ ] Security review completed

## Getting Help

### Development Questions

1. Check existing documentation
2. Search GitHub issues
3. Ask in GitHub Discussions
4. Contact maintainers directly

### Useful Resources

- [Python Style Guide](https://pep8.org/)
- [Git Best Practices](https://git-scm.com/book)
- [Testing Best Practices](https://docs.pytest.org/)
- [Documentation Guide](https://www.sphinx-doc.org/)

---

Thank you for contributing to JARVIS AI Assistant! 🤖✨