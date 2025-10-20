# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""
Oobeya Python Client Library

A Python library for interacting with the Oobeya API - Software Engineering Intelligence Platform.
"""

from oobeya.client import OobeyaClient
from oobeya.exceptions import (
    OobeyaError,
    OobeyaAuthenticationError,
    OobeyaNotFoundError,
    OobeyaValidationError,
    OobeyaServerError,
    OobeyaTimeoutError,
    OobeyaConnectionError,
)

__version__ = "0.1.0"
__all__ = [
    "OobeyaClient",
    "OobeyaError",
    "OobeyaAuthenticationError",
    "OobeyaNotFoundError",
    "OobeyaValidationError",
    "OobeyaServerError",
    "OobeyaTimeoutError",
    "OobeyaConnectionError",
]
