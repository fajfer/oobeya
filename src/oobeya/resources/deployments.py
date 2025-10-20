# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Deployments resource for Oobeya API."""

from typing import TYPE_CHECKING, List, Optional

from oobeya.models import DeploymentDTO, DeploymentRequestDTO
from oobeya.utils import build_query_params, from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class DeploymentsResource:
    """Deployments resource client for managing deployments in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the deployments resource."""
        self.client = client
        self.base_path = "/apis/v1/deployments"

    def list(
        self,
        page: int = 0,
        size: int = 10,
        sort: Optional[List[str]] = None,
    ) -> Optional[List[DeploymentDTO]]:
        """Get deployments with pagination."""
        params = build_query_params(
            page=page,
            size=size,
            sort=sort or ["modifyDate:DESC"],
        )
        response_data = self.client.get(self.base_path, params=params)
        if response_data and isinstance(response_data, list):
            deployments = [from_dict(item, DeploymentDTO) for item in response_data]
            return [deployment for deployment in deployments if deployment is not None]
        return None

    def create(self, deployment: DeploymentRequestDTO) -> Optional[DeploymentDTO]:
        """Create a new deployment."""
        deployment_data = to_dict(deployment)
        response_data = self.client.post(self.base_path, json=deployment_data)
        return from_dict(response_data, DeploymentDTO) if response_data else None

    def delete(self, deployment_id: str) -> Optional[bool]:
        """Delete a deployment."""
        response_data = self.client.delete(f"{self.base_path}/{deployment_id}")

        return bool(response_data) if response_data is not None else None
