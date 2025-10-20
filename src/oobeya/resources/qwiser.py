# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Qwiser resource for Oobeya API."""

from typing import TYPE_CHECKING, Optional

from oobeya.models import QwiserAnalysisRequestDTO
from oobeya.utils import to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class QwiserResource:
    """Qwiser resource client for managing Qwiser (SonarQube) analysis in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the qwiser resource."""
        self.client = client
        self.base_path = "/apis/v1/qwiser"

    def start_analysis(self, request: QwiserAnalysisRequestDTO) -> Optional[bool]:
        """Start Qwiser analysis."""
        request_data = to_dict(request)
        response_data = self.client.post(f"{self.base_path}/analysis", json=request_data)

        return bool(response_data) if response_data is not None else None
