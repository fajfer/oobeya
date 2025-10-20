# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Reports resource for Oobeya API."""

from typing import TYPE_CHECKING, Optional

from oobeya.models import (
    MemberCommitReportResponse,
    MemberPullRequestReportResponse,
    MemberQualityReportResponse,
    TeamCommitReportResponse,
    TeamPullRequestReportResponse,
    TeamQualityReportResponse,
)
from oobeya.utils import build_query_params, from_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class ReportsResource:
    """Reports resource client for retrieving reports from Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the reports resource."""
        self.client = client
        self.base_path = "/apis/v1/reports"

    def get_member_qualities(
        self, member_id: str, start_date: str, end_date: str
    ) -> Optional[MemberQualityReportResponse]:
        """Get member-based quality metrics."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/member/{member_id}/qualities", params=params)
        return from_dict(response_data, MemberQualityReportResponse) if response_data else None

    def get_member_pull_requests(
        self, member_id: str, start_date: str, end_date: str
    ) -> Optional[MemberPullRequestReportResponse]:
        """Get member-based pull request metrics."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/member/{member_id}/pull-requests", params=params)
        return from_dict(response_data, MemberPullRequestReportResponse) if response_data else None

    def get_member_commits(
        self, member_id: str, start_date: str, end_date: str
    ) -> Optional[MemberCommitReportResponse]:
        """Get member-based commit metrics."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/member/{member_id}/commits", params=params)
        return from_dict(response_data, MemberCommitReportResponse) if response_data else None

    def get_team_qualities(self, team_id: str, start_date: str, end_date: str) -> Optional[TeamQualityReportResponse]:
        """Get team-based quality metrics."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/team/{team_id}/qualities", params=params)
        return from_dict(response_data, TeamQualityReportResponse) if response_data else None

    def get_team_pull_requests(
        self, team_id: str, start_date: str, end_date: str
    ) -> Optional[TeamPullRequestReportResponse]:
        """Get team-based pull request metrics."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/team/{team_id}/pull-requests", params=params)
        return from_dict(response_data, TeamPullRequestReportResponse) if response_data else None

    def get_team_commits(self, team_id: str, start_date: str, end_date: str) -> Optional[TeamCommitReportResponse]:
        """Get team-based commit metrics."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/team/{team_id}/commits", params=params)
        return from_dict(response_data, TeamCommitReportResponse) if response_data else None

    def get_team_member_qualities(
        self, team_id: str, member_id: str, start_date: str, end_date: str
    ) -> Optional[MemberQualityReportResponse]:
        """Get member-based quality metrics in team."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/team/{team_id}/member/{member_id}/qualities", params=params)
        return from_dict(response_data, MemberQualityReportResponse) if response_data else None

    def get_team_member_pull_requests(
        self, team_id: str, member_id: str, start_date: str, end_date: str
    ) -> Optional[MemberPullRequestReportResponse]:
        """Get member-based pull request metrics in team."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(
            f"{self.base_path}/team/{team_id}/developer/{member_id}/pull-requests", params=params
        )
        return from_dict(response_data, MemberPullRequestReportResponse) if response_data else None

    def get_team_member_commits(
        self, team_id: str, member_id: str, start_date: str, end_date: str
    ) -> Optional[MemberCommitReportResponse]:
        """Get member-based commit metrics in team."""
        params = build_query_params(startDate=start_date, endDate=end_date)
        response_data = self.client.get(f"{self.base_path}/team/{team_id}/developer/{member_id}/commits", params=params)
        return from_dict(response_data, MemberCommitReportResponse) if response_data else None
