# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for OobeyaClient."""

import os

import pytest
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
    HTTPError,
    Timeout,
)
from unittest.mock import Mock, patch

from oobeya.client import OobeyaClient
from oobeya.exceptions import (
    OobeyaAuthenticationError,
    OobeyaConnectionError,
    OobeyaNotFoundError,
    OobeyaServerError,
    OobeyaTimeoutError,
    OobeyaValidationError,
)


class TestOobeyaClientInit:
    """Test OobeyaClient initialization."""

    def test_init_with_api_key(self):
        """Test initialization with API key parameter."""
        client = OobeyaClient(api_key="test-key", base_url="http://test.com")
        assert client.api_key == "test-key"
        assert client.base_url == "http://test.com"

    def test_init_from_env(self):
        """Test initialization from environment variable."""
        with patch.dict(os.environ, {"OOBEYA_API_KEY": "env-key"}):
            client = OobeyaClient(base_url="http://test.com")
            assert client.api_key == "env-key"

    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(OobeyaAuthenticationError) as exc_info:
                OobeyaClient(base_url="http://test.com")
            assert "API key is required" in str(exc_info.value)

    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is removed from base URL."""
        client = OobeyaClient(api_key="test-key", base_url="http://test.com/")
        assert client.base_url == "http://test.com"


class TestOobeyaClientRequests:
    """Test OobeyaClient HTTP request methods."""

    @patch("oobeya.client.requests.Session.request")
    def test_get_request(self, mock_request):
        """Test GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"result": "success"}'
        mock_response.json.return_value = {"result": "success"}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        result = client.get("/test")

        assert result == {"result": "success"}
        mock_request.assert_called_once()

    @patch("oobeya.client.requests.Session.request")
    def test_post_request(self, mock_request):
        """Test POST request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"id": "123"}'
        mock_response.json.return_value = {"id": "123"}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        result = client.post("/test", json={"name": "test"})

        assert result == {"id": "123"}

    @patch("oobeya.client.requests.Session.request")
    def test_timeout_error(self, mock_request):
        """Test timeout handling."""
        mock_request.side_effect = Timeout("Request timed out")

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaTimeoutError) as exc_info:
            client.get("/test")
        assert "timed out" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_connection_error(self, mock_request):
        """Test connection error handling."""
        mock_request.side_effect = RequestsConnectionError("Connection failed")

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaConnectionError) as exc_info:
            client.get("/test")
        assert "Failed to connect" in str(exc_info.value)


class TestOobeyaClientErrorHandling:
    """Test OobeyaClient error handling."""

    @patch("oobeya.client.requests.Session.request")
    def test_401_authentication_error(self, mock_request):
        """Test 401 authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError("401 Client Error: Unauthorized", response=mock_response)
        mock_response.text = "Invalid API key"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaAuthenticationError) as exc_info:
            client.get("/test")
        assert "Authentication failed" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_404_not_found_error(self, mock_request):
        """Test 404 not found error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error: Not Found", response=mock_response)
        mock_response.text = "Resource not found"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaNotFoundError) as exc_info:
            client.get("/test/123")
        assert "not found" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_400_validation_error(self, mock_request):
        """Test 400 validation error."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = HTTPError("400 Client Error: Bad Request", response=mock_response)
        mock_response.text = "Invalid parameters"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaValidationError) as exc_info:
            client.post("/test", json={"invalid": "data"})
        assert "Validation failed" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_500_server_error(self, mock_request):
        """Test 500 server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error: Internal Server Error", response=mock_response)
        mock_response.text = "Server error"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaServerError) as exc_info:
            client.get("/test")
        assert "Server error" in str(exc_info.value)


class TestOobeyaClientContextManager:
    """Test OobeyaClient as context manager."""

    def test_context_manager(self):
        """Test using client as context manager."""
        with OobeyaClient(api_key="test-key") as client:
            assert client.api_key == "test-key"
            assert client.session is not None
