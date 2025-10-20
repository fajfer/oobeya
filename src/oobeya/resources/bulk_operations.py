# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Bulk Operations resource for Oobeya API."""

from typing import TYPE_CHECKING, Any, Dict, Optional

from oobeya.models import BulkAnalysisPrepareRequest, SyncGitAnalysisDTO
from oobeya.utils import to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class BulkOperationsResource:
    """Bulk Operations resource client for bulk git analysis operations in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the bulk operations resource."""
        self.client = client
        self.base_path = "/apis/v1/bulk"

    def prepare_bulk_analyses(self, request: BulkAnalysisPrepareRequest) -> Optional[bool]:
        """Prepare bulk git analyses."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/analyses", json=request_data)

        return bool(response_data) if response_data is not None else None

    def get_bulk_analyses_file(self) -> Optional[bytes]:
        """Get bulk git analysis file."""
        response = self.client.get(f"{self.base_path}/analyses")
        # For binary file download, we need to handle the response differently
        if response:
            return response  # type: ignore
        return None

    def import_git_analysis(self, file_path: str) -> Optional[bool]:
        """Import new git analysis from file."""
        with open(file_path, "rb") as f:
            files: Dict[str, Any] = {"file": f}
            response_data = self.client.post(f"{self.base_path}/analyses/analysis", files=files)

            return bool(response_data) if response_data is not None else None

    def update_git_analysis(self, file_path: str) -> Optional[bool]:
        """Update git analysis from file."""
        with open(file_path, "rb") as f:
            files: Dict[str, Any] = {"file": f}
            response_data = self.client.put(f"{self.base_path}/analyses/analysis", files=files)

            return bool(response_data) if response_data is not None else None

    def sync_git_analysis(self, request: SyncGitAnalysisDTO) -> Optional[bool]:
        """Sync git analysis."""
        request_data = to_dict(request)
        response_data = self.client.put(f"{self.base_path}/analyses/sync", json=request_data)

        return bool(response_data) if response_data is not None else None
