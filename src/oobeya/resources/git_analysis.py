# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Git Analysis resource for Oobeya API."""

from typing import TYPE_CHECKING, List, Optional

from oobeya.models import (
    DoraAnalysisRequestDTO,
    DoraSummaryDTO,
    GitAnalysisDTO,
    GitAnalysisRequestDTO,
    JenkinsDoraAnalysisRequestDTO,
)
from oobeya.utils import build_query_params, from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class GitAnalysisResource:
    """Git Analysis resource client for managing git analysis in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the git analysis resource."""
        self.client = client
        self.base_path = "/apis/v1/analysis"

    def list(
        self,
        page: int = 0,
        size: int = 10,
        sort: Optional[List[str]] = None,
    ) -> Optional[List[GitAnalysisDTO]]:
        """Get git analyses with pagination."""
        params = build_query_params(
            page=page,
            size=size,
            sort=sort or ["modifyDate:DESC"],
        )
        response_data = self.client.get(self.base_path, params=params)
        if response_data and isinstance(response_data, list):
            analyses = [from_dict(item, GitAnalysisDTO) for item in response_data]
            return [analysis for analysis in analyses if analysis is not None]
        return None

    def create(self, analysis: GitAnalysisRequestDTO) -> Optional[GitAnalysisDTO]:
        """Create a new git analysis."""
        analysis_data = to_dict(analysis)
        response_data = self.client.post(self.base_path, json=analysis_data)
        return from_dict(response_data, GitAnalysisDTO) if response_data else None

    def delete(self, analysis_id: str) -> Optional[bool]:
        """Delete a git analysis."""
        response_data = self.client.delete(f"{self.base_path}/{analysis_id}")

        return bool(response_data) if response_data is not None else None

    def delete_commit(self, analysis_id: str, commit_id: str) -> Optional[bool]:
        """Delete a commit from git analysis."""
        response_data = self.client.delete(f"{self.base_path}/{analysis_id}/commit/{commit_id}")

        return bool(response_data) if response_data is not None else None

    def create_jenkins_dora_analysis(
        self, analysis_id: str, jenkins_request: JenkinsDoraAnalysisRequestDTO
    ) -> Optional[bool]:
        """Create Jenkins DORA analysis."""
        jenkins_data = to_dict(jenkins_request)
        response_data = self.client.post(f"{self.base_path}/{analysis_id}/dora/jenkins", json=jenkins_data)

        return bool(response_data) if response_data is not None else None

    def create_bulk_dora_analysis(self, dora_request: DoraAnalysisRequestDTO) -> Optional[bool]:
        """Create bulk DORA analysis."""
        dora_data = to_dict(dora_request)
        response_data = self.client.post(f"{self.base_path}/all-dora-analyses", json=dora_data)

        return bool(response_data) if response_data is not None else None

    def delete_bulk_dora_analysis(self) -> Optional[bool]:
        """Delete bulk DORA analysis."""
        response_data = self.client.delete(f"{self.base_path}/all-dora-analyses")

        return bool(response_data) if response_data is not None else None

    def trigger_bulk_dora_analysis(self) -> Optional[bool]:
        """Trigger bulk DORA analysis."""
        response_data = self.client.post(f"{self.base_path}/trigger-all-dora-analyses")

        return bool(response_data) if response_data is not None else None

    def get_dora_summary_metrics(
        self,
        widgets: List[str],
        team_id: Optional[str] = None,
        analysis_id: Optional[List[str]] = None,
        from_timestamp: Optional[int] = None,
        to_timestamp: Optional[int] = None,
    ) -> Optional[DoraSummaryDTO]:
        """Get DORA summary metrics."""
        params = build_query_params(
            widgets=widgets,
            teamId=team_id,
            analysisId=analysis_id,
            **{"from": from_timestamp, "to": to_timestamp},
        )
        response_data = self.client.get(f"{self.base_path}/dora-summary-metrics", params=params)
        return from_dict(response_data, DoraSummaryDTO) if response_data else None
