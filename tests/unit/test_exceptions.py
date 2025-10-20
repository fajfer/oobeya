# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for exception handling."""

from oobeya.exceptions import (
    OobeyaAuthenticationError,
    OobeyaConnectionError,
    OobeyaError,
    OobeyaNotFoundError,
    OobeyaRateLimitError,
    OobeyaServerError,
    OobeyaTimeoutError,
    OobeyaValidationError,
)


class TestExceptions:
    """Test custom exception classes."""

    def test_base_exception(self):
        """Test base OobeyaError exception."""
        error = OobeyaError("Test error")
        assert "[Oobeya Library]" in str(error)
        assert "Test error" in str(error)
        assert error.original_message == "Test error"

    def test_authentication_error(self):
        """Test OobeyaAuthenticationError."""
        error = OobeyaAuthenticationError("Invalid API key")
        assert "[Oobeya Library]" in str(error)
        assert "Invalid API key" in str(error)
        assert isinstance(error, OobeyaError)

    def test_not_found_error(self):
        """Test OobeyaNotFoundError."""
        error = OobeyaNotFoundError("Resource not found")
        assert "[Oobeya Library]" in str(error)
        assert "Resource not found" in str(error)
        assert isinstance(error, OobeyaError)

    def test_validation_error(self):
        """Test OobeyaValidationError."""
        error = OobeyaValidationError("Invalid parameters")
        assert "[Oobeya Library]" in str(error)
        assert "Invalid parameters" in str(error)
        assert isinstance(error, OobeyaError)

    def test_server_error(self):
        """Test OobeyaServerError."""
        error = OobeyaServerError("Internal server error")
        assert "[Oobeya Library]" in str(error)
        assert "Internal server error" in str(error)
        assert isinstance(error, OobeyaError)

    def test_timeout_error(self):
        """Test OobeyaTimeoutError."""
        error = OobeyaTimeoutError("Request timed out")
        assert "[Oobeya Library]" in str(error)
        assert "Request timed out" in str(error)
        assert isinstance(error, OobeyaError)

    def test_connection_error(self):
        """Test OobeyaConnectionError."""
        error = OobeyaConnectionError("Cannot connect")
        assert "[Oobeya Library]" in str(error)
        assert "Cannot connect" in str(error)
        assert isinstance(error, OobeyaError)

    def test_rate_limit_error(self):
        """Test OobeyaRateLimitError."""
        error = OobeyaRateLimitError("Rate limit exceeded")
        assert "[Oobeya Library]" in str(error)
        assert "Rate limit exceeded" in str(error)
        assert isinstance(error, OobeyaError)

    def test_exception_hierarchy(self):
        """Test that all exceptions inherit from OobeyaError."""
        exceptions = [
            OobeyaAuthenticationError,
            OobeyaNotFoundError,
            OobeyaValidationError,
            OobeyaServerError,
            OobeyaTimeoutError,
            OobeyaConnectionError,
            OobeyaRateLimitError,
        ]

        for exc_class in exceptions:
            assert issubclass(exc_class, OobeyaError)
            assert issubclass(exc_class, Exception)
