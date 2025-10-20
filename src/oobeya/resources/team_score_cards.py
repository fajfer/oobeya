# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Team Score Cards resource for Oobeya API."""

from typing import TYPE_CHECKING, Optional

from oobeya.models import TeamScoreCardDTO
from oobeya.utils import from_dict, to_dict

if TYPE_CHECKING:
    from oobeya.client import OobeyaClient


class TeamScoreCardsResource:
    """Team Score Cards resource client for managing team score cards in Oobeya."""

    def __init__(self, client: "OobeyaClient") -> None:
        """Initialize the team score cards resource."""
        self.client = client
        self.base_path = "/apis/v1/team-score-cards"

    def create(self, score_card: TeamScoreCardDTO) -> Optional[TeamScoreCardDTO]:
        """Create a new team score card."""
        score_card_data = to_dict(score_card)
        response_data = self.client.post(self.base_path, json=score_card_data)
        return from_dict(response_data, TeamScoreCardDTO) if response_data else None

    def update(self, score_card: TeamScoreCardDTO) -> Optional[TeamScoreCardDTO]:
        """Update an existing team score card."""
        score_card_data = to_dict(score_card)
        response_data = self.client.put(self.base_path, json=score_card_data)
        return from_dict(response_data, TeamScoreCardDTO) if response_data else None
