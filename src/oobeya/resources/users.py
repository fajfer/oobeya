# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Users resource for Oobeya API."""

from typing import TYPE_CHECKING, List, Optional

from oobeya.models import DeveloperResource, PaginationResponse, UserRequestDTO
from oobeya.utils import build_query_params, from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class UsersResource:
    """
    Users resource client for managing users in Oobeya.

    This resource provides methods for CRUD operations on users.
    """

    def __init__(self, client: "OobeyaClient") -> None:
        """
        Initialize the users resource.

        Args:
            client: The Oobeya client instance
        """
        self.client = client
        self.base_path = "/apis/v1/users"

    def list(
        self,
        page: int = 0,
        size: int = 10,
        sort: Optional[List[str]] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        start_creation_date: Optional[str] = None,
        end_creation_date: Optional[str] = None,
        start_termination_date: Optional[str] = None,
        end_termination_date: Optional[str] = None,
        start_hire_date: Optional[str] = None,
        end_hire_date: Optional[str] = None,
    ) -> Optional[PaginationResponse]:
        """
        Get users with pagination.

        Args:
            page: Page number (default: 0)
            size: Page size (default: 10)
            sort: Sort criteria (default: ["modifyDate:DESC"])
            username: Filter by username
            email: Filter by email
            start_creation_date: Filter by creation date start
            end_creation_date: Filter by creation date end
            start_termination_date: Filter by termination date start
            end_termination_date: Filter by termination date end
            start_hire_date: Filter by hire date start
            end_hire_date: Filter by hire date end

        Returns:
            PaginationResponse with paginated user data
        """
        params = build_query_params(
            page=page,
            size=size,
            sort=sort or ["modifyDate:DESC"],
            username=username,
            email=email,
            startCreationDate=start_creation_date,
            endCreationDate=end_creation_date,
            startTerminationDate=start_termination_date,
            endTerminationDate=end_termination_date,
            startHireDate=start_hire_date,
            endHireDate=end_hire_date,
        )
        response_data = self.client.get(self.base_path, params=params)
        if not response_data:
            return None

        # Convert to PaginationResponse
        pagination = from_dict(response_data, PaginationResponse)

        # Convert contents from dicts to DeveloperResource objects
        if pagination and pagination.contents:
            pagination.contents = [
                from_dict(item, DeveloperResource) if isinstance(item, dict) else item for item in pagination.contents
            ]

        return pagination

    def get(self, user_id: str) -> Optional[DeveloperResource]:
        """
        Get a specific user by ID (developerId).

        Note: This endpoint may not be fully supported by the API.
        Use list() with filters instead if this fails.

        Args:
            user_id: The developer/user ID

        Returns:
            DeveloperResource object or None
        """
        response_data = self.client.get(f"{self.base_path}/{user_id}")
        return from_dict(response_data, DeveloperResource) if response_data else None

    def create(self, user: UserRequestDTO) -> Optional[DeveloperResource]:
        """
        Create a new user.

        Args:
            user: User data

        Returns:
            Created user as DeveloperResource
        """
        user_data = to_dict(user)
        response_data = self.client.post(self.base_path, json=user_data)
        return from_dict(response_data, DeveloperResource) if response_data else None

    def update(self, user: UserRequestDTO) -> Optional[DeveloperResource]:
        """
        Update an existing user.

        Args:
            user: User data with ID

        Returns:
            Updated user as DeveloperResource
        """
        user_data = to_dict(user)
        response_data = self.client.put(self.base_path, json=user_data)
        return from_dict(response_data, DeveloperResource) if response_data else None

    def delete(self, user_id: str) -> bool:
        """
        Delete a user.

        Args:
            user_id: The user ID (account ID, not developer ID) to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        response_data = self.client.delete(f"{self.base_path}/{user_id}")
        return bool(response_data) if response_data is not None else False
