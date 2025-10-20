# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Main Oobeya client class."""

import os
from typing import TYPE_CHECKING, Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from oobeya.exceptions import (
    OobeyaAuthenticationError,
    OobeyaConnectionError,
    OobeyaNotFoundError,
    OobeyaRateLimitError,
    OobeyaServerError,
    OobeyaTimeoutError,
    OobeyaValidationError,
)

if TYPE_CHECKING:
    from oobeya.resources.api_keys import ApiKeysResource
    from oobeya.resources.bulk_operations import BulkOperationsResource
    from oobeya.resources.defect_detection import DefectDetectionResource
    from oobeya.resources.deployments import DeploymentsResource
    from oobeya.resources.external_test import ExternalTestResource
    from oobeya.resources.git_analysis import GitAnalysisResource
    from oobeya.resources.members import MembersResource
    from oobeya.resources.organization_level import OrganizationLevelResource
    from oobeya.resources.qwiser import QwiserResource
    from oobeya.resources.reports import ReportsResource
    from oobeya.resources.system import SystemResource
    from oobeya.resources.team_score_cards import TeamScoreCardsResource
    from oobeya.resources.teams import TeamsResource
    from oobeya.resources.users import UsersResource


class OobeyaClient:
    """
    Main client for interacting with the Oobeya API.

    This client handles authentication, HTTP requests, and error handling
    for all Oobeya API operations.

    Example:
        >>> client = OobeyaClient(api_key="your-api-key", base_url="http://your-oobeya-instance")
        >>> users = client.users.list()
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "http://your-IP-or-Domain",
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the Oobeya client.

        Args:
            api_key: Oobeya API key. If not provided, will try to read from
                    OOBEYA_API_KEY environment variable
            base_url: Base URL of the Oobeya instance
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries for failed requests (default: 3)

        Raises:
            OobeyaAuthenticationError: If no API key is provided or found in environment
        """
        self.api_key = api_key or os.getenv("OOBEYA_API_KEY")
        if not self.api_key:
            raise OobeyaAuthenticationError(
                "API key is required. Provide it via the api_key parameter "
                "or set the OOBEYA_API_KEY environment variable."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # Set up session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update(
            {
                "Oobeya-API-Key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Initialize resource clients (lazy-loaded to avoid circular imports)
        self._users: Optional[Any] = None
        self._members: Optional[Any] = None
        self._teams: Optional[Any] = None
        self._team_score_cards: Optional[Any] = None
        self._git_analysis: Optional[Any] = None
        self._deployments: Optional[Any] = None
        self._qwiser: Optional[Any] = None
        self._defect_detection: Optional[Any] = None
        self._reports: Optional[Any] = None
        self._external_test: Optional[Any] = None
        self._bulk_operations: Optional[Any] = None
        self._api_keys: Optional[Any] = None
        self._system: Optional[Any] = None
        self._organization_level: Optional[Any] = None

    @property
    def users(self) -> "UsersResource":
        """Get the users resource client."""
        if self._users is None:
            from oobeya.resources.users import UsersResource

            self._users = UsersResource(self)
        return self._users

    @property
    def members(self) -> "MembersResource":
        """Get the members resource client."""
        if self._members is None:
            from oobeya.resources.members import MembersResource

            self._members = MembersResource(self)
        return self._members

    @property
    def teams(self) -> "TeamsResource":
        """Get the teams resource client."""
        if self._teams is None:
            from oobeya.resources.teams import TeamsResource

            self._teams = TeamsResource(self)
        return self._teams

    @property
    def team_score_cards(self) -> "TeamScoreCardsResource":
        """Get the team score cards resource client."""
        if self._team_score_cards is None:
            from oobeya.resources.team_score_cards import TeamScoreCardsResource

            self._team_score_cards = TeamScoreCardsResource(self)
        return self._team_score_cards

    @property
    def git_analysis(self) -> "GitAnalysisResource":
        """Get the git analysis resource client."""
        if self._git_analysis is None:
            from oobeya.resources.git_analysis import GitAnalysisResource

            self._git_analysis = GitAnalysisResource(self)
        return self._git_analysis

    @property
    def deployments(self) -> "DeploymentsResource":
        """Get the deployments resource client."""
        if self._deployments is None:
            from oobeya.resources.deployments import DeploymentsResource

            self._deployments = DeploymentsResource(self)
        return self._deployments

    @property
    def qwiser(self) -> "QwiserResource":
        """Get the qwiser resource client."""
        if self._qwiser is None:
            from oobeya.resources.qwiser import QwiserResource

            self._qwiser = QwiserResource(self)
        return self._qwiser

    @property
    def defect_detection(self) -> "DefectDetectionResource":
        """Get the defect detection resource client."""
        if self._defect_detection is None:
            from oobeya.resources.defect_detection import DefectDetectionResource

            self._defect_detection = DefectDetectionResource(self)
        return self._defect_detection

    @property
    def reports(self) -> "ReportsResource":
        """Get the reports resource client."""
        if self._reports is None:
            from oobeya.resources.reports import ReportsResource

            self._reports = ReportsResource(self)
        return self._reports

    @property
    def external_test(self) -> "ExternalTestResource":
        """Get the external test resource client."""
        if self._external_test is None:
            from oobeya.resources.external_test import ExternalTestResource

            self._external_test = ExternalTestResource(self)
        return self._external_test

    @property
    def bulk_operations(self) -> "BulkOperationsResource":
        """Get the bulk operations resource client."""
        if self._bulk_operations is None:
            from oobeya.resources.bulk_operations import BulkOperationsResource

            self._bulk_operations = BulkOperationsResource(self)
        return self._bulk_operations

    @property
    def api_keys(self) -> "ApiKeysResource":
        """Get the API keys resource client."""
        if self._api_keys is None:
            from oobeya.resources.api_keys import ApiKeysResource

            self._api_keys = ApiKeysResource(self)
        return self._api_keys

    @property
    def system(self) -> "SystemResource":
        """Get the system resource client."""
        if self._system is None:
            from oobeya.resources.system import SystemResource

            self._system = SystemResource(self)
        return self._system

    @property
    def organization_level(self) -> "OrganizationLevelResource":
        """Get the organization level resource client."""
        if self._organization_level is None:
            from oobeya.resources.organization_level import OrganizationLevelResource

            self._organization_level = OrganizationLevelResource(self)
        return self._organization_level

    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Full URL
        """
        return urljoin(self.base_url, endpoint.lstrip("/"))

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle API response and raise appropriate exceptions.

        Args:
            response: Response object from requests

        Returns:
            Parsed JSON response (unwrapped from payload if present)

        Raises:
            OobeyaAuthenticationError: For 401/403 responses
            OobeyaNotFoundError: For 404 responses
            OobeyaValidationError: For 400 responses
            OobeyaRateLimitError: For 429 responses
            OobeyaServerError: For 5xx responses
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status_code = response.status_code

            # Try to parse error message from response
            try:
                error_data = response.json()
                error_message = str(error_data)
            except Exception:
                error_message = response.text or str(e)

            if status_code == 401 or status_code == 403:
                raise OobeyaAuthenticationError(f"Authentication failed: {error_message}")
            elif status_code == 404:
                raise OobeyaNotFoundError(f"Resource not found: {error_message}")
            elif status_code == 400:
                raise OobeyaValidationError(f"Validation failed: {error_message}")
            elif status_code == 429:
                raise OobeyaRateLimitError(f"Rate limit exceeded: {error_message}")
            elif status_code >= 500:
                raise OobeyaServerError(f"Server error (HTTP {status_code}): {error_message}")
            else:
                raise OobeyaServerError(f"HTTP error (HTTP {status_code}): {error_message}")

        # Handle empty responses
        if not response.content:
            return None

        try:
            json_response = response.json()

            # Unwrap Oobeya response structure if present
            # Oobeya API wraps responses in: {"version": "1.0", "referenceId": "...", "payload": {...}}
            if isinstance(json_response, dict) and "payload" in json_response:
                return json_response["payload"]

            return json_response
        except ValueError as e:
            raise OobeyaServerError(f"Invalid JSON response: {str(e)}")

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make an HTTP request to the Oobeya API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json: JSON payload
            data: Form data
            files: Files to upload

        Returns:
            Parsed response data

        Raises:
            OobeyaTimeoutError: If request times out
            OobeyaConnectionError: If connection fails
            Various OobeyaError subclasses: For different HTTP errors
        """
        url = self._build_url(endpoint)

        try:
            # Remove Content-Type header for file uploads
            headers: Dict[str, Any] = {}
            if files is not None:
                headers["Content-Type"] = None  # Let requests set it with boundary

            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                files=files,
                timeout=self.timeout,
                headers=headers if files else {},
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout as e:
            raise OobeyaTimeoutError(f"Request timed out after {self.timeout} seconds: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise OobeyaConnectionError(f"Failed to connect to Oobeya API: {str(e)}")
        except (OobeyaAuthenticationError, OobeyaNotFoundError, OobeyaValidationError, OobeyaServerError):
            # Re-raise our custom exceptions
            raise

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request."""
        return self.request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a POST request."""
        return self.request("POST", endpoint, json=json, data=data, files=files)

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a PUT request."""
        return self.request("PUT", endpoint, json=json, files=files)

    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make a PATCH request."""
        return self.request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a DELETE request."""
        return self.request("DELETE", endpoint, params=params)

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self) -> "OobeyaClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()
