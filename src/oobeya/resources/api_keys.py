# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""API Keys resource for Oobeya API."""

from typing import TYPE_CHECKING, List, Optional

from oobeya.models import ApiKeyRequestDTO, ApiTokenDTO
from oobeya.utils import from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class ApiKeysResource:
    """API Keys resource client for managing API keys in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the API keys resource."""
        self.client = client
        self.base_path = "/apis/v1/api-keys"

    def list_all(self) -> Optional[List[ApiTokenDTO]]:
        """Get all API keys."""
        response_data = self.client.get(self.base_path)
        if response_data and isinstance(response_data, list):
            api_keys = [from_dict(item, ApiTokenDTO) for item in response_data]
            return [key for key in api_keys if key is not None]
        return None

    def create(self, api_key: ApiKeyRequestDTO) -> Optional[ApiTokenDTO]:
        """Create a new API key."""
        api_key_data = to_dict(api_key)
        response_data = self.client.post(self.base_path, json=api_key_data)
        return from_dict(response_data, ApiTokenDTO) if response_data else None

    def delete(self, api_key_id: str) -> Optional[bool]:
        """Delete an API key."""
        response_data = self.client.delete(f"{self.base_path}/{api_key_id}")

        return bool(response_data) if response_data is not None else None
