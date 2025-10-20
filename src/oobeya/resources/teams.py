# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Teams resource for Oobeya API."""

from typing import TYPE_CHECKING, List, Optional

from oobeya.models import (
    OobeyaResponseBoolean,
    SyncAnalysisTeamDTO,
    TeamAnalysisRequestDTO,
    TeamDTO,
    TeamPartialUpdateRequest,
)
from oobeya.utils import from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class TeamsResource:
    """Teams resource client for managing teams in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the teams resource."""
        self.client = client
        self.base_path = "/apis/v1/teams"

    def list_all(self) -> Optional[List[TeamDTO]]:
        """Get all teams."""
        response_data = self.client.get(f"{self.base_path}/all")
        if response_data and isinstance(response_data, list):
            teams = [from_dict(item, TeamDTO) for item in response_data]
            return [team for team in teams if team is not None]
        return None

    def create(self, team: TeamDTO) -> Optional[TeamDTO]:
        """Create a new team."""
        team_data = to_dict(team)
        response_data = self.client.post(self.base_path, json=team_data)
        return from_dict(response_data, TeamDTO) if response_data else None

    def update(self, team: TeamDTO) -> Optional[TeamDTO]:
        """Update an existing team."""
        team_data = to_dict(team)
        response_data = self.client.put(self.base_path, json=team_data)
        return from_dict(response_data, TeamDTO) if response_data else None

    def partial_update(self, team_id_or_name: str, update: TeamPartialUpdateRequest) -> Optional[OobeyaResponseBoolean]:
        """Partially update a team (PATCH)."""
        update_data = to_dict(update)
        response_data = self.client.patch(f"{self.base_path}/{team_id_or_name}", json=update_data)
        return from_dict(response_data, OobeyaResponseBoolean) if response_data else None

    def delete(self, team_id: str) -> Optional[bool]:
        """Delete a team."""
        response_data = self.client.delete(f"{self.base_path}/{team_id}")
        return bool(response_data) if response_data is not None else None

    def trigger_analysis(self, request: TeamAnalysisRequestDTO) -> Optional[bool]:
        """Trigger git pull request and DORA analysis."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/trigger-analysis", json=request_data)
        return bool(response_data) if response_data is not None else None

    def sync_analysis(self, request: SyncAnalysisTeamDTO) -> Optional[bool]:
        """Sync analysis."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/sync-analysis", json=request_data)
        return bool(response_data) if response_data is not None else None

    def replace_selection(self, request: SyncAnalysisTeamDTO) -> Optional[bool]:
        """Replace team selection."""
        request_data = to_dict(request)
        response_data = self.client.put(f"{self.base_path}/replace-selection", json=request_data)
        return bool(response_data) if response_data is not None else None
