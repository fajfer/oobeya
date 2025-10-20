<!--
SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>

SPDX-License-Identifier: EUPL-1.2
-->
# Development Guidelines

This document contains critical information about working with this codebase. Follow these guidelines precisely.

## Core Development Rules

1. Code Quality
   - Type hints required for all code
   - Public APIs must have docstrings
   - Functions must be focused and small
   - Follow existing patterns exactly
   - Line length: 120 chars maximum

2. Testing Requirements
   - Coverage: test edge cases and errors
   - New features require tests
   - Bug fixes require regression tests

3. Code Style
    - PEP 8 naming (snake_case for functions/variables)
    - Class names in PascalCase
    - Constants in UPPER_SNAKE_CASE
    - Document with docstrings
    - Use f-strings for formatting

4. Licensing
  - Always input SPDX-compliant headers to files
  - Update SPDX headers for year mismatch
    - eg. if it said 2025-2026 and the current year is 2027, change the date range to 2025-2027

- Use [conventional commits](https://www.conventionalcommits.org/) as a standard for committing
- NEVER ever mention a `co-authored-by` or similar aspects. In particular, never
  mention the tool used to create the commit message or PR.

## Code Formatting

1. Use black for code formatting

2. Type Checking
   - Requirements:
     - Explicit None checks for Optional
     - Type narrowing for strings
     - Version warnings can be ignored if checks pass

## Error Resolution

1. Common Issues
   - Line length:
     - Break strings with parentheses
     - Multi-line function calls
     - Split imports
   - Types:
     - Add None checks
     - Narrow string types
     - Match existing patterns

3. Best Practices
   - Run formatters before type checks
   - Keep changes minimal, only modify code related to the task at hand
   - Follow existing patterns
   - Document public APIs
   - Test thoroughly
   - DRY Code: Don't repeat yourself
   - Start with minimal functionality and verify it works before adding complexity

## Exception Handling

- **Always use `logger.exception()` instead of `logger.error()` when catching exceptions**
  - Don't include the exception in the message: `logger.exception("Failed")` not `logger.exception(f"Failed: {e}")`
- **Catch specific exceptions** where possible:
  - File ops: `except (OSError, PermissionError):`
  - JSON: `except json.JSONDecodeError:`
  - Network: `except (ConnectionError, TimeoutError):`
- **Only catch `Exception` for**:
  - Top-level handlers that must not crash
  - Cleanup blocks (log at debug level)

## Oobeya Python Library Specifications

### Project Requirements
- **Package Name**: `oobeya` (for PyPI)
- **Python Version**: Support from Ubuntu 24.04 LTS (Python 3.12+)
- **Package Manager**: `uv` for dependency management and project setup
- **Code Quality Tools**:
  - `black` for code formatting
  - `flake8` for linting
  - `mypy` for type checking (strict mode)

### Authentication
- **Support**: `Oobeya-API-Key` header authentication only
- Configurable base URL (default: `http://your-IP-or-Domain`)
- API key should be configurable via:
  - Constructor parameter
  - Environment variable (`OOBEYA_API_KEY`)

### API Implementation
- **Scope**: Implement ALL endpoints from the OpenAPI specification (api.json)
- **Approach**: Implement everything as-is first, then suggest improvements
- **Endpoints to cover**:
  1. Organization Level (01.Organization Level)
  2. User Management (02.User)
  3. Member Management (03.Member)
  4. Team Management (04.Team)
  5. Team Score Card (05.Team Score Card)
  6. Git Analysis (06.Git Analysis)
  7. Deployment (07.Deployment)
  8. Qwiser (08.Qwiser)
  9. Defect Detection (09.Defect Detection)
  10. Reports (10.Reports)
  11. External Test (11.External Test)
  12. API Key (12.Api Key)
  13. Bulk Operation (12.Bulk Operation)
  14. System (14.System)

### Error Handling Strategy
- **Custom Exception Hierarchy**: Use library-specific exceptions
  - Base: `OobeyaError` (or `OobeyaAPIError`)
  - Derived: `OobeyaAuthenticationError`, `OobeyaValidationError`, `OobeyaNotFoundError`, `OobeyaServerError`
- **Critical**: All custom exceptions MUST be clearly identifiable as library errors, NOT API errors
- **Documentation**: Clearly document that error handling is implemented by the library, as the API itself has limited error handling
- Example error message format: `[Oobeya Library] Authentication failed: Invalid API key`

### Testing Requirements
- **Framework**: `pytest`
- **Coverage**: Unit tests with mocked HTTP responses
- **Target**: Cover all implemented endpoints
- **Test Organization**:
  - Unit tests for each API resource/category
  - Mock all HTTP calls
  - Test error scenarios and edge cases
- No integration tests required (but structure should allow for future addition)

### Documentation Requirements
- **Code Documentation**:
  - Docstrings for all public APIs
  - Type hints throughout (mypy strict compliance)
  - Usage examples in docstrings where appropriate
- **SPDX Headers**: All files must include EUPL-1.2 license headers

### Development Workflow
1. Set up project with `uv init`
2. Validate existing models iwth openapi.json spec
3. Write unit tests for each new resource
5. Run quality checks: `black`, `flake8`, `mypy`
6. Ensure all tests pass
