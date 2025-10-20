# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Organization Level resource for Oobeya API."""

from typing import TYPE_CHECKING, List, Optional

from oobeya.models import OrganizationLevelDTO
from oobeya.utils import from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class OrganizationLevelResource:
    """Organization Level resource client for managing organization levels in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the organization level resource."""
        self.client = client
        self.base_path = "/apis/v1/organization-level"

    def list_all(self) -> Optional[List[OrganizationLevelDTO]]:
        """Get all organization levels."""
        response_data = self.client.get(self.base_path)
        if response_data and isinstance(response_data, list):
            levels = [from_dict(item, OrganizationLevelDTO) for item in response_data]
            return [level for level in levels if level is not None]
        return None

    def create(self, org_level: OrganizationLevelDTO) -> Optional[OrganizationLevelDTO]:
        """Create a new organization level."""
        org_level_data = to_dict(org_level)
        response_data = self.client.post(self.base_path, json=org_level_data)
        return from_dict(response_data, OrganizationLevelDTO) if response_data else None

    def update(self, org_level_id: str, org_level: OrganizationLevelDTO) -> Optional[OrganizationLevelDTO]:
        """Update an existing organization level."""
        org_level_data = to_dict(org_level)
        response_data = self.client.put(f"{self.base_path}/{org_level_id}", json=org_level_data)
        return from_dict(response_data, OrganizationLevelDTO) if response_data else None
