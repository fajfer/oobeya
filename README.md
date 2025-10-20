<!--
SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>

SPDX-License-Identifier: EUPL-1.2
-->
# Oobeya Python Client Library

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-EUPL--1.2-green.svg)](LICENSE)

A community maintained, Python client library for interacting with the [Oobeya API](https://www.oobeya.io) - Software Engineering Intelligence Platform. This library provides a comprehensive interface to manage users, teams, git analysis, DORA metrics, deployments, and more.

## Installation

### Using pip

```bash
pip install oobeya
```

### Using uv (recommended)

```bash
uv pip install oobeya
```

### From source

```bash
git clone https://github.com/fajfer/oobeya.git
cd oobeya
uv pip install -e .
```

## Quick Start

```python
from oobeya import OobeyaClient

# Initialize the client
client = OobeyaClient(
    api_key="your-api-key-here",  # Or set OOBEYA_API_KEY env var
    base_url="http://your-oobeya-instance"
)

# List users
users = client.users.list(page=0, size=10)

# Get a specific user
user = client.users.get("user-id")

# Create a team
from oobeya.models import TeamDTO

team = TeamDTO(
    organization_name="Engineering",
    unit_name="Backend Team",
    unit_members=["member-1", "member-2"],
    unit_leads=["member-1"]
)
created_team = client.teams.create(team)

# Get DORA metrics
dora_metrics = client.git_analysis.get_dora_summary_metrics(
    widgets=["DEPLOYMENT_FREQUENCY", "LEAD_TIME_FOR_CHANGES"],
    analysis_id=["analysis-123"]
)
```

## Authentication

The library supports authentication via the `Oobeya-API-Key` header. You can provide the API key in two ways:

### 1. Via constructor parameter

```python
client = OobeyaClient(api_key="your-api-key-here")
```

### 2. Via environment variable

```bash
export OOBEYA_API_KEY="your-api-key-here"
```

```python
client = OobeyaClient()  # Will use OOBEYA_API_KEY from environment
```

## Supported Resources

The library provides access to all Oobeya API resources:

| Resource | Description | Example |
|----------|-------------|---------|
| `users` | User management | `client.users.list()` |
| `members` | Member (developer) management | `client.members.create(member)` |
| `teams` | Team management | `client.teams.list_all()` |
| `team_score_cards` | Team score cards | `client.team_score_cards.create(card)` |
| `git_analysis` | Git analysis & DORA metrics | `client.git_analysis.get_dora_summary_metrics()` |
| `deployments` | Deployment tracking | `client.deployments.list()` |
| `qwiser` | SonarQube analysis | `client.qwiser.start_analysis(request)` |
| `defect_detection` | Defect detection | `client.defect_detection.create(request)` |
| `reports` | Team and member reports | `client.reports.get_team_commits(team_id, start, end)` |
| `external_test` | External test metrics | `client.external_test.create_execution(request)` |
| `bulk_operations` | Bulk git operations | `client.bulk_operations.sync_git_analysis(request)` |
| `api_keys` | API key management | `client.api_keys.list_all()` |
| `system` | System operations | `client.system.get_logs()` |
| `organization_level` | Organization levels | `client.organization_level.list_all()` |

## Usage Examples

### User Management

```python
from oobeya import OobeyaClient
from oobeya.models import UserRequestDTO

client = OobeyaClient(api_key="your-api-key")

# Create a user
user = UserRequestDTO(
    name="John",
    surname="Doe",
    username="john.doe",
    email="john.doe@example.com",
    user_type="DB",
    company_role="DEVELOPER",
    hire_date="2025-01-15T00:00:00+00:00"
)
created_user = client.users.create(user)

# Update a user
user.id = created_user.id
user.company_role = "TEAM_LEAD"
updated_user = client.users.update(user)

# Delete a user
client.users.delete(created_user.id)
```

### Team Management

```python
from oobeya.models import TeamDTO, TeamPartialUpdateRequest

# Create a team
team = TeamDTO(
    organization_name="Engineering",
    unit_name="Backend Team",
    unit_members=["member-1", "member-2"],
    unit_leads=["member-1"]
)
created_team = client.teams.create(team)

# Partial update (add/remove members)
update = TeamPartialUpdateRequest(
    add_unit_members=["member-3"],
    remove_unit_members=["member-2"]
)
client.teams.partial_update(created_team.id, update)

# List all teams
teams = client.teams.list_all()
```

### Git Analysis & DORA Metrics

```python
from oobeya.models import GitAnalysisRequestDTO

# Create git analysis
analysis = GitAnalysisRequestDTO(
    datasource_id="datasource-123",
    project_name="backend-service",
    branch="main",
    type="GITLAB",
    release_strategy_type="GITFLOW_RELEASE",
    analysis_type="PULL_REQUEST",
    is_include_deployment=True
)
created_analysis = client.git_analysis.create(analysis)

# Get DORA metrics
dora_metrics = client.git_analysis.get_dora_summary_metrics(
    widgets=[
        "DEPLOYMENT_FREQUENCY",
        "LEAD_TIME_FOR_CHANGES",
        "CHANGE_FAILURE_RATE",
        "MEAN_TIME_TO_RECOVERY"
    ],
    analysis_id=[created_analysis.id]
)

print(f"Deployment Frequency: {dora_metrics.deployment_frequency.formatted_value}")
print(f"Lead Time: {dora_metrics.lead_time_for_changes.formatted_value}")
```

### Deployments

```python
from datetime import datetime, timezone
from oobeya.models import DeploymentRequestDTO

# Create a deployment
deployment = DeploymentRequestDTO(
    analysis_id="analysis-123",
    clone_url="https://github.com/myorg/backend-service.git",
    pipeline_start_at=datetime.now(timezone.utc),
    last_commit_sha="abc123",
    deployment_type="RELEASE",
    analysis_type="PULL_REQUEST",
    deployed_at=datetime.now(timezone.utc),
    name="v1.2.3",
    title="Release 1.2.3"
)
created_deployment = client.deployments.create(deployment)

# List deployments
deployments = client.deployments.list(page=0, size=10)
```

### Reports

```python
# Get team-based commit metrics
team_commits = client.reports.get_team_commits(
    team_id="team-123",
    start_date="2025-01-01",
    end_date="2025-01-31"
)

# Get member-based quality metrics
member_quality = client.reports.get_member_qualities(
    member_id="member-456",
    start_date="2025-01-01",
    end_date="2025-01-31"
)

# Get team pull request metrics
team_prs = client.reports.get_team_pull_requests(
    team_id="team-123",
    start_date="2025-01-01",
    end_date="2025-01-31"
)
```

For more comprehensive examples, see the [examples](examples/) directory:

- [crud_users.py](examples/crud_users.py) - User CRUD operations
- [crud_members.py](examples/crud_members.py) - Member CRUD operations
- [crud_teams.py](examples/crud_teams.py) - Team CRUD operations
- [crud_git_analysis.py](examples/crud_git_analysis.py) - Git analysis and DORA metrics
- [crud_deployments.py](examples/crud_deployments.py) - Deployment tracking

## Error Handling

The library provides clear, library-specific exceptions to help you handle errors:

```python
from oobeya import OobeyaClient
from oobeya.exceptions import (
    OobeyaAuthenticationError,
    OobeyaNotFoundError,
    OobeyaValidationError,
    OobeyaServerError,
    OobeyaTimeoutError,
    OobeyaConnectionError
)

client = OobeyaClient(api_key="your-api-key")

try:
    user = client.users.get("invalid-user-id")
except OobeyaAuthenticationError:
    print("Authentication failed - check your API key")
except OobeyaNotFoundError:
    print("User not found")
except OobeyaValidationError as e:
    print(f"Validation error: {e}")
except OobeyaServerError as e:
    print(f"Server error: {e}")
except OobeyaTimeoutError:
    print("Request timed out")
except OobeyaConnectionError:
    print("Could not connect to Oobeya")
```

**Note**: All exceptions are prefixed with `[Oobeya Library]` to clearly distinguish them from API-level errors, as the Oobeya API itself has limited error handling.

## Context Manager Support

The client can be used as a context manager to ensure proper cleanup:

```python
with OobeyaClient(api_key="your-api-key") as client:
    users = client.users.list()
    # Session is automatically closed when exiting the context
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/fajfer/oobeya.git
cd oobeya

# Install dependencies with uv
uv pip install -e ".[dev]"
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/oobeya --cov-report=html

# Run specific test file
pytest tests/unit/test_users.py
```

### Code quality checks

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type check with mypy
mypy src/
```

## Requirements

- Python 3.12 or higher (Ubuntu 24.04 LTS)
- Dependencies:
  - `requests>=2.31.0`
  - `python-dateutil>=2.8.2`

## License

This project is licensed under the European Union Public License 1.2 (EUPL-1.2). See the [LICENSE](LICENSE) file for details.

## Links

- [Oobeya Website](https://www.oobeya.io)
- [Oobeya Documentation](https://www.oobeya.io)
- [GitHub Repository](https://github.com/fajfer/oobeya)
<!-- - [PyPI Package](https://pypi.org/project/oobeya/) -->
