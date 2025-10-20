# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""System resource for Oobeya API."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class SystemResource:
    """System resource client for system operations in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the system resource."""
        self.client = client
        self.base_path = "/apis/v1/systems"

    def get_logs(self) -> Optional[str]:
        """Get system logs."""
        response_data = self.client.get(f"{self.base_path}/logs")
        return str(response_data) if response_data is not None else None

    def clear_git_analyses(self) -> Optional[bool]:
        """Clear analyses for commits before 2 years."""
        response_data = self.client.delete(f"{self.base_path}/clear-git-analyses")

        return bool(response_data) if response_data is not None else None
