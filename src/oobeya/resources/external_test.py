# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""External Test resource for Oobeya API."""

from typing import TYPE_CHECKING, Optional

from oobeya.models import (
    CreateBugRequest,
    CreateCoverageRequest,
    CreateDefectRequest,
    CreateExecutionRequest,
    ExternalBugResource,
    ExternalCoverageResource,
    ExternalExecutionResource,
)
from oobeya.utils import from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class ExternalTestResource:
    """External Test resource client for managing external test metrics in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the external test resource."""
        self.client = client
        self.base_path = "/apis/v1/test/external"

    # Execution methods
    def create_execution(self, request: CreateExecutionRequest) -> Optional[ExternalExecutionResource]:
        """Create execution."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/execution", json=request_data)
        return from_dict(response_data, ExternalExecutionResource) if response_data else None

    def get_last_execution(self, application_id: str) -> Optional[ExternalExecutionResource]:
        """Get last execution."""
        response_data = self.client.get(f"{self.base_path}/execution/last/{application_id}")
        return from_dict(response_data, ExternalExecutionResource) if response_data else None

    def delete_execution(self, execution_id: str, scenario_id: str) -> Optional[bool]:
        """Delete execution."""
        response_data = self.client.delete(f"{self.base_path}/execution/{execution_id}/scenario/{scenario_id}")

        return bool(response_data) if response_data is not None else None

    # Defect methods
    def create_defect(self, request: CreateDefectRequest) -> Optional[CreateDefectRequest]:
        """Create defect."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/defect", json=request_data)
        return from_dict(response_data, CreateDefectRequest) if response_data else None

    def get_last_defect(self, application_id: str) -> Optional[CreateDefectRequest]:
        """Get last defect."""
        response_data = self.client.get(f"{self.base_path}/defect/last/application/{application_id}")
        return from_dict(response_data, CreateDefectRequest) if response_data else None

    def delete_defect(self, application_id: str, problem_no: str) -> Optional[bool]:
        """Delete defect."""
        response_data = self.client.delete(
            f"{self.base_path}/defect/application/{application_id}/problem-no/{problem_no}"
        )

        return bool(response_data) if response_data is not None else None

    # Coverage methods
    def create_coverage(self, request: CreateCoverageRequest) -> Optional[ExternalCoverageResource]:
        """Create coverage."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/coverage", json=request_data)
        return from_dict(response_data, ExternalCoverageResource) if response_data else None

    def get_last_coverage(self, application_id: str, coverage_service: str) -> Optional[ExternalCoverageResource]:
        """Get last coverage."""
        response_data = self.client.get(
            f"{self.base_path}/coverage/last/{application_id}/coverage-service/{coverage_service}"
        )
        return from_dict(response_data, ExternalCoverageResource) if response_data else None

    def delete_coverage(self, coverage_id: str) -> Optional[bool]:
        """Delete coverage."""
        response_data = self.client.delete(f"{self.base_path}/coverage/{coverage_id}")

        return bool(response_data) if response_data is not None else None

    # Bug methods
    def create_bug(self, request: CreateBugRequest) -> Optional[ExternalBugResource]:
        """Create bug."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/bug", json=request_data)
        return from_dict(response_data, ExternalBugResource) if response_data else None

    def get_last_bug(self, application_id: str) -> Optional[ExternalBugResource]:
        """Get last bug."""
        response_data = self.client.get(f"{self.base_path}/bug/last/{application_id}")
        return from_dict(response_data, ExternalBugResource) if response_data else None

    def delete_bug(self, bug_id: str) -> Optional[bool]:
        """Delete bug."""
        response_data = self.client.delete(f"{self.base_path}/bug/{bug_id}")

        return bool(response_data) if response_data is not None else None
