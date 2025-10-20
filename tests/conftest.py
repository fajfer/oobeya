# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock
from oobeya.client import OobeyaClient


@pytest.fixture
def mock_client():
    """Create a mock Oobeya client for testing."""
    client = Mock(spec=OobeyaClient)
    client.base_url = "http://test.oobeya.io"
    client.api_key = "test-api-key"
    return client


@pytest.fixture
def oobeya_client():
    """Create a real Oobeya client with test credentials."""
    return OobeyaClient(api_key="test-api-key", base_url="http://test.oobeya.io")
