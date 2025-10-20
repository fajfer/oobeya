# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Defect Detection resource for Oobeya API."""

from typing import TYPE_CHECKING, Optional

from oobeya.models import DefectDetectionRequest
from oobeya.utils import to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class DefectDetectionResource:
    """Defect Detection resource client for managing defect detections in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the defect detection resource."""
        self.client = client
        self.base_path = "/apis/v1/defect-detections"

    def create(self, request: DefectDetectionRequest) -> Optional[bool]:
        """Create new defect detections."""
        request_data = to_dict(request)
        response_data = self.client.post(self.base_path, json=request_data)

        return bool(response_data) if response_data is not None else None
