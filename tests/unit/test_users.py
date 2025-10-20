# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for Users resource."""

from unittest.mock import Mock

import pytest

from oobeya.client import OobeyaClient
from oobeya.models import UserRequestDTO
from oobeya.resources.users import UsersResource


@pytest.fixture
def users_resource():
    """Create a users resource with mocked client."""
    client = Mock(spec=OobeyaClient)
    return UsersResource(client)


class TestUsersResource:
    """Test UsersResource methods."""

    def test_list_users(self, users_resource):
        """Test listing users."""
        mock_response = {
            "version": "v1",
            "referenceId": "ref123",
            "payload": {"contents": [], "totalElements": 0},
        }
        users_resource.client.get.return_value = mock_response

        result = users_resource.list(page=0, size=10)

        users_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_user(self, users_resource):
        """Test getting a single user."""
        mock_response = {"id": "user123", "userName": "testuser", "enabled": True}
        users_resource.client.get.return_value = mock_response

        result = users_resource.get("user123")

        users_resource.client.get.assert_called_once_with("/apis/v1/users/user123")
        assert result is not None
        assert result.id == "user123"

    def test_create_user(self, users_resource):
        """Test creating a user."""
        user = UserRequestDTO(
            name="John",
            surname="Doe",
            username="johndoe",
            email="john@example.com",
            user_type="DB",
            company_role="DEVELOPER",
        )
        mock_response = {
            "id": "user123",
            "userName": "johndoe",
            "fullName": "John Doe",
            "enabled": True,
        }
        users_resource.client.post.return_value = mock_response

        result = users_resource.create(user)

        users_resource.client.post.assert_called_once()
        assert result is not None
        assert result.id == "user123"

    def test_update_user(self, users_resource):
        """Test updating a user."""
        user = UserRequestDTO(id="user123", name="John", surname="Doe", username="johndoe")
        mock_response = {
            "id": "user123",
            "userName": "johndoe",
            "fullName": "John Doe",
        }
        users_resource.client.put.return_value = mock_response

        result = users_resource.update(user)

        users_resource.client.put.assert_called_once()
        assert result is not None

    def test_delete_user(self, users_resource):
        """Test deleting a user."""
        mock_response = {"id": "user123", "userName": "johndoe"}
        users_resource.client.delete.return_value = mock_response

        result = users_resource.delete("user123")

        users_resource.client.delete.assert_called_once_with("/apis/v1/users/user123")
        assert result is not None
