# Development Guide

This guide provides comprehensive instructions for setting up and working with the MCP RAG System development environment.

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm 7 or higher
- Git
- Docker and Docker Compose (optional)

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Install development dependencies:
   ```bash
   npm install --save-dev @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint eslint-config-prettier eslint-plugin-react eslint-plugin-react-hooks prettier
   ```

## Development Tools

### Code Quality Tools

#### Backend

- **Black**: Code formatter
  - Configuration: `pyproject.toml`
  - Usage: `black .`

- **isort**: Import sorter
  - Configuration: `pyproject.toml`
  - Usage: `isort .`

- **Flake8**: Linter
  - Configuration: `pyproject.toml`
  - Usage: `flake8 .`

- **MyPy**: Type checker
  - Configuration: `pyproject.toml`
  - Usage: `mypy .`

- **Bandit**: Security linter
  - Configuration: `pyproject.toml`
  - Usage: `bandit -r .`

#### Frontend

- **ESLint**: JavaScript/TypeScript linter
  - Configuration: `.eslintrc.json`
  - Usage: `npm run lint`

- **Prettier**: Code formatter
  - Configuration: `.prettierrc`
  - Usage: `npm run format`

- **TypeScript**: Type checker
  - Configuration: `tsconfig.json`
  - Usage: `npm run type-check`

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality before commits. The configuration is in `.pre-commit-config.yaml`.

Hooks include:
- Code formatting (Black, Prettier)
- Import sorting (isort)
- Linting (Flake8, ESLint)
- Type checking (MyPy)
- Security checks (Bandit)

### Testing

#### Backend Testing

1. Run tests:
   ```bash
   pytest
   ```

2. Generate coverage report:
   ```bash
   pytest --cov=mcp --cov-report=html
   ```

#### Frontend Testing

1. Run tests:
   ```bash
   npm test
   ```

2. Run tests with coverage:
   ```bash
   npm test -- --coverage
   ```

### Development Workflow

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run pre-commit hooks:
   ```bash
   pre-commit run --all-files
   ```

4. Run tests:
   ```bash
   # Backend
   pytest
   
   # Frontend
   npm test
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

6. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request

### Best Practices

1. **Code Style**
   - Follow PEP 8 for Python code
   - Use TypeScript for frontend code
   - Write meaningful commit messages
   - Keep functions small and focused
   - Add docstrings to Python functions
   - Add JSDoc comments to TypeScript functions

2. **Testing**
   - Write tests for new features
   - Maintain test coverage above 80%
   - Use meaningful test names
   - Test edge cases and error conditions

3. **Documentation**
   - Update documentation when changing features
   - Add comments for complex logic
   - Keep README up to date
   - Document API changes

4. **Security**
   - Never commit sensitive data
   - Use environment variables for secrets
   - Follow security best practices
   - Run security checks regularly

### Troubleshooting

1. **Pre-commit Hooks Fail**
   - Run `pre-commit run --all-files` to see detailed errors
   - Fix formatting issues with `black .` or `prettier --write .`
   - Fix import issues with `isort .`

2. **Tests Fail**
   - Check test output for specific failures
   - Run individual test files to isolate issues
   - Check test coverage report

3. **Type Checking Errors**
   - Backend: Run `mypy .` for detailed errors
   - Frontend: Run `npm run type-check` for detailed errors

4. **Build Issues**
   - Clear build caches
   - Check for dependency conflicts
   - Verify environment setup

### Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Material-UI Documentation](https://mui.com/getting-started/usage/) 