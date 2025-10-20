# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for utility functions."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from oobeya.utils import (
    build_query_params,
    camel_to_snake,
    format_datetime,
    from_dict,
    parse_datetime,
    snake_to_camel,
    to_dict,
)


class TestCaseConversion:
    """Test case conversion functions."""

    def test_snake_to_camel(self):
        """Test snake_case to camelCase conversion."""
        assert snake_to_camel("hello_world") == "helloWorld"
        assert snake_to_camel("api_key_name") == "apiKeyName"
        assert snake_to_camel("simple") == "simple"
        assert snake_to_camel("team_id") == "teamId"

    def test_camel_to_snake(self):
        """Test camelCase to snake_case conversion."""
        assert camel_to_snake("helloWorld") == "hello_world"
        assert camel_to_snake("apiKeyName") == "api_key_name"
        assert camel_to_snake("simple") == "simple"
        assert camel_to_snake("teamId") == "team_id"


class TestDataclassConversion:
    """Test dataclass conversion functions."""

    @dataclass
    class SampleModel:
        """Sample model for conversion tests."""

        user_name: str
        team_id: Optional[str] = None
        is_active: bool = True

    def test_to_dict_basic(self):
        """Test basic to_dict conversion."""
        model = self.SampleModel(user_name="john", team_id="team-1")
        result = to_dict(model)

        assert result["userName"] == "john"
        assert result["teamId"] == "team-1"
        assert result["isActive"] is True

    def test_to_dict_with_none(self):
        """Test to_dict filters None values."""
        model = self.SampleModel(user_name="john", team_id=None)
        result = to_dict(model)

        assert "userName" in result
        assert "teamId" not in result  # None values should be filtered
        assert "isActive" in result

    def test_to_dict_no_conversion(self):
        """Test to_dict without key conversion."""
        model = self.SampleModel(user_name="john")
        result = to_dict(model, convert_keys=False)

        assert "user_name" in result
        assert "userName" not in result

    def test_from_dict_basic(self):
        """Test basic from_dict conversion."""
        data = {"userName": "john", "teamId": "team-1", "isActive": False}
        result = from_dict(data, self.SampleModel)

        assert result is not None
        assert result.user_name == "john"
        assert result.team_id == "team-1"
        assert result.is_active is False

    def test_from_dict_none(self):
        """Test from_dict with None input."""
        result = from_dict(None, self.SampleModel)
        assert result is None


class TestDatetimeFunctions:
    """Test datetime utility functions."""

    def test_parse_datetime(self):
        """Test datetime parsing."""
        dt_str = "2025-01-15T10:30:00+00:00"
        result = parse_datetime(dt_str)

        assert result is not None
        assert isinstance(result, datetime)

    def test_parse_datetime_none(self):
        """Test parsing None datetime."""
        assert parse_datetime(None) is None
        assert parse_datetime("") is None

    def test_format_datetime(self):
        """Test datetime formatting."""
        dt = datetime(2025, 1, 15, 10, 30, 0)
        result = format_datetime(dt)

        assert result is not None
        assert "2025" in result
        assert "01" in result

    def test_format_datetime_none(self):
        """Test formatting None datetime."""
        assert format_datetime(None) is None


class TestQueryParams:
    """Test query parameter building."""

    def test_build_query_params(self):
        """Test building query parameters."""
        params = build_query_params(
            page=0,
            size=10,
            name="test",
            active=True,
        )

        assert params["page"] == 0
        assert params["size"] == 10
        assert params["name"] == "test"
        assert params["active"] == "true"  # Boolean converted to string

    def test_build_query_params_filters_none(self):
        """Test that None values are filtered out."""
        params = build_query_params(
            page=0,
            name=None,
            active=True,
        )

        assert "page" in params
        assert "name" not in params
        assert "active" in params

    def test_build_query_params_with_list(self):
        """Test building query parameters with lists."""
        params = build_query_params(
            ids=["id1", "id2", "id3"],
            tags=["tag1"],
        )

        assert params["ids"] == ["id1", "id2", "id3"]
        assert params["tags"] == ["tag1"]
