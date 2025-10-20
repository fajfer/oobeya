# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""
Custom exceptions for the Oobeya library.

All exceptions are clearly marked as library errors to distinguish them from API errors,
as the Oobeya API itself has limited error handling.
"""


class OobeyaError(Exception):
    """
    Base exception for all Oobeya library errors.

    All custom exceptions inherit from this base class and are prefixed with
    "[Oobeya Library]" to clearly identify them as library-level errors,
    not API-level errors.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the exception with a library-prefixed message.

        Args:
            message: The error message describing what went wrong
        """
        super().__init__(f"[Oobeya Library] {message}")
        self.original_message = message


class OobeyaAuthenticationError(OobeyaError):
    """
    Raised when authentication fails.

    This includes:
    - Missing API key
    - Invalid API key
    - Expired API key
    - Authorization header issues
    """

    pass


class OobeyaNotFoundError(OobeyaError):
    """
    Raised when a requested resource is not found (404).

    This typically occurs when:
    - Requesting a resource with an invalid ID
    - The resource has been deleted
    - The endpoint does not exist
    """

    pass


class OobeyaValidationError(OobeyaError):
    """
    Raised when request validation fails.

    This includes:
    - Missing required parameters
    - Invalid parameter types
    - Invalid parameter values
    - Schema validation failures
    """

    pass


class OobeyaServerError(OobeyaError):
    """
    Raised when the server returns a 5xx error.

    This indicates an issue on the Oobeya server side.
    """

    pass


class OobeyaTimeoutError(OobeyaError):
    """
    Raised when a request times out.

    This occurs when the server does not respond within the configured timeout period.
    """

    pass


class OobeyaConnectionError(OobeyaError):
    """
    Raised when a connection to the server cannot be established.

    This includes:
    - Network connectivity issues
    - DNS resolution failures
    - Server unreachable
    """

    pass


class OobeyaRateLimitError(OobeyaError):
    """
    Raised when rate limit is exceeded (429).

    This occurs when too many requests are made in a short period.
    """

    pass
