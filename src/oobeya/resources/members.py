# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Members resource for Oobeya API."""

from typing import TYPE_CHECKING, List, Optional

from oobeya.models import DeveloperRequestDTO, PaginationResponse
from oobeya.utils import build_query_params, from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class MembersResource:
    """
    Members resource client for managing members in Oobeya.

    This resource provides methods for CRUD operations on members.
    """

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the members resource."""
        self.client = client
        self.base_path = "/apis/v1/members"

    def list(
        self,
        page: int = 0,
        size: int = 10,
        sort: Optional[List[str]] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[PaginationResponse]:
        """
        Get members with pagination.

        Args:
            page: Page number (default: 0)
            size: Page size (default: 10)
            sort: Sort criteria (default: ["modifyDate:DESC"])
            username: Filter by username
            email: Filter by email

        Returns:
            PaginationResponse with member data
        """
        params = build_query_params(
            page=page,
            size=size,
            sort=sort or ["modifyDate:DESC"],
            username=username,
            email=email,
        )
        response_data = self.client.get(self.base_path, params=params)
        return from_dict(response_data, PaginationResponse) if response_data else None

    def get(self, member_id: str) -> Optional[DeveloperRequestDTO]:
        """Get a specific member by ID."""
        response_data = self.client.get(f"{self.base_path}/{member_id}")
        return from_dict(response_data, DeveloperRequestDTO) if response_data else None

    def create(self, member: DeveloperRequestDTO) -> Optional[DeveloperRequestDTO]:
        """Create a new member."""
        member_data = to_dict(member)
        response_data = self.client.post(self.base_path, json=member_data)
        return from_dict(response_data, DeveloperRequestDTO) if response_data else None

    def update(self, member: DeveloperRequestDTO) -> Optional[DeveloperRequestDTO]:
        """Update an existing member."""
        member_data = to_dict(member)
        response_data = self.client.put(self.base_path, json=member_data)
        return from_dict(response_data, DeveloperRequestDTO) if response_data else None

    def delete(self, member_id: str) -> Optional[DeveloperRequestDTO]:
        """Delete a member."""
        response_data = self.client.delete(f"{self.base_path}/{member_id}")
        return from_dict(response_data, DeveloperRequestDTO) if response_data else None
