# Tests

This directory contains unit and integration tests for the RAG application backend.

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
```

### Run Tests with Verbose Output

```bash
pytest -v
```

## Test Structure

- **conftest.py**: Pytest configuration and shared fixtures
- **test_auth.py**: Authentication and JWT token tests
- **test_text_processing.py**: Text chunking and cleaning tests
- **test_api.py**: API endpoint integration tests
- **test_embeddings.py**: Embedding and vector search tests
- **test_config.py**: Configuration and environment variable tests

## Test Coverage

The test suite covers:
- Password hashing and verification
- JWT token creation and validation
- Text processing utilities
- API request/response structures
- Embedding operations and vector search
- Configuration validation

## CI/CD Integration

Tests are automatically run in the CI/CD pipeline as specified in `submission.yml`.
