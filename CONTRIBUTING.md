# Contributing to Years of Lead

Thank you for your interest in contributing to Years of Lead! This document provides guidelines and information for contributors.

## 🎯 Getting Started

### Prerequisites
- Python 3.12 or higher
- Git
- Basic understanding of Python development

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/years-of-lead.git
cd years-of-lead

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests to ensure everything works
python test_improvements.py
```

## 🔧 Development Workflow

### 1. Choose an Issue
- Check the [Issues](https://github.com/yourusername/years-of-lead/issues) page
- Look for issues labeled `good first issue` for beginners
- Comment on the issue to let others know you're working on it

### 2. Create a Branch
```bash
# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Changes
- Follow the coding standards below
- Write tests for new features
- Update documentation as needed

### 4. Test Your Changes
```bash
# Run the test suite
python test_improvements.py

# Run linting
flake8 src/

# Run type checking (if available)
mypy src/
```

### 5. Commit Your Changes
```bash
# Add your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: brief description of changes

- Detailed description of what was added
- Any important notes or considerations
- Related issue: #123"
```

### 6. Push and Create Pull Request
```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## 📝 Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters
- Use meaningful variable and function names

### Code Structure
```python
"""
Module docstring explaining the purpose of this module.
"""

import os
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass

# Constants at the top
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

@dataclass
class ExampleClass:
    """Class docstring explaining the purpose of this class."""

    name: str
    value: int

    def example_method(self, param: str) -> bool:
        """
        Method docstring explaining what this method does.

        Args:
            param: Description of the parameter

        Returns:
            Description of the return value

        Raises:
            ValueError: When something goes wrong
        """
        if not param:
            raise ValueError("Parameter cannot be empty")

        return len(param) > 0
```

### Type Hints
- Use type hints for all function parameters and return values
- Import types from the `typing` module
- Use `Optional[Type]` for parameters that can be None

### Error Handling
```python
def safe_operation(data: Dict[str, Any]) -> Optional[str]:
    """Example of proper error handling."""
    try:
        result = process_data(data)
        return result
    except KeyError as e:
        logger.error(f"Missing key in data: {e}")
        return None
    except ValueError as e:
        logger.error(f"Invalid data format: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

## 🧪 Testing

### Writing Tests
- Write tests for all new features
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

```python
import pytest
from unittest.mock import Mock, patch
from game.character_creation import CharacterCreator

def test_character_creation_success():
    """Test successful character creation."""
    creator = CharacterCreator()
    character = creator.create_character(
        name="Test Character",
        background_type=BackgroundType.MILITARY,
        primary_trait=PersonalityTrait.LOYAL,
        secondary_trait=PersonalityTrait.PRAGMATIC
    )

    assert character.name == "Test Character"
    assert character.background.type == BackgroundType.MILITARY
    assert character.traits.primary_trait == PersonalityTrait.LOYAL

def test_character_creation_invalid_background():
    """Test character creation with invalid background."""
    creator = CharacterCreator()

    with pytest.raises(ValueError, match="Invalid background type"):
        creator.create_character(
            name="Test",
            background_type="invalid",
            primary_trait=PersonalityTrait.LOYAL,
            secondary_trait=PersonalityTrait.PRAGMATIC
        )
```

### Running Tests
```bash
# Run all tests
python test_improvements.py

# Run specific test file
python -m pytest tests/test_character_creation.py

# Run with coverage
python -m pytest --cov=src tests/
```

## 📚 Documentation

### Code Documentation
- Write docstrings for all classes and methods
- Use Google-style docstring format
- Include examples for complex functions
- Document exceptions and edge cases

### User Documentation
- Update README.md for user-facing changes
- Add examples and usage instructions
- Include screenshots for UI changes
- Update installation instructions if needed

### Technical Documentation
- Document new systems and architectures
- Update API documentation
- Include diagrams for complex systems
- Document configuration options

## 🎮 Game Design Guidelines

### Character System
- New backgrounds should have clear mechanical benefits
- Personality traits should affect gameplay meaningfully
- Skills should be balanced and useful
- Trauma should have realistic psychological effects

### Mission System
- Missions should have clear objectives and consequences
- Risk assessment should be comprehensive
- Locations should have distinct characteristics
- Team composition should matter

### Intelligence System
- Intelligence events should be actionable
- Sources should have realistic reliability
- Patterns should emerge from multiple events
- Threat assessment should be dynamic

### Narrative Design
- Choices should have meaningful consequences
- Moral complexity should be realistic
- Characters should feel human and relatable
- Story should be engaging and immersive

## 🐛 Bug Reports

### Before Reporting
- Check existing issues for duplicates
- Try to reproduce the bug consistently
- Gather relevant information (error messages, logs, etc.)

### Bug Report Template
```markdown
**Bug Description**
Brief description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python Version: [e.g., 3.12.0]
- Game Version: [e.g., v1.0.1]

**Additional Information**
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting
- Check the [To-Do List](TODO.md) for existing plans
- Consider if the feature fits the game's vision
- Think about implementation complexity

### Feature Request Template
```markdown
**Feature Description**
Brief description of the feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it could be implemented

**Alternatives Considered**
Other approaches you considered

**Additional Information**
Any other relevant information
```

## 🔄 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] No new warnings or errors
- [ ] Feature is complete and working

### Pull Request Template
```markdown
**Description**
Brief description of changes

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

**Testing**
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

**Documentation**
- [ ] README updated
- [ ] Code comments added
- [ ] API documentation updated

**Related Issues**
Closes #123
```

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested
- `wontfix`: This will not be worked on

## 📞 Getting Help

### Questions and Discussion
- Use [GitHub Discussions](https://github.com/yourusername/years-of-lead/discussions)
- Ask questions in the Q&A category
- Share ideas in the Ideas category

### Code Reviews
- Be respectful and constructive
- Focus on the code, not the person
- Suggest improvements, don't just point out problems
- Explain the reasoning behind your suggestions

## 🎉 Recognition

Contributors will be recognized in:
- The README.md file
- Release notes
- The game credits (if applicable)

## 📄 License

By contributing to Years of Lead, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Years of Lead! Your help makes this project better for everyone.
