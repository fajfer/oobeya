# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for utility functions."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Union

from oobeya.utils import (
    _convert_value,
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


class TestAdvancedDataclassConversion:
    """Test advanced dataclass conversion scenarios."""

    @dataclass
    class NestedModel:
        """Nested model for testing."""

        name: str
        value: int = 0

    @dataclass
    class ParentModel:
        """Parent model with nested dataclass."""

        id: str
        nested: Optional["TestAdvancedDataclassConversion.NestedModel"] = None
        items: List["TestAdvancedDataclassConversion.NestedModel"] = field(default_factory=list)
        metadata: Optional[Dict[str, str]] = None

    @dataclass
    class DateTimeModel:
        """Model with datetime field."""

        created_at: Optional[datetime] = None
        updated_at: Optional[datetime] = None

    @dataclass
    class UnionModel:
        """Model with Union type."""

        value: Optional[str] = None

    def test_to_dict_with_dict_input(self):
        """Test to_dict with dict input."""
        data = {"user_name": "john", "team_id": "team-1"}
        result = to_dict(data)

        assert result["userName"] == "john"
        assert result["teamId"] == "team-1"

    def test_to_dict_with_dict_no_conversion(self):
        """Test to_dict with dict input without key conversion."""
        data = {"user_name": "john", "team_id": "team-1", "none_value": None}
        result = to_dict(data, convert_keys=False)

        assert result["user_name"] == "john"
        assert result["team_id"] == "team-1"
        assert "none_value" not in result

    def test_to_dict_with_list_input(self):
        """Test to_dict with list input."""
        data = [{"user_name": "john"}, {"user_name": "jane"}]
        result = to_dict(data)

        assert len(result) == 2
        assert result[0]["userName"] == "john"
        assert result[1]["userName"] == "jane"

    def test_to_dict_with_primitive(self):
        """Test to_dict with primitive input."""
        assert to_dict("hello") == "hello"
        assert to_dict(123) == 123
        assert to_dict(None) is None

    def test_to_dict_with_datetime(self):
        """Test to_dict with datetime values."""
        dt = datetime(2025, 1, 15, 10, 30, 0)
        model = self.DateTimeModel(created_at=dt)
        result = to_dict(model)

        assert "createdAt" in result
        assert "2025-01-15" in result["createdAt"]

    def test_to_dict_with_nested_dataclass(self):
        """Test to_dict with nested dataclass."""
        nested = self.NestedModel(name="test", value=42)
        parent = self.ParentModel(id="parent-1", nested=nested)
        result = to_dict(parent)

        assert result["id"] == "parent-1"
        assert result["nested"]["name"] == "test"
        assert result["nested"]["value"] == 42

    def test_convert_value_with_dict(self):
        """Test _convert_value with dict."""
        data = {"key": "value", "nested": {"inner": "data"}}
        result = _convert_value(data)

        assert result["key"] == "value"
        assert result["nested"]["inner"] == "data"

    def test_convert_value_with_list(self):
        """Test _convert_value with list."""
        data = ["a", "b", "c"]
        result = _convert_value(data)

        assert result == ["a", "b", "c"]

    def test_from_dict_with_non_dataclass(self):
        """Test from_dict with non-dataclass type."""
        data = {"key": "value"}
        result = from_dict(data, dict)  # type: ignore

        assert result == data

    def test_from_dict_with_datetime_field(self):
        """Test from_dict with datetime field."""
        data = {"createdAt": "2025-01-15T10:30:00+00:00"}
        result = from_dict(data, self.DateTimeModel)

        assert result is not None
        assert isinstance(result.created_at, datetime)

    def test_from_dict_with_datetime_already_parsed(self):
        """Test from_dict when datetime is already a datetime object."""
        dt = datetime(2025, 1, 15, 10, 30, 0)
        data = {"createdAt": dt}
        result = from_dict(data, self.DateTimeModel)

        assert result is not None
        assert result.created_at == dt

    def test_from_dict_with_list_field(self):
        """Test from_dict with list field."""
        data = {"id": "parent-1", "items": [{"name": "item1", "value": 1}, {"name": "item2", "value": 2}]}
        result = from_dict(data, self.ParentModel)

        assert result is not None
        assert len(result.items) == 2
        assert result.items[0]["name"] == "item1"  # List items are dicts without conversion

    def test_from_dict_with_dict_field(self):
        """Test from_dict with dict field."""
        data = {"id": "parent-1", "metadata": {"key1": "value1", "key2": "value2"}}
        result = from_dict(data, self.ParentModel)

        assert result is not None
        assert result.metadata == {"key1": "value1", "key2": "value2"}

    def test_from_dict_with_nested_dataclass(self):
        """Test from_dict with nested dataclass field."""
        # Note: The from_dict function requires a proper type hint, not a string forward reference
        # In practice, nested dataclasses are handled when the field_type is an actual dataclass type
        data = {"id": "parent-1", "nested": {"name": "nested-item", "value": 100}}
        result = from_dict(data, self.ParentModel)

        assert result is not None
        # Due to forward reference, nested is returned as dict
        assert result.nested == {"name": "nested-item", "value": 100}

    def test_from_dict_with_optional_field(self):
        """Test from_dict with Optional field."""
        data = {"value": "test-value"}
        result = from_dict(data, self.UnionModel)

        assert result is not None
        assert result.value == "test-value"


class TestParseDatetimeEdgeCases:
    """Test edge cases for parse_datetime."""

    def test_parse_datetime_invalid_format(self):
        """Test parsing invalid datetime format returns None."""
        result = parse_datetime("not a date")
        assert result is None

    def test_parse_datetime_valid_format(self):
        """Test parsing various valid datetime formats."""
        # ISO format
        result = parse_datetime("2025-01-15T10:30:00Z")
        assert result is not None

        # Date only
        result = parse_datetime("2025-01-15")
        assert result is not None


class TestFromDictUnionHandling:
    """Test Union type handling in from_dict."""

    @dataclass
    class ModelWithUnion:
        """Model with Union type (Optional is Union[T, None])."""

        value: Union[str, None] = None

    def test_from_dict_with_union_value(self):
        """Test from_dict with Union type having a value."""
        data = {"value": "test"}
        result = from_dict(data, self.ModelWithUnion)

        assert result is not None
        assert result.value == "test"

    def test_from_dict_with_union_none(self):
        """Test from_dict with Union type having None."""
        data = {"value": None}
        result = from_dict(data, self.ModelWithUnion)

        assert result is not None
        assert result.value is None


class TestConvertValueEdgeCases:
    """Test edge cases in _convert_value function."""

    def test_convert_value_none(self):
        """Test _convert_value with None."""
        result = _convert_value(None)
        assert result is None

    def test_convert_value_dataclass(self):
        """Test _convert_value with a dataclass instance."""

        @dataclass
        class SimpleModel:
            name: str

        model = SimpleModel(name="test")
        result = _convert_value(model)
        assert result == {"name": "test"}


class TestConvertFieldValueEdgeCases:
    """Test edge cases in _convert_field_value function."""

    @dataclass
    class ModelWithList:
        """Model with list field."""

        items: List[str] = field(default_factory=list)

    @dataclass
    class ModelWithOptional:
        """Model with optional field where None is second arg."""

        value: Union[str, None] = None

    @dataclass
    class ModelWithNonOptionalUnion:
        """Model with Union type that doesn't include None."""

        value: Union[str, int] = "default"

    def test_list_field_with_non_list_value(self):
        """Test list field when value is not actually a list."""
        # This tests the case where args exist but value is not a list
        data = {"items": "not-a-list"}
        result = from_dict(data, self.ModelWithList)

        assert result is not None
        # When value is not a list but type hint says List, it returns as-is
        assert result.items == "not-a-list"

    def test_union_field_where_none_is_first_arg(self):
        """Test Union field where None might be in different position."""
        data = {"value": "actual-value"}
        result = from_dict(data, self.ModelWithOptional)

        assert result is not None
        assert result.value == "actual-value"

    def test_union_field_without_none(self):
        """Test Union field that doesn't include None (e.g., Union[str, int])."""
        data = {"value": 42}
        result = from_dict(data, self.ModelWithNonOptionalUnion)

        assert result is not None
        assert result.value == 42
