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
    OobeyaRateLimitError,
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
        mock_response.raise_for_status.side_effect = HTTPError(
            "500 Server Error: Internal Server Error", response=mock_response
        )
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


class TestOobeyaClientResourceProperties:
    """Test OobeyaClient resource property access."""

    def test_users_property(self):
        """Test users property returns UsersResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.users import UsersResource

        assert isinstance(client.users, UsersResource)
        # Test caching
        assert client.users is client.users

    def test_members_property(self):
        """Test members property returns MembersResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.members import MembersResource

        assert isinstance(client.members, MembersResource)
        # Test caching
        assert client.members is client.members

    def test_teams_property(self):
        """Test teams property returns TeamsResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.teams import TeamsResource

        assert isinstance(client.teams, TeamsResource)
        assert client.teams is client.teams

    def test_team_score_cards_property(self):
        """Test team_score_cards property returns TeamScoreCardsResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.team_score_cards import TeamScoreCardsResource

        assert isinstance(client.team_score_cards, TeamScoreCardsResource)
        assert client.team_score_cards is client.team_score_cards

    def test_git_analysis_property(self):
        """Test git_analysis property returns GitAnalysisResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.git_analysis import GitAnalysisResource

        assert isinstance(client.git_analysis, GitAnalysisResource)
        assert client.git_analysis is client.git_analysis

    def test_deployments_property(self):
        """Test deployments property returns DeploymentsResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.deployments import DeploymentsResource

        assert isinstance(client.deployments, DeploymentsResource)
        assert client.deployments is client.deployments

    def test_qwiser_property(self):
        """Test qwiser property returns QwiserResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.qwiser import QwiserResource

        assert isinstance(client.qwiser, QwiserResource)
        assert client.qwiser is client.qwiser

    def test_defect_detection_property(self):
        """Test defect_detection property returns DefectDetectionResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.defect_detection import DefectDetectionResource

        assert isinstance(client.defect_detection, DefectDetectionResource)
        assert client.defect_detection is client.defect_detection

    def test_reports_property(self):
        """Test reports property returns ReportsResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.reports import ReportsResource

        assert isinstance(client.reports, ReportsResource)
        assert client.reports is client.reports

    def test_external_test_property(self):
        """Test external_test property returns ExternalTestResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.external_test import ExternalTestResource

        assert isinstance(client.external_test, ExternalTestResource)
        assert client.external_test is client.external_test

    def test_bulk_operations_property(self):
        """Test bulk_operations property returns BulkOperationsResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.bulk_operations import BulkOperationsResource

        assert isinstance(client.bulk_operations, BulkOperationsResource)
        assert client.bulk_operations is client.bulk_operations

    def test_api_keys_property(self):
        """Test api_keys property returns ApiKeysResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.api_keys import ApiKeysResource

        assert isinstance(client.api_keys, ApiKeysResource)
        assert client.api_keys is client.api_keys

    def test_system_property(self):
        """Test system property returns SystemResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.system import SystemResource

        assert isinstance(client.system, SystemResource)
        assert client.system is client.system

    def test_organization_level_property(self):
        """Test organization_level property returns OrganizationLevelResource."""
        client = OobeyaClient(api_key="test-key")
        from oobeya.resources.organization_level import OrganizationLevelResource

        assert isinstance(client.organization_level, OrganizationLevelResource)
        assert client.organization_level is client.organization_level


class TestOobeyaClientAdditionalErrorHandling:
    """Test additional error handling in OobeyaClient."""

    @patch("oobeya.client.requests.Session.request")
    def test_403_authentication_error(self, mock_request):
        """Test 403 forbidden error."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = HTTPError("403 Client Error: Forbidden", response=mock_response)
        mock_response.text = "Access denied"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaAuthenticationError) as exc_info:
            client.get("/test")
        assert "Authentication failed" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_429_rate_limit_error(self, mock_request):
        """Test 429 rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = HTTPError("429 Too Many Requests", response=mock_response)
        mock_response.text = "Rate limit exceeded"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaRateLimitError) as exc_info:
            client.get("/test")
        assert "Rate limit exceeded" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_other_http_error(self, mock_request):
        """Test other HTTP errors (e.g., 418)."""
        mock_response = Mock()
        mock_response.status_code = 418
        mock_response.raise_for_status.side_effect = HTTPError("418 I'm a teapot", response=mock_response)
        mock_response.text = "I'm a teapot"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaServerError) as exc_info:
            client.get("/test")
        assert "HTTP error" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_error_with_json_response(self, mock_request):
        """Test error handling with JSON response body."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = HTTPError("400 Bad Request", response=mock_response)
        mock_response.json.return_value = {"error": "Invalid field", "details": "Missing required param"}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaValidationError) as exc_info:
            client.post("/test", json={})
        assert "Invalid field" in str(exc_info.value)

    @patch("oobeya.client.requests.Session.request")
    def test_empty_response(self, mock_request):
        """Test handling of empty response."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.content = b""
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        result = client.delete("/test/123")
        assert result is None

    @patch("oobeya.client.requests.Session.request")
    def test_payload_unwrapping(self, mock_request):
        """Test that payload is unwrapped from Oobeya response structure."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"version": "1.0", "referenceId": "123", "payload": {"id": "user-1"}}'
        mock_response.json.return_value = {"version": "1.0", "referenceId": "123", "payload": {"id": "user-1"}}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        result = client.get("/test")
        assert result == {"id": "user-1"}

    @patch("oobeya.client.requests.Session.request")
    def test_invalid_json_response(self, mock_request):
        """Test handling of invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"not json"
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaServerError) as exc_info:
            client.get("/test")
        assert "Invalid JSON response" in str(exc_info.value)


class TestOobeyaClientHttpMethods:
    """Test HTTP method wrappers."""

    @patch("oobeya.client.requests.Session.request")
    def test_put_request(self, mock_request):
        """Test PUT request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"updated": true}'
        mock_response.json.return_value = {"updated": True}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        result = client.put("/test", json={"name": "updated"})
        assert result == {"updated": True}

    @patch("oobeya.client.requests.Session.request")
    def test_patch_request(self, mock_request):
        """Test PATCH request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"patched": true}'
        mock_response.json.return_value = {"patched": True}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        result = client.patch("/test", json={"field": "value"})
        assert result == {"patched": True}

    @patch("oobeya.client.requests.Session.request")
    def test_delete_request(self, mock_request):
        """Test DELETE request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"deleted": true}'
        mock_response.json.return_value = {"deleted": True}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        result = client.delete("/test/123")
        assert result == {"deleted": True}

    @patch("oobeya.client.requests.Session.request")
    def test_file_upload(self, mock_request):
        """Test file upload removes Content-Type header."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"uploaded": true}'
        mock_response.json.return_value = {"uploaded": True}
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        files = {"file": ("test.txt", b"test content")}
        result = client.post("/upload", files=files)

        assert result == {"uploaded": True}
        # Verify Content-Type header was set to None for file upload
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs.get("headers", {}).get("Content-Type") is None

    @patch("oobeya.client.requests.Session.request")
    def test_error_with_json_parse_failure(self, mock_request):
        """Test error handling when JSON parsing fails for error response."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = HTTPError("400 Bad Request", response=mock_response)
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_response.text = "Plain text error message"
        mock_request.return_value = mock_response

        client = OobeyaClient(api_key="test-key")
        with pytest.raises(OobeyaValidationError) as exc_info:
            client.post("/test", json={})
        assert "Plain text error message" in str(exc_info.value)
